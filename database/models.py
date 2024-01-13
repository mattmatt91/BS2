from pydantic import BaseModel
from typing import Optional, Union, List

class SensorData(BaseModel):
    timestamp: str
    humidity: float
    temperature: float
    pressure:float
    lamp_bloom: bool
    lamp_grow: bool
    fan: bool

class ParameterData(BaseModel):
    parameter: str
    datatype: str
    value: Union[float, bool, str] 
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    entrys: List[str] = []
