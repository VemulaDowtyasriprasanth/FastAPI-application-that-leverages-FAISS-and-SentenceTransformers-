from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class Document(BaseModel):
    content: str
    content_type: str  # "pdf", "html", or "url"

class LoadResponse(BaseModel):
    document_id: int
    message: str

class RetrieveRequest(BaseModel):
    query: str

class RetrieveResponse(BaseModel):
    document_ids: List[int]
    contents: List[str]
