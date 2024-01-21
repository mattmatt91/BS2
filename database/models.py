from pydantic import BaseModel
from typing import Optional, Union, List


class SensorData(BaseModel):
    timestamp: str
    humidity: float
    temperature: float
    pressure: float
    lamp_bloom: bool
    lamp_grow: bool
    fan: bool
    pH: float
    ec: float
    temp_water: float
    pump_ph_up: bool
    pump_ph_down: bool
    pump_fertiliser: bool


class ParameterData(BaseModel):
    parameter: str
    datatype: str
    value: Union[float, bool, str]
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    entrys: List[str] = []
