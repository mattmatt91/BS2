from pydantic import BaseModel
from typing import Union, Optional, List

class ParameterModel(BaseModel):
    parameter: str
    datatype: str
    value: Union[float, bool, str]
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    entrys: List[str] = []

class ParameterUpdateModel(BaseModel):
    parameter: str
    value: Union[float, bool, str] 