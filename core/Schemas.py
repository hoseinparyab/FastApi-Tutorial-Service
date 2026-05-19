from pydantic import BaseModel


class BasePersonShchema(BaseModel):
    name: str


class PersonSchema(BasePersonShchema):
    pass


class PersonResponseSchema(BasePersonShchema):
    id: int


class PersonResponseUpdateSchema(BasePersonShchema):
    pass
