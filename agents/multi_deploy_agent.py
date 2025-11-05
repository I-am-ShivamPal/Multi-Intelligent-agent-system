import threading
import time
import random
from datetime import datetime
import pandas as pd
import os
from core.realtime_bus import realtime_bus

class MultiDeployAgent:
    def __init__(self, agent_id: int, num_agents: int = 3):
        self.agent_id = agent_id
        self.num_agents = num_agents
        self.running = False
        self.deployment_count = 0
        self.log_file = "logs/deployment_log.csv"
        
        # Initialize log file
        os.makedirs("logs", exist_ok=True)
        if not os.path.exists(self.log_file):
            df = pd.DataFrame(columns=['timestamp', 'agent_id', 'status', 'latency_ms', 'details'])
            df.to_csv(self.log_file, index=False)
    
    def start(self):
        """Start the deploy agent"""
        self.running = True
        thread = threading.Thread(target=self._run_deployment_loop, daemon=True)
        thread.start()
        return thread
    
    def stop(self):
        """Stop the deploy agent"""
        self.running = False
    
    def _run_deployment_loop(self):
        """Main deployment loop"""
        while self.running:
            try:
                # Simulate deployment with random latency
                latency = random.randint(1000, 5000)  # 1-5 seconds
                success_rate = 0.85  # 85% success rate
                
                status = "success" if random.random() < success_rate else "failure"
                
                # Log deployment
                deployment_data = {
                    'timestamp': datetime.now().isoformat(),
                    'agent_id': self.agent_id,
                    'status': status,
                    'latency_ms': latency,
                    'details': f"Agent-{self.agent_id} deployment #{self.deployment_count + 1}"
                }
                
                # Write to CSV
                df = pd.DataFrame([deployment_data])
                df.to_csv(self.log_file, mode='a', header=False, index=False)
                
                # Publish to realtime bus
                realtime_bus.publish('deployments', {
                    'type': 'deployment_complete',
                    'agent_id': self.agent_id,
                    'status': status,
                    'latency_ms': latency,
                    'deployment_count': self.deployment_count + 1
                })
                
                self.deployment_count += 1
                
                # Random interval between deployments (2-8 seconds)
                time.sleep(random.uniform(2, 8))
                
            except Exception as e:
                print(f"Deploy Agent {self.agent_id} error: {e}")
                time.sleep(1)

class ScalingSimulator:
    def __init__(self, num_agents: int = 3):
        self.num_agents = num_agents
        self.agents = []
        self.threads = []
        self.running = False
    
    def start_simulation(self):
        """Start multiple deploy agents"""
        print(f"🚀 Starting {self.num_agents} deploy agents...")
        self.running = True
        
        for i in range(self.num_agents):
            agent = MultiDeployAgent(agent_id=i+1, num_agents=self.num_agents)
            thread = agent.start()
            self.agents.append(agent)
            self.threads.append(thread)
        
        # Log scaling event
        realtime_bus.publish('scaling', {
            'type': 'scale_up',
            'agent_count': self.num_agents,
            'message': f"Scaled up to {self.num_agents} deploy agents"
        })
        
        return self.agents
    
    def stop_simulation(self):
        """Stop all deploy agents"""
        print("🛑 Stopping deploy agents...")
        self.running = False
        
        for agent in self.agents:
            agent.stop()
        
        # Log scaling event
        realtime_bus.publish('scaling', {
            'type': 'scale_down',
            'agent_count': 0,
            'message': "Scaled down all deploy agents"
        })
    
    def get_stats(self):
        """Get deployment statistics"""
        total_deployments = sum(agent.deployment_count for agent in self.agents)
        return {
            'active_agents': len([a for a in self.agents if a.running]),
            'total_deployments': total_deployments,
            'avg_deployments_per_agent': total_deployments / len(self.agents) if self.agents else 0
        }

# Global simulator instance
scaling_simulator = ScalingSimulator()