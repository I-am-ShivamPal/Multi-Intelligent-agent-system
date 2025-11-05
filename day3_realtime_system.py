#!/usr/bin/env python3
"""
Day 3: Real-Time Event Bus & Auto-Scaling Simulation
"""

import time
import threading
from datetime import datetime
from core.realtime_bus import realtime_bus
from agents.multi_deploy_agent import scaling_simulator

def monitor_bus_events():
    """Monitor and display real-time bus events"""
    def deployment_handler(message):
        print(f"📦 Deployment: Agent-{message['agent_id']} - {message['status']} ({message['latency_ms']}ms)")
    
    def scaling_handler(message):
        print(f"⚡ Scaling: {message['message']}")
    
    # Subscribe to events
    realtime_bus.subscribe('deployments', deployment_handler)
    realtime_bus.subscribe('scaling', scaling_handler)
    
    print("🔍 Monitoring real-time events...")

def run_day3_simulation(duration_minutes: int = 2):
    """Run Day 3 real-time simulation"""
    print("🚀 Day 3: Real-Time Event Bus & Auto-Scaling Simulation")
    print("=" * 60)
    
    # Start monitoring
    monitor_bus_events()
    
    # Start scaling simulation with 3 agents
    agents = scaling_simulator.start_simulation()
    
    try:
        # Run simulation for specified duration
        start_time = time.time()
        while time.time() - start_time < duration_minutes * 60:
            # Display stats every 10 seconds
            stats = realtime_bus.get_stats()
            agent_stats = scaling_simulator.get_stats()
            
            print(f"\n📊 Real-time Stats:")
            print(f"   Bus Throughput: {stats['throughput_per_sec']:.2f} msg/sec")
            print(f"   Total Messages: {stats['total_messages']}")
            print(f"   Active Agents: {agent_stats['active_agents']}")
            print(f"   Total Deployments: {agent_stats['total_deployments']}")
            
            time.sleep(10)
    
    except KeyboardInterrupt:
        print("\n⏹️ Simulation interrupted by user")
    
    finally:
        # Stop simulation
        scaling_simulator.stop_simulation()
        
        # Final stats
        final_stats = realtime_bus.get_stats()
        final_agent_stats = scaling_simulator.get_stats()
        
        print(f"\n🏁 Final Results:")
        print(f"   Total Runtime: {final_stats['uptime_seconds']:.1f} seconds")
        print(f"   Messages Processed: {final_stats['total_messages']}")
        print(f"   Average Throughput: {final_stats['throughput_per_sec']:.2f} msg/sec")
        print(f"   Total Deployments: {final_agent_stats['total_deployments']}")
        print(f"   Performance Log: logs/performance_log.csv")
        print(f"   Deployment Log: logs/deployment_log.csv")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Day 3 Real-Time System Simulation")
    parser.add_argument("--duration", type=int, default=2, help="Simulation duration in minutes")
    parser.add_argument("--agents", type=int, default=3, help="Number of deploy agents")
    
    args = parser.parse_args()
    
    # Configure scaling simulator
    scaling_simulator.num_agents = args.agents
    
    # Run simulation
    run_day3_simulation(args.duration)