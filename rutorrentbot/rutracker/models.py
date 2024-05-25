from pydantic import BaseModel
from typing import Optional


class FoundFile(BaseModel):
    object_name: str
    object_link: str
    object_data: Optional[dict] = None

    category: str

    download_size: str
    download_link: str
    magnet_link: Optional[str] = None
