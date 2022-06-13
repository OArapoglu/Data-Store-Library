from data.format.json_format import JSONFormat
from data.format.xml_format import XMLFormat
from data.format.file_format import FileFormat


class FileFormatFactory:
    """Factory for file formats."""

    @staticmethod
    def get_file_format(file_format: str, name: str) -> FileFormat:
        """
        Return the suitable file format class according to file format.

        Parameters:
            file_format(str): The format type of the file.
            name(str): The name of the file.
        """
        if file_format.upper() == "JSON":
            return JSONFormat(name)
        elif file_format.upper() == "XML":
            return XMLFormat(name)
        else:
            raise ValueError(format)
