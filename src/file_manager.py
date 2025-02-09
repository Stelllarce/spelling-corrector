class FileManager:
    """
    Class for reading and writing files.
    """
    def __init__(self, path: str) -> None:
        """
        :param path: Path to the file
        """
        self.path: str = path

    def read_file(self) -> str:
        """
        Read the file and return its content as a string.
        """
        with open(self.path, 'r', encoding='utf8') as file:
            return file.read()

    def write_file(self, data: str, new_path: str = None) -> None:
        """
        Write the data to the file.
        :param data: The data to write
        :param new_path: Optional new path to write to
        """
        if new_path is not None:
            self.path = new_path
        with open(self.path, 'w', encoding='utf8') as file:
            file.write(data)
