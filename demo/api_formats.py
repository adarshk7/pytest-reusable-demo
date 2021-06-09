from typing import Optional

from pydantic import BaseModel


class ConcatRequest(BaseModel):
    value_string: str
    value_integer: int
    value_string_optional: Optional[str]


class ConcatResponse(BaseModel):
    data: str

