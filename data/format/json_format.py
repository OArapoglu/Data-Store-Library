import json
from data.format.file_format import FileFormat


class JSONFormat(FileFormat):
    """JSON file format."""

    def __init__(self, name: str):
        super().__init__(name)

    @staticmethod
    def convert(data: dict[int:str]):
        """Convert the data in file format."""
        return json.dumps(data)
