# src/modules/pattern_manager.py
import os
import json
import logging

class PatternManager:
    def __init__(self, patterns_dir, selected_patterns_file):
        self.patterns_dir = patterns_dir
        self.selected_patterns_file = selected_patterns_file
        self.initial_patterns = [
            "analyze_claims",
            "analyze_debate",
            "analyze_incident",
            "create_summary",
            "explain_code",
            "extract_ideas",
            "extract_wisdom",
            "improve_writing",
            "summarize",
            "write_essay"
        ]
        self.selected_patterns = self.load_selected_patterns()

    def load_selected_patterns(self):
        if os.path.exists(self.selected_patterns_file):
            with open(self.selected_patterns_file, 'r') as f:
                patterns = json.load(f)
            return patterns if patterns else self.initial_patterns
        return self.initial_patterns

    def save_selected_patterns(self):
        with open(self.selected_patterns_file, 'w') as f:
            json.dump(self.selected_patterns, f)

    def get_all_patterns(self):
        return [d for d in os.listdir(self.patterns_dir) if os.path.isdir(os.path.join(self.patterns_dir, d))]

    def get_selected_patterns(self):
        return self.selected_patterns

    def add_pattern(self, pattern):
        if pattern not in self.selected_patterns and pattern in self.get_all_patterns():
            self.selected_patterns.append(pattern)
            self.save_selected_patterns()

    def remove_pattern(self, pattern):
        if pattern in self.selected_patterns:
            self.selected_patterns.remove(pattern)
            self.save_selected_patterns()

    def edit_pattern_list(self):
        while True:
            print("\nCurrent selected patterns:")
            for i, pattern in enumerate(self.selected_patterns, 1):
                print(f"{i}. {pattern}")
            
            print("\nAvailable patterns:")
            all_patterns = self.get_all_patterns()
            for pattern in all_patterns:
                if pattern not in self.selected_patterns:
                    print(f"- {pattern}")
            
            action = input("\nEnter 'add <pattern>', 'remove <number>', or 'done': ").strip().lower()
            
            if action == 'done':
                break
            elif action.startswith('add '):
                pattern = action[4:].strip()
                self.add_pattern(pattern)
            elif action.startswith('remove '):
                try:
                    index = int(action[7:].strip()) - 1
                    if 0 <= index < len(self.selected_patterns):
                        removed_pattern = self.selected_patterns[index]
                        self.remove_pattern(removed_pattern)
                    else:
                        print("Invalid pattern number.")
                except ValueError:
                    print("Invalid input. Please enter a number after 'remove'.")
            else:
                print("Invalid action. Please try again.")

        self.save_selected_patterns()

    def load_system_content(self, pattern_name):
        pattern_dir = os.path.join(self.patterns_dir, pattern_name)
        system_file = os.path.join(pattern_dir, 'system.md')
        if os.path.exists(system_file):
            with open(system_file, 'r') as f:
                return f.read()
        else:
            logging.error(f"system.md not found for pattern {pattern_name}")
            return f"Error: system.md not found for pattern {pattern_name}"
