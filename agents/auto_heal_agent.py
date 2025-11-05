import random
import os
import csv
import datetime
import shutil
from utils import trigger_dashboard_deployment
from core.base_agent import BaseAgent

class AutoHealAgent(BaseAgent):
    """A simple agent that can execute healing strategies."""
    def __init__(self, healing_log_file):
        self.strategies = ['retry_deployment', 'restore_previous_version', 'adjust_thresholds']
        super().__init__(healing_log_file, "AutoHealAgent")
        self.logger.info("Agent ready", strategies=len(self.strategies))
    
    def get_log_headers(self) -> list:
        return ["timestamp", "strategy", "status", "response_time_ms"]
    
    def run(self):
        pass  # Called by external systems

    def _log_healing_attempt(self, strategy, status, response_time):
        """Log healing attempt using base class method."""
        self._log_entry({
            "strategy": strategy,
            "status": status,
            "response_time_ms": round(response_time, 2)
        })

    def attempt_healing(self, state, dataset_path):
        """Chooses a random healing strategy and executes it."""
        strategy = random.choice(self.strategies)
        print(f"\n--- Auto-Heal Agent: Initiating random recovery for state '{state}' ---")
        # This now calls the new, centralized execution method
        return self.execute_action(strategy, dataset_path)

    def execute_action(self, strategy, dataset_path):
        """
        Executes a specific, chosen healing strategy.
        This allows the RL Trainer to command this agent.
        """
        self.logger.info(f"Executing healing strategy", strategy=strategy, dataset=dataset_path)
        status, response_time = "failure", 0
        heal_type = "unknown_strategy"

        if strategy == 'retry_deployment':
            status, response_time = self._retry_deployment()
            heal_type = "heal_retry"
        elif strategy == 'restore_previous_version':
            status, response_time = self._restore_previous_version(dataset_path)
            heal_type = "heal_restore"
        elif strategy == 'adjust_thresholds':
            status, response_time = self._adjust_thresholds()
            heal_type = "heal_adjust"
        
        self._log_healing_attempt(strategy, status, response_time)
        self.logger.log_action("healing_completed", status, 
                              strategy=strategy, 
                              response_time=response_time,
                              heal_type=heal_type)
        
        return status, response_time, heal_type, strategy

    def _retry_deployment(self):
        """Healing Action 1: Simply try deploying again."""
        return trigger_dashboard_deployment(should_fail=False)

    def _restore_previous_version(self, dataset_path):
        """Healing Action 2: Roll back by restoring the data from backup."""
        backup_path = f"{dataset_path}.bak"
        if os.path.exists(backup_path):
            try:
                shutil.copyfile(backup_path, dataset_path)
                print(f"  -> Successfully restored '{dataset_path}' from backup.")
                return trigger_dashboard_deployment(should_fail=False)
            except Exception as e:
                print(f"  -> Error while restoring backup: {e}")
                return "failure", 0
        else:
            print("  -> No backup file found. Cannot restore.")
            return "failure", 0

    def _adjust_thresholds(self):
        """Healing Action 3: Simulate adjusting a performance threshold."""
        return "success", 200

