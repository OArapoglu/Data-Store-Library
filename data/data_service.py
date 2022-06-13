"""
    DATA Service.

    This module manages data store library.

"""
from typing import Optional, Any
from db.db_service import sqlalchemy_session
from orm.orm_service import FileType, DestinationType, Record, RecordFileDestination
from data.format.file_format_factory import FileFormatFactory
from data.destination.file_destination_factory import FileDestinationFactory


class DataService:
    """Data management service."""

    __instance = None
    __engine = None

    @staticmethod
    def get_instance():
        """Static access method."""
        if DataService.__instance is None:
            DataService()
        return DataService.__instance

    def __init__(self):
        """Virtually private constructor."""
        if DataService.__instance is not None:
            raise Exception("DataService is a singleton!")
        else:
            DataService.__instance = self
            self.__session = sqlalchemy_session()

    def put(
        self,
        records,
        files,
        destinations,
    ):
        """Insert records in multiple formats and into multiple destinations."""
        try:
            record_file_destinations = []
            for record_item in records:
                for file in files:
                    file_type = (
                        self.__session.query(FileType)
                        .filter(FileType.description == file["file_type"])
                        .first()
                    )
                    record = (
                        self.__session.query(Record)
                        .filter(Record.key == record_item["key"])
                        .first()
                    )
                    if file_type and record is None:
                        file_format_factory = FileFormatFactory()
                        file_format = file_format_factory.get_file_format(
                            file["file_type"], file["name"]
                        )
                        file_data = file_format.convert(record_item)
                        for destination in destinations:
                            destination_type = (
                                self.__session.query(DestinationType)
                                .filter(
                                    DestinationType.description
                                    == destination["destination_type"]
                                )
                                .first()
                            )
                            if destination_type:
                                file_destination_factory = FileDestinationFactory()
                                file_destination = file_destination_factory.get_file(
                                    destination["destination_type"], destination["path"]
                                )
                                file_destination.write(file_data, file["name"])
                                record_file_destination = RecordFileDestination(
                                    file["name"],
                                    destination["path"],
                                    file_type.id,
                                    destination_type.id,
                                    record_item["key"],
                                )
                                record_file_destinations.append(record_file_destination)
                self.__session.add_all(record_file_destinations)
                record = Record(record_item["key"], record_item["value"])
                self.__session.add(record)
            if self.__session.is_modified:
                self.__session.commit()
        except:
            self.__session.rollback()
            return 500
        finally:
            self.__session.close()

    def update(
        self,
        records,
    ):
        """Update records in multiple formats and into multiple destinations."""
        try:
            for record_item in records:
                record_file_destinations = (
                    self.__session.query(RecordFileDestination)
                    .filter(RecordFileDestination.record_id == record_item["key"])
                    .all()
                )
                for record_file_destination in record_file_destinations:
                    file_type = (
                        self.__session.query(FileType)
                        .filter(FileType.id == record_file_destination.file_type_id)
                        .first()
                    )
                    destination_type = (
                        self.__session.query(DestinationType)
                        .filter(
                            DestinationType.id
                            == record_file_destination.destination_type_id
                        )
                        .first()
                    )
                    if file_type and destination_type:
                        file_format_factory = FileFormatFactory()
                        file_format = file_format_factory.get_file_format(
                            file_type.description, record_file_destination.name
                        )
                        file_data = file_format.convert(record_item)
                        file_destination_factory = FileDestinationFactory()
                        file_destination = file_destination_factory.get_file(
                            destination_type.description, record_file_destination.path
                        )
                        file_destination.write(file_data, record_file_destination.name)
                self.__session.query(Record).filter(
                    Record.key == record_item["key"]
                ).update({"value": record_item["value"]})
            if self.__session.is_modified:
                self.__session.commit()
        except:
            self.__session.rollback()
            return 500
        finally:
            self.__session.close()

    def delete(self, record_keys: list):
        """Delete records from multiple destinations."""
        try:
            for key in record_keys:
                record_file_destinations = (
                    self.__session.query(RecordFileDestination)
                    .filter(RecordFileDestination.record_id == key)
                    .all()
                )
                for record_file_destination in record_file_destinations:
                    destination_type = (
                        self.__session.query(DestinationType)
                        .filter(
                            DestinationType.id
                            == record_file_destination.destination_type_id
                        )
                        .first()
                    )
                    if destination_type:
                        file_destination_factory = FileDestinationFactory()
                        file_destination = file_destination_factory.get_file(
                            destination_type.description, record_file_destination.path
                        )
                        file_destination.delete(record_file_destination.name)
                self.__session.query(RecordFileDestination).filter(
                    RecordFileDestination.record_id == key
                ).delete()
                self.__session.query(Record).filter(Record.key == key).delete()

            if self.__session.is_modified:
                self.__session.commit()
        except:
            self.__session.rollback()
            return 500
        finally:
            self.__session.close()

    def filter_records(
        self,
        value: str,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Any:
        """Filter records from multiple destinations."""
        try:
            query = f"""
                SELECT rfd.name, rfd.path, ft.description, dt.description FROM record_file_destination rfd
                INNER JOIN record r ON r.key = rfd.record_id and r.value = {value}
                INNER JOIN file_type ft ON ft.id = rfd.file_type_id
                INNER JOIN destination_type dt ON dt.id = rfd.destination_type_id
            """
            if limit:
                query += f" LIMIT {limit}"
            if offset:
                query += f" OFFSET {offset}"
            results = []
            record_dict = {}
            for result in self.__session.connection().execute(query):
                record_dict["name"] = result[0]
                record_dict["path"] = result[1]
                record_dict["file_format"] = result[2]
                record_dict["file_destination"] = result[3]
                results.append(record_dict)
            return results
        except:
            self.__session.rollback()
            return 500
        finally:
            self.__session.close()
