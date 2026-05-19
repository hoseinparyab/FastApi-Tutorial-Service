from pydantic import BaseModel, field_validator


class BasePersonShchema(BaseModel):
    name: str

    @field_validator("name")
    def validate_name(cls, value):
        if len(value) > 32:
            raise ValueError("32 charchter nist")
        if not value.isalpha():
            raise ValueError("our errors..")
        return value


class PersonSchema(BasePersonShchema):
    pass


class PersonResponseSchema(BasePersonShchema):
    id: int


class PersonResponseUpdateSchema(BasePersonShchema):
    pass
