from pydantic import BaseModel, Field
from typing import Literal

class SatelliteAction(BaseModel):
    action: Literal["take_photo", "transmit_data", "sleep"] = Field(
        ..., description="Action to perform: take_photo (uses 5 power, +25 storage), transmit_data (uses 15 power, clears storage), sleep (recharges in sun, drains in dark)."
    )

class SatelliteObservation(BaseModel):
    battery_level: float = Field(..., description="Battery from 0.0 to 100.0")
    storage_used: float = Field(..., description="Storage from 0.0 to 100.0")
    in_sunlight: bool = Field(..., description="True if in sunlight, False if in darkness")

class SatelliteState(BaseModel):
    step_count: int
    total_data_transmitted: float
    is_dead: bool
    current_task: str