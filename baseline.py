import os
import json
from openai import OpenAI
from openenv_core import EnvClient

def run_inference():
    # 1. Enforce Mandatory Environment Variables
    api_base_url = os.getenv("API_BASE_URL", "https://api-inference.huggingface.co/v1/")
    model_name = os.getenv("MODEL_NAME", "meta-llama/Meta-Llama-3-8B-Instruct")
    hf_token = os.getenv("HF_TOKEN")

    if not hf_token:
        print("ERROR: HF_TOKEN environment variable is not set. Please set it before running.")
        return

    # 2. Setup the OpenAI Client using the required variables
    llm_client = OpenAI(
        base_url=api_base_url,
        api_key=hf_token
    )
    
    client = EnvClient("http://localhost:8000")
    
    # 3. Define the Tasks
    tasks = [
        "task_1_easy_survival",
        "task_2_medium_transmission",
        "task_3_hard_maximization"
    ]

    for task_id in tasks:
        # STRICT LOGGING: [START]
        start_log = {"task_id": task_id, "environment_name": "aerospace_satellite_manager"}
        print(f"[START] {json.dumps(start_log)}")
        
        obs = client.reset()
        done = False
        step_count = 0
        total_reward = 0.0
        final_grade = 0.0
        
        while not done:
            # Prompt the LLM
            prompt = f"""
            You are a satellite. Choose an action.
            Status: {obs}
            Task: {task_id}
            Reply with ONLY ONE word: 'take_photo', 'transmit_data', or 'sleep'.
            """
            
            response = llm_client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10
            )
            
            # Clean AI response
            action_text = response.choices[0].message.content.strip().lower()
            if action_text not in ["take_photo", "transmit_data", "sleep"]:
                action_text = "sleep" # Fallback
            
            # Execute step
            next_obs, reward, done, info = client.step({"action": action_text})
            
            # STRICT LOGGING: [STEP]
            step_log = {
                "step": step_count,
                "observation": obs,
                "action": action_text,
                "reward": reward,
                "done": done,
                "info": info
            }
            print(f"[STEP] {json.dumps(step_log)}")
            
            # Update variables
            obs = next_obs
            total_reward += reward
            step_count += 1
            
            if done:
                final_grade = info.get("grade", 0.0)
                
        # STRICT LOGGING: [END]
        end_log = {
            "task_id": task_id,
            "total_reward": total_reward,
            "grade": final_grade,
            "success": final_grade >= 1.0
        }
        print(f"[END] {json.dumps(end_log)}")

if __name__ == "__main__":
    run_inference()