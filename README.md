# Aerospace Satellite Manager (OpenEnv) 🛰️

## Environment Overview & Motivation
The Aerospace Satellite Manager is a resource-constrained Reinforcement Learning environment where an AI agent must balance power consumption against data transmission requirements while orbiting Earth. It simulates a real-world aerospace operations task where agents must anticipate predictable environmental changes (the Earth's shadow) and make precise trade-offs between completing objectives and catastrophic battery failure.

## Observation Space (Pydantic Typed)
* `battery_level` (float): Current power reserves (0.0 to 100.0).
* `storage_used` (float): Current onboard data storage capacity utilized (0.0 to 100.0).
* `in_sunlight` (bool): Environmental flag dictating if solar charging is currently possible.

## Action Space (Pydantic Typed)
* `take_photo`: Consumes 5.0 power, increases storage by 25.0.
* `transmit_data`: Consumes 15.0 power, successfully clears storage to 0.0.
* `sleep`: Recharges battery by 20.0 (if in sunlight) or passively drains by 2.0 (if in darkness).

## Task Descriptions & Difficulty Levels
The environment features a programmatic grader that evaluates trajectories and returns a strict `0.0` to `1.0` score across three increasing difficulty levels:
1. **Easy (`task_1_easy_survival`)**: The agent must survive 1 full orbit (10 steps) without the battery ever reaching 0%.
2. **Medium (`task_2_medium_transmission`)**: The agent must survive 2 orbits (20 steps) and successfully transmit at least 50MB of data. Partial credit is awarded based on data sent.
3. **Hard (`task_3_hard_maximization`)**: The agent must survive 3 orbits (30 steps) and maximize data transmission under severe power constraints (Requires 150+ data transmitted for a perfect 1.0 score).

## Setup and Usage Instructions

### 1. Containerized Execution (Local)
To run the environment server locally via Docker:
```bash
docker build -t satellite_env:v2 .
docker run -p 8000:8000 satellite_env:v2
