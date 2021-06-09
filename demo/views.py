from fastapi import APIRouter, Depends

from demo.api_formats import ConcatRequest, ConcatResponse
from demo.service import concat_values 


router = APIRouter()


@router.get('/concat')
def concat(concat_req: ConcatRequest = Depends()) -> ConcatResponse:
    result = concat_values(concat_req.value_string, concat_req.value_integer)
    return ConcatResponse(data=result)
