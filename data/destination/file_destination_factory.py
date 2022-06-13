from data.destination.ftp_destionation import FTPDestination
from data.destination.local_destination import LocalDestination
from data.destination.file_destination import FileDestination


class FileDestinationFactory:
    """Factory for file destinations."""

    @staticmethod
    def get_file(destination_type: str, path: str) -> FileDestination:
        """
        Return the suitable file destination class according to the destination type.

        Parameters:
            path(str): The format type of the file.
            destination_type(str): The name of the file.
        """
        if destination_type.upper() == "FTP":
            return FTPDestination(path)
        elif destination_type.upper() == "LOCAL":
            return LocalDestination(path)
        else:
            raise ValueError(format)
