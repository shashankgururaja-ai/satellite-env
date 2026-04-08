from openenv_core.env_server import create_app
from .env import SatelliteEnv
from .schema import SatelliteAction, SatelliteObservation

# We now pass the environment and models directly without keywords!
app = create_app(
    lambda: SatelliteEnv(),
    SatelliteAction,
    SatelliteObservation,
    env_name="aerospace_satellite_manager"
)
