import pandas as pd
import random
import os
import csv
import datetime

class RLOptimizer:
    """Lightweight Q-learning agent for healing strategy optimization."""
    
    def __init__(self, q_table_file, performance_log_file):
        self.q_table_file = q_table_file
        self.performance_log_file = performance_log_file
        self.states = ["deployment_failure", "latency_issue", "anomaly_score", "anomaly_health"]
        self.actions = ["retry_deployment", "restore_previous_version", "adjust_thresholds"]
        self.alpha = 0.1  # Learning rate
        self.epsilon = 0.2  # Exploration rate
        self.q_table = self._load_q_table()
        self._init_performance_log()
        print("Initialized RL Optimizer Agent.")

    def _init_performance_log(self):
        """Initialize performance log file."""
        os.makedirs(os.path.dirname(self.performance_log_file), exist_ok=True)
        if not os.path.exists(self.performance_log_file):
            with open(self.performance_log_file, 'w', newline='') as f:
                csv.writer(f).writerow(["timestamp", "state", "action", "reward"])

    def _load_q_table(self):
        """Load or create Q-table."""
        os.makedirs(os.path.dirname(self.q_table_file), exist_ok=True)
        try:
            qt = pd.read_csv(self.q_table_file, index_col=0)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            qt = pd.DataFrame(index=self.states, columns=self.actions, data=0.0)
        
        # Ensure all states and actions exist
        for state in self.states:
            if state not in qt.index:
                qt.loc[state] = 0.0
        for action in self.actions:
            if action not in qt.columns:
                qt[action] = 0.0
        
        return qt.fillna(0.0)

    def choose_action(self, state):
        """Choose action using epsilon-greedy policy."""
        if state not in self.q_table.index:
            self.q_table.loc[state] = 0.0
        
        if random.random() < self.epsilon:
            action = random.choice(self.actions)
            print(f"RL Optimizer: Exploring -> {action}")
        else:
            action = self.q_table.loc[state].idxmax()
            print(f"RL Optimizer: Exploiting best -> {action}")
        
        return action

    def learn(self, state, action, reward):
        """Update Q-table based on reward."""
        if state not in self.q_table.index:
            self.q_table.loc[state] = 0.0
        
        old_value = self.q_table.loc[state, action]
        new_value = old_value + self.alpha * (reward - old_value)
        self.q_table.loc[state, action] = new_value
        
        # Log performance
        timestamp = datetime.datetime.now().isoformat()
        with open(self.performance_log_file, 'a', newline='') as f:
            csv.writer(f).writerow([timestamp, state, action, reward])
        
        print(f"RL Update: {state}/{action}: {old_value:.3f} -> {new_value:.3f}")
        
        # Show best action for this state
        best_action = self.q_table.loc[state].idxmax()
        best_value = self.q_table.loc[state].max()
        print(f"Best strategy for {state}: {best_action} (Q={best_value:.3f})")

    def save_q_table(self):
        """Save Q-table to file."""
        self.q_table.to_csv(self.q_table_file)
        print(f"Q-table saved to {self.q_table_file}")