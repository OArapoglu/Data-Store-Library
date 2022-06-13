from dict2xml import dict2xml
from data.format.file_format import FileFormat


class XMLFormat(FileFormat):
    """XML File Format"""

    def __init__(self, name: str):
        super().__init__(name)

    def convert(self, data: dict[int:str]):
        """Convert the data in file format."""
        xml_file = dict2xml(data)
        xml_file = "<data>" + xml_file + "</data>"
        return xml_file
