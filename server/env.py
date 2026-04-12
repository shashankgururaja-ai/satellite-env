from .schema import SatelliteObservation, SatelliteAction

class SatelliteEnv:
    def __init__(self):
        # Initialize the starting state
        self.battery_level = 100.0
        self.storage_used = 0.0
        self.in_sunlight = True

    def reset(self) -> SatelliteObservation:
        # Reset the environment back to the starting conditions
        self.battery_level = 100.0
        self.storage_used = 0.0
        self.in_sunlight = True
        
        # CORRECT: Return the dataclass object, NOT a dictionary
        return SatelliteObservation(
            battery_level=self.battery_level,
            storage_used=self.storage_used,
            in_sunlight=self.in_sunlight
        )

    def step(self, action: SatelliteAction) -> SatelliteObservation:
        # Extract the action string sent by the grader
        action_name = action.action.lower()
        
        # Simple game logic (modify values based on action)
        if action_name == "take_photo":
            self.battery_level -= 10.0
            self.storage_used += 20.0
        elif action_name == "transmit_data":
            self.battery_level -= 15.0
            self.storage_used = max(0.0, self.storage_used - 50.0) # Prevent negative storage
        elif action_name == "sleep":
            if self.in_sunlight:
                self.battery_level = min(100.0, self.battery_level + 20.0) # Charge battery

        # Safety check: Keep battery between 0 and 100
        self.battery_level = max(0.0, min(100.0, self.battery_level))
        
        # CORRECT: Return the dataclass object, NOT a dictionary
        return SatelliteObservation(
            battery_level=self.battery_level,
            storage_used=self.storage_used,
            in_sunlight=self.in_sunlight
        )
