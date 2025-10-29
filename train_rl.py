#!/usr/bin/env python3
"""Train RL agent across multiple scenarios."""

import subprocess
import sys

def train_rl():
    """Run 8 training scenarios to learn optimal strategies."""
    scenarios = [
        ["--dataset", "dataset/student_scores.csv", "--force-anomaly", "--planner", "rl", "--train"],
        ["--dataset", "dataset/patient_health.csv", "--force-anomaly", "--planner", "rl", "--train"],
        ["--dataset", "dataset/student_scores.csv", "--fail-type", "latency", "--planner", "rl", "--train"],
        ["--dataset", "dataset/patient_health.csv", "--fail-type", "crash", "--planner", "rl", "--train"],
        ["--dataset", "dataset/student_scores.csv", "--force-anomaly", "--planner", "rl"],
        ["--dataset", "dataset/patient_health.csv", "--force-anomaly", "--planner", "rl"],
        ["--dataset", "dataset/student_scores.csv", "--fail-type", "latency", "--planner", "rl"],
        ["--dataset", "dataset/patient_health.csv", "--fail-type", "crash", "--planner", "rl"]
    ]
    
    print("🧠 Training RL Agent - 8 scenarios")
    
    for i, args in enumerate(scenarios, 1):
        print(f"\n--- Run {i}/8 ---")
        try:
            subprocess.run([sys.executable, "main.py"] + args, 
                         input="y\n", text=True, timeout=60, check=False)
        except:
            pass
    
    print("\n✅ Training complete! Run 'python show_qtable.py' to see results.")

if __name__ == "__main__":
    train_rl()