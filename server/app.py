import uvicorn
from openenv_core.env_server import create_app
from .env import SatelliteEnv
from .schema import SatelliteAction, SatelliteObservation

app = create_app(
    SatelliteEnv(),
    SatelliteAction,
    SatelliteObservation,
    env_name="aerospace_satellite_manager"
)

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
