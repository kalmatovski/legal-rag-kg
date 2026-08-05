from pydantic import BaseModel

class AskRequest(BaseModel):
    question:str
    top_k:int = 5

class SourceArticle(BaseModel):
    number:str
    title:str
    chapter_title:str | None = None

class AskResponse(BaseModel):
    answer:str
    sources:list[SourceArticle]