import json
import os

class CommandManager:
    def __init__(self, filename="saved_commands.json"):
        self.filename = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), filename)
        self.commands = []
        self.load_commands()

    def load_commands(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.commands = json.load(f)
            except Exception as e:
                print(f"Error loading commands: {e}")
                self.commands = []
        
        if not self.commands:
            # Default sample commands
            self.commands = [
                {"name": "Check Connection", "command": "AT", "is_hex": False},
                {"name": "Get Device Info", "command": "ATI", "is_hex": False},
                {"name": "Reset Device", "command": "ATZ", "is_hex": False}
            ]
            self.save_commands()

    def save_commands(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.commands, f, indent=4)
        except Exception as e:
            print(f"Error saving commands: {e}")

    def add_command(self, name, command, is_hex=False):
        self.commands.append({
            "name": name,
            "command": command,
            "is_hex": is_hex
        })
        self.save_commands()

    def update_command(self, index, name, command, is_hex=False):
        if 0 <= index < len(self.commands):
            self.commands[index] = {
                "name": name,
                "command": command,
                "is_hex": is_hex
            }
            self.save_commands()

    def delete_command(self, index):
        if 0 <= index < len(self.commands):
            self.commands.pop(index)
            self.save_commands()

    def get_commands(self):
        return self.commands
