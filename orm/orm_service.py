"""
    ORM Service.

    This module keeps the models of the DB tables.
    Initial data is automatically stored into DB.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from db.db_service import sqlalchemy_session


db = SQLAlchemy()


class Record(db.Model):
    """Record model."""

    __tablename__ = "record"

    key = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String)

    def __init__(self, key: int, value: str):
        self.key = key
        self.value = value


class DestinationType(db.Model):
    """Destination type model."""

    __tablename__ = "destination_type"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)

    def __init__(self, description: str):
        self.description = description


class FileType(db.Model):
    """File type model."""

    __tablename__ = "file_type"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)

    def __init__(self, description: str):
        self.description = description


class RecordFileDestination(db.Model):
    """Record, file and destination model."""

    __tablename__ = "record_file_destination"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    path = db.Column(db.String)
    file_type_id = db.Column(db.Integer, db.ForeignKey("file_type.id"))
    destination_type_id = db.Column(db.Integer, db.ForeignKey("destination_type.id"))
    record_id = db.Column(db.Integer, db.ForeignKey("record.key"))

    def __init__(
        self,
        name: str,
        path: str,
        file_type_id: int,
        destination_type_id: int,
        record_id: int,
    ):
        self.name = name
        self.path = path
        self.file_type_id = file_type_id
        self.destination_type_id = destination_type_id
        self.record_id = record_id


class User(db.Model, UserMixin):
    """User model for authentication."""

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    api_key = db.Column(db.String)


class ORMService:
    """ORM management service."""

    __instance = None
    __engine = None

    @staticmethod
    def get_instance():
        """Static access method."""
        if ORMService.__instance is None:
            ORMService()
        return ORMService.__instance

    def __init__(self):
        """Virtually private constructor."""
        if ORMService.__instance is not None:
            raise Exception("ORMService is a singleton!")
        else:
            ORMService.__instance = self
            self.__session = sqlalchemy_session()

    def insert_initial_data(self):
        """Insert initial data of the tables."""
        try:
            file_types = ["XML", "JSON"]
            for file_type in file_types:
                ft = (
                    self.__session.query(FileType)
                    .filter(FileType.description == file_type)
                    .first()
                )
                if ft is None:
                    ft = FileType(file_type)
                    self.__session.add(ft)

            destination_types = ["LOCAL", "FTP"]
            for destination_type in destination_types:
                dt = (
                    self.__session.query(DestinationType)
                    .filter(DestinationType.description == destination_type)
                    .first()
                )
                if dt is None:
                    dt = DestinationType(destination_type)
                    self.__session.add(dt)

            admin_user = (
                self.__session.query(User).filter(User.username == "admin").first()
            )
            if admin_user is None:
                user = User()
                user.username = "admin"
                user.api_key = "bWFnZ2llOnN1bW1lcnk="
                self.__session.add(user)

            if self.__session.is_modified:
                self.__session.commit()
        except:
            self.__session.rollback()
        finally:
            self.__session.close()
