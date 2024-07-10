# src/modules/pattern_manager.py
import os
import json
import logging

class PatternManager:
    def __init__(self, patterns_dir, selected_patterns_file):
        self.patterns_dir = patterns_dir
        self.selected_patterns_file = selected_patterns_file
        self.selected_pattern = "simple"  # Default pattern

    def get_all_patterns(self):
        return [d for d in os.listdir(self.patterns_dir) if os.path.isdir(os.path.join(self.patterns_dir, d))]

    def select_pattern(self, pattern):
        if pattern in self.get_all_patterns():
            self.selected_pattern = pattern

    def get_selected_pattern(self):
        return self.selected_pattern

    def load_system_content(self, pattern_name):
        pattern_dir = os.path.join(self.patterns_dir, pattern_name)
        system_file = os.path.join(pattern_dir, 'system.md')
        if os.path.exists(system_file):
            with open(system_file, 'r') as f:
                return f.read()
        else:
            logging.error(f"system.md not found for pattern {pattern_name}")
            return f"Error: system.md not found for pattern {pattern_name}"
