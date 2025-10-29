#!/usr/bin/env python3
"""Display learned Q-table and best strategies."""

import pandas as pd
import os

def show_qtable():
    """Show learned strategies from Q-table."""
    qtable_file = "logs/rl_log.csv"
    
    if not os.path.exists(qtable_file):
        print("❌ No Q-table found. Run: python train_rl.py")
        return
    
    try:
        qtable = pd.read_csv(qtable_file, index_col=0)
        print("🧠 Learned Q-Table:")
        print("=" * 50)
        print(qtable.round(3))
        
        print("\n🎯 Best Strategies:")
        print("=" * 30)
        for state in qtable.index:
            best_action = qtable.loc[state].idxmax()
            best_value = qtable.loc[state].max()
            print(f"{state}: {best_action} (Q={best_value:.3f})")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    show_qtable()