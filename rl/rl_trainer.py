# import pandas as pd
# import random
# import os
# import csv
# import datetime
# import shutil
# from utils import trigger_dashboard_deployment


# class RLTrainer:
#     """Uses a Q-learning table to choose the best healing strategy and learn from user feedback."""

#     def __init__(self, healing_log_file, rl_log_file, feedback_file, train_mode=False):
#         self.healing_log_file = healing_log_file
#         self.q_table_file = rl_log_file
#         self.feedback_file = feedback_file
#         self.train_mode = train_mode

#         # RL core parameters
#         self.states = ["deployment_failure", "latency_issue", "anomaly_score", "anomaly_health"]
#         self.actions = ["retry_deployment", "restore_previous_version", "adjust_thresholds"]
#         self.alpha = 0.1     # Learning rate
#         self.gamma = 0.9     # Discount factor
#         self.epsilon = 0.1   # Exploration rate

#         self._initialize_logs()
#         self.q_table = self._load_q_table()
#         print("✅ Initialized RL Optimizer Agent.")

#     # -------------------------------------------------------
#     # --- Initialization & Logging Utilities ---
#     # -------------------------------------------------------
#     def _initialize_logs(self):
#         """Creates log files with headers if they don't exist."""
#         for f in [self.healing_log_file, self.feedback_file]:
#             os.makedirs(os.path.dirname(f), exist_ok=True)
#             if not os.path.exists(f):
#                 with open(f, mode='w', newline='') as file:
#                     writer = csv.writer(file)
#                     if "healing" in f:
#                         writer.writerow(["timestamp", "strategy", "status", "response_time_ms"])
#                     elif "feedback" in f:
#                         writer.writerow(["timestamp", "state", "action", "outcome", "feedback"])

#     def _log_healing_attempt(self, strategy, status, response_time):
#         """Logs the outcome of a single healing attempt."""
#         timestamp = datetime.datetime.now().isoformat()
#         with open(self.healing_log_file, mode='a', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow([timestamp, strategy, status, round(response_time, 2)])

#     def log_performance(self, state, action, reward):
#         """Logs RL performance statistics."""
#         perf_path = self.q_table_file.replace(".csv", "_performance.csv")
#         os.makedirs(os.path.dirname(perf_path), exist_ok=True)
#         with open(perf_path, 'a', newline='') as file:
#             writer = csv.writer(file)
#             if file.tell() == 0:
#                 writer.writerow(["timestamp", "state", "action", "reward"])
#             writer.writerow([datetime.datetime.now().isoformat(), state, action, reward])

#     # -------------------------------------------------------
#     # --- Q-Table Handling ---
#     # -------------------------------------------------------
#     def _load_q_table(self):
#         """Loads or initializes the Q-table."""
#         os.makedirs(os.path.dirname(self.q_table_file), exist_ok=True)
#         try:
#             qt = pd.read_csv(self.q_table_file, index_col=0)
#         except (FileNotFoundError, pd.errors.EmptyDataError):
#             qt = pd.DataFrame()

#         for a in self.actions:
#             if a not in qt.columns:
#                 qt[a] = 0.0
#         for s in self.states:
#             if s not in qt.index:
#                 qt.loc[s] = 0.0

#         return qt.loc[self.states, self.actions].fillna(0.0).astype(float)

#     def save_q_table(self):
#         """Saves the Q-table."""
#         self.q_table.to_csv(self.q_table_file)
#         print(f"💾 Saved Q-table to {self.q_table_file}")

#     # -------------------------------------------------------
#     # --- RL Core Logic ---
#     # -------------------------------------------------------
#     def update_q_table(self, state, action, reward, next_state=None):
#         """Core Q-learning update rule with reward propagation."""
#         if state not in self.q_table.index:
#             self.q_table.loc[state] = 0.0

#         old_value = self.q_table.loc[state, action]
#         next_max = 0
#         if next_state and next_state in self.q_table.index:
#             next_max = self.q_table.loc[next_state].max()

#         new_value = old_value + self.alpha * (reward + self.gamma * next_max - old_value)
#         self.q_table.loc[state, action] = new_value
#         self.log_performance(state, action, reward)

#         print(f"RL Update → ({state}, {action}): {old_value:.3f} → {new_value:.3f}")

#     def choose_action(self, state):
#         """Selects an action using epsilon-greedy policy."""
#         if state not in self.q_table.index:
#             self.q_table.loc[state] = 0.0

#         if self.train_mode:
#             # Prefer untried actions during training
#             untrained_actions = self.q_table.loc[state][self.q_table.loc[state] == 0].index.tolist()
#             if untrained_actions:
#                 action = random.choice(untrained_actions)
#                 print(f"🧠 Training: trying new action '{action}' for state '{state}'")
#                 return action
#             else:
#                 action = random.choice(self.actions)
#                 print(f"🧠 Training: all tried, exploring randomly → {action}")
#                 return action

#         if random.uniform(0, 1) < self.epsilon:
#             action = random.choice(self.actions)
#             print(f"RL Policy: Exploring → {action}")
#         else:
#             action = self.q_table.loc[state].idxmax()
#             print(f"RL Policy: Exploiting → {action}")
#         return action

#     def _apply_user_feedback(self):
#         """Checks and applies latest user feedback."""
#         if not os.path.exists(self.feedback_file) or os.path.getsize(self.feedback_file) == 0:
#             return

#         # try:
#         #     feedback_df = pd.read_csv(self.feedback_file)
#         # except pd.errors.EmptyDataError:
#         #     return
#         # if feedback_df.empty or len(feedback_df) <= 1:
        

#         if not os.path.exists(self.feedback_file):
#             print(f"⚠️ No feedback file found at {self.feedback_file} — skipping user feedback adjustment.")
#             return

#         try:
#             feedback_df = pd.read_csv(self.feedback_file, on_bad_lines='skip')
#             if feedback_df.empty:
#                 print("⚠️ Feedback file is empty — no feedback applied.")
#                 return
#         except Exception as e:
#             print(f"⚠️ Could not read feedback file: {e}")
#             return


#         last_feedback = feedback_df.iloc[-1]
#         state, action, outcome, feedback = (
#             last_feedback['state'],
#             last_feedback['action'],
#             last_feedback['outcome'],
#             last_feedback['feedback'],
#         )

#         # Reward mapping
#         if feedback == 'agreed':
#             reward = 2
#         elif feedback == 'rejected':
#             reward = -1
#         elif outcome == 'success':
#             reward = 1
#         else:
#             reward = -1

#         print(f"📥 Applying feedback: {state} / {action} → reward {reward}")
#         self.update_q_table(state, action, reward)
#         self.save_q_table()

#         # Clear feedback file
#         with open(self.feedback_file, 'w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow(["timestamp", "state", "action", "outcome", "feedback"])

#     # -------------------------------------------------------
#     # --- Healing Execution ---
#     # -------------------------------------------------------
#     def attempt_healing(self, state, dataset_path):
#         """Chooses and executes a healing strategy."""
#         self._apply_user_feedback()
#         action = self.choose_action(state)

#         print(f"\n🚑 Healing Initiated: {state} → {action}")
#         status, response_time, heal_type = "failure", 0, "unknown_strategy"

#         if action == 'retry_deployment':
#             status, response_time = trigger_dashboard_deployment(should_fail=False)
#             heal_type = "heal_retry"

#         elif action == 'restore_previous_version':
#             backup_path = f"{dataset_path}.bak"
#             if os.path.exists(backup_path):
#                 shutil.copyfile(backup_path, dataset_path)
#                 status, response_time = trigger_dashboard_deployment(should_fail=False)
#             heal_type = "heal_restore"

#         elif action == 'adjust_thresholds':
#             status, response_time = "success", 200
#             heal_type = "heal_adjust"

#         # Log and learn immediately
#         self._log_healing_attempt(action, status, response_time)
#         reward = 1 if status == "success" else -1
#         self.update_q_table(state, action, reward)
#         self.save_q_table()

#         return status, response_time, heal_type, action














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

