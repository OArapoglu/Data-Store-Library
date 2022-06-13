from abc import ABC, abstractmethod


class FileFormat(ABC):
    """This is an abstract class for file format objects."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def convert(self, data: dict[int:str]):
        """Convert the data into the related file format."""
