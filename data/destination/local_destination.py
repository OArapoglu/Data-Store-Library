import os
from typing import Any
from data.format.file_format import FileFormat
from data.destination.file_destination import FileDestination


class LocalDestination(FileDestination):
    """File Destination."""

    def __init__(self, path: str):
        super().__init__(path)

    def write(self, data: Any, name: str):
        """Write the related destination."""
        with open(os.path.join(self.path, name), "w", encoding="utf-8") as f:
            f.write(data)

    def read(self) -> FileFormat:
        """Read the related destination."""
        with open(self.path, "r+") as d:
            data = d.read()
            return data

    def delete(self, name: str):
        """Write the related destination."""
        file_path = os.path.join(self.path, name)
        if os.path.exists(file_path):
            os.remove(file_path)
