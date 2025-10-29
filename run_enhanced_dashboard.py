#!/usr/bin/env python3
"""Launch enhanced InsightFlow dashboard."""

import subprocess
import sys
import os

def main():
    # Ensure telemetry directory exists
    os.makedirs("insightflow", exist_ok=True)
    
    # Initialize telemetry file if not exists
    if not os.path.exists("insightflow/telemetry.json"):
        with open("insightflow/telemetry.json", 'w') as f:
            f.write("[]")
    
    print("🚀 Starting InsightFlow Dashboard...")
    print("📊 Real-time agent monitoring enabled")
    print("🔄 Auto-refresh every 5 seconds")
    print("💡 Toggle between User/Developer modes")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "dashboard/dashboard.py",
            "--server.port=8501"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped")

if __name__ == "__main__":
    main()