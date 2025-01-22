class FileManager:
    def __init__(self, path: str) -> None:
        self.path: str = path

    def read_file(self) -> str:
        with open(self.path, 'r', encoding='utf8') as file:
            return file.read()

    def write_file(self, data: str, new_path: str = None) -> None:
        if new_path is not None:
            self.path = new_path
        with open(self.path, 'w', encoding='utf8') as file:
            file.write(data)
