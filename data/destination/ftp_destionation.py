import os
from ftplib import FTP
from typing import Any
from data.format.file_format import FileFormat
from data.destination.file_destination import FileDestination


class FTPDestination(FileDestination):
    """File Destination."""

    def __init__(self, path: str):
        super().__init__(path)
        self.hostname = "ftp.test.com"
        self.username = "admin"
        self.password = "password"

    def write(self, data: Any, name: str):
        """Write the related destination."""
        with open(self.path, "w") as f:
            ftp = self.__connect()
            ftp.storlines(f"STOR {self.filename}", f)

    def read(self) -> FileFormat:
        """Write the related destination."""
        ftp = self.__connect()
        data = ""
        ftp.retrlines(f"RETR {self.filename}", lambda x: data + f"{x}\n")
        ftp.close()

    def delete(self, name: str):
        """Write the related destination."""
        ftp = self.__connect()
        file_path = os.path.join(self.path, name)
        ftp.delete(file_path)

    def connect(self) -> FTP:
        connection = FTP(self.hostname, self.username, self.password)
        return connection
