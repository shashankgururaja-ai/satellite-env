from dataclasses import dataclass

@dataclass
class SatelliteObservation:
    battery_level: float
    storage_used: float
    in_sunlight: bool

@dataclass
class SatelliteAction:
    action: str
