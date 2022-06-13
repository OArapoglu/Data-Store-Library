from abc import ABC, abstractmethod
from data.format.file_format import FileFormat
from typing import Any


class FileDestination(ABC):
    """This is an abstract class for file destination objects."""

    def __init__(self, path: str):
        self.path = path

    @abstractmethod
    def write(self, data: Any, name: str):
        """Write the related destination."""

    @abstractmethod
    def read(self) -> FileFormat:
        """Write the related destination."""

    @abstractmethod
    def delete(self):
        """Write the related destination."""
