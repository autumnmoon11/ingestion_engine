from abc import ABC, abstractmethod

class Destination(ABC):
    @abstractmethod
    def write(self, data: dict) -> None:
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

class FileDestination(Destination):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def write(self, data: dict) -> None:
        self.file.write(",".join(map(str, data.values())) + "\n")

    def __enter__(self):
        self.file = open(self.file_path, "w")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()

class ConsoleDestination(Destination):
    def write(self, data: dict) -> None:
        print(data)

class CloudDestination(Destination):
    def __init__(self, cloud_provider: str):
        self.cloud_provider = cloud_provider

    def write(self, data: dict) -> None:
        print(f"Writing data to {self.cloud_provider}: {data}")