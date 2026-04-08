from .schema import SatelliteAction, SatelliteObservation, SatelliteState

class SatelliteEnv:
    def __init__(self):
        # Default to the hardest task, but can be changed during reset
        self.current_task = "task_3_hard_maximization"
        self.reset(self.current_task)

    def reset(self, task_id: str = "task_3_hard_maximization") -> SatelliteObservation:
        self.current_task = task_id
        self.battery = 100.0
        self.storage = 0.0
        self.step_count = 0
        self.total_data_transmitted = 0.0
        self.is_dead = False
        
        # Set difficulty parameters based on task
        if "easy" in self.current_task:
            self.max_steps = 10
        elif "medium" in self.current_task:
            self.max_steps = 20
        else:
            self.max_steps = 30 # Hard
            
        return self._get_obs()

    def state(self) -> dict:
        return SatelliteState(
            step_count=self.step_count,
            total_data_transmitted=self.total_data_transmitted,
            is_dead=self.is_dead,
            current_task=self.current_task
        ).model_dump()

    def _get_obs(self) -> SatelliteObservation:
        in_sunlight = (self.step_count % 10) < 5
        return SatelliteObservation(
            battery_level=round(self.battery, 2),
            storage_used=round(self.storage, 2),
            in_sunlight=in_sunlight
        )

    def step(self, action: SatelliteAction):
        obs = self._get_obs()
        reward = 0.0 # Meaningful incremental reward
        
        if action.action == "sleep":
            if obs.in_sunlight:
                self.battery = min(100.0, self.battery + 20.0)
                reward += 0.1 # Tiny reward for charging properly
            else:
                self.battery -= 2.0
                
        elif action.action == "take_photo":
            self.battery -= 5.0
            if self.storage < 100.0:
                self.storage += 25.0
                reward += 0.5 # Incremental progress
            else:
                reward -= 1.0 # Penalize destructive/wasted action

        elif action.action == "transmit_data":
            self.battery -= 15.0
            if self.storage > 0:
                self.total_data_transmitted += self.storage
                reward += (self.storage * 0.1) # Big reward for sending data
                self.storage = 0.0 
            else:
                reward -= 1.0 # Penalize transmitting empty drive
                
        # Check death condition
        if self.battery <= 0.0:
            self.battery = 0.0
            self.is_dead = True
            reward -= 10.0 # Huge penalty for infinite loop / dying
            
        self.step_count += 1
        done = self.is_dead or (self.step_count >= self.max_steps)
        
        # --- THE PROGRAMMATIC GRADER (0.0 to 1.0) ---
        grade = 0.0
        if done:
            if "easy" in self.current_task:
                # Goal: Just survive
                grade = 0.0 if self.is_dead else 1.0
            elif "medium" in self.current_task:
                # Goal: Survive AND transmit 50+ data
                if not self.is_dead and self.total_data_transmitted >= 50.0:
                    grade = 1.0
                elif not self.is_dead:
                    grade = self.total_data_transmitted / 50.0 # Partial credit
            else:
                # Goal: Hard Maximization (Perfect score requires 150+ data transmitted)
                if self.is_dead:
                    grade = 0.0
                else:
                    grade = min(1.0, self.total_data_transmitted / 150.0)

        # OpenEnv strictly expects: obs, reward, done, info
        info = {"grade": grade, "state": self.state()}
        
        return self._get_obs(), reward, done, info