from openenv_core.env_server import create_app
from .env import SatelliteEnv
from .schema import SatelliteAction, SatelliteObservation

app = create_app(
    SatelliteEnv(),
    SatelliteAction,
    SatelliteObservation,
    env_name="aerospace_satellite_manager"
)
