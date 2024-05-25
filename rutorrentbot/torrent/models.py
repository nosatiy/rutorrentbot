from pydantic import BaseModel


class DownloadedFile(BaseModel):
    file_name: str
    file_path: str
    delete_path: str