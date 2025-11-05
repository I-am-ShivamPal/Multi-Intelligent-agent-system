import pandas as pd
import random
import os
import csv
import datetime
from core.sovereign_bus import bus

class RLTrainer:
    """Q-learning trainer that learns optimal strategies across multiple runs."""
    def __init__(self, rl_log_file, performance_log_file, train_mode=False):
        self.q_table_file = rl_log_file
        self.performance_log_file = performance_log_file
        self.train_mode = train_mode
        self.states = ["deployment_failure", "latency_issue", "anomaly_score", "anomaly_health"]
        self.actions = ["retry_deployment", "restore_previous_version", "adjust_thresholds"]
        self.alpha = 0.1
        self.epsilon = 0.2 if train_mode else 0.1
        self.q_table = self._load_q_table()
        self._initialize_performance_log()
        print("Initialized RL Trainer.")

    def _initialize_performance_log(self):
        """Creates the performance log file with a header if it doesn't exist."""
        os.makedirs(os.path.dirname(self.performance_log_file), exist_ok=True)
        if not os.path.exists(self.performance_log_file):
            with open(self.performance_log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "state", "action", "reward"])

    def _log_performance(self, state, action, reward):
        """Logs a single state, action, and reward tuple to the performance log."""
        timestamp = pd.Timestamp.now().isoformat()
        with open(self.performance_log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, state, action, reward])

    def _load_q_table(self):
        """Loads the Q-table, creating it if it doesn't exist."""
        os.makedirs(os.path.dirname(self.q_table_file), exist_ok=True)
        try:
            qt = pd.read_csv(self.q_table_file, index_col=0)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            qt = pd.DataFrame(index=self.states, columns=self.actions, data=0.0)
            return qt
        
        # Ensure all states and actions exist
        for a in self.actions:
            if a not in qt.columns: qt[a] = 0.0
        for s in self.states:
            if s not in qt.index: qt.loc[s] = 0.0
        
        return qt.loc[self.states, self.actions].fillna(0.0).astype(float)

    def save_q_table(self):
        """Saves the current Q-table to the log file."""
        self.q_table.to_csv(self.q_table_file)
        print(f"Q-table saved to {self.q_table_file}")

    def choose_action(self, state):
        """Chooses an action based on the current policy."""
        if state not in self.q_table.index:
            self.q_table.loc[state] = 0.0
        
        if self.train_mode:
            untrained = self.q_table.loc[state][self.q_table.loc[state] == 0].index.tolist()
            if untrained:
                action = random.choice(untrained)
                print(f"Training: Trying untrained action '{action}'")
                return action
        
        if random.uniform(0, 1) < self.epsilon:
            action = random.choice(self.actions)
            print(f"RL: Exploring -> {action}")
        else:
            action = self.q_table.loc[state].idxmax()
            print(f"RL: Best strategy -> {action}")
        
        # Publish to bus
        q_value = self.q_table.loc[state, action]
        bus.publish("rl.action_chosen", {
            "state": state,
            "action": action,
            "q_value": float(q_value)
        })
        return action
    
    def _show_best_strategy(self, state):
        """Show current best strategy for the state."""
        best_action = self.q_table.loc[state].idxmax()
        best_value = self.q_table.loc[state].max()
        print(f"Best for {state}: {best_action} (Q={best_value:.3f})")
    
    def show_learning_progress(self):
        """Display learned strategies for all states."""
        print("\n=== LEARNED STRATEGIES ===")
        for state in self.states:
            if state in self.q_table.index:
                best_action = self.q_table.loc[state].idxmax()
                best_value = self.q_table.loc[state].max()
                print(f"{state}: {best_action} (Q={best_value:.3f})")
        print("========================\n")

    def learn(self, state, action, base_reward, user_feedback=None):
        """Updates Q-table and tracks learning progress."""
        final_reward = base_reward
        if user_feedback == 'accepted':
            final_reward += 1
        elif user_feedback == 'rejected':
            final_reward = -1
        
        self._log_performance(state, action, final_reward)
        
        old_value = self.q_table.loc[state, action]
        new_value = old_value + self.alpha * (final_reward - old_value)
        self.q_table.loc[state, action] = new_value
        
        print(f"RL Update: {state}/{action}: {old_value:.3f} -> {new_value:.3f}")
        self._show_best_strategy(state)
        
        # Publish to bus
        bus.publish("rl.learned", {
            "state": state,
            "action": action,
            "reward": final_reward,
            "new_q": float(new_value)
        })

