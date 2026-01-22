import json
import os
import shutil

class CommandManager:
    def __init__(self, filename="saved_commands.json"):
        # Use user's home directory for persistent storage
        # This ensures data is NOT lost during package upgrades
        self.app_data_dir = os.path.join(os.path.expanduser("~"), ".sparkserial")
        
        # Create the directory if it doesn't exist
        if not os.path.exists(self.app_data_dir):
            os.makedirs(self.app_data_dir)
        
        # Default location
        default_location = os.path.join(self.app_data_dir, filename)
        
        # Check if user has set a custom location in config
        config_file = os.path.join(self.app_data_dir, "config.json")
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    custom_path = config.get('commands_file')
                    if custom_path and os.path.exists(custom_path):
                        self.filename = custom_path
                        print(f"Using custom commands location: {custom_path}")
                    else:
                        self.filename = default_location
            except Exception:
                self.filename = default_location
        else:
            self.filename = default_location
        
        # Migration: Check if old file exists in package directory and migrate
        old_location = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), filename)
        if os.path.exists(old_location) and not os.path.exists(self.filename):
            try:
                shutil.copy2(old_location, self.filename)
                print(f"Migrated saved commands from {old_location} to {self.filename}")
            except Exception as e:
                print(f"Migration failed: {e}")
        
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

    def bulk_replace(self, find_text, replace_text):
        """
        Replaces occurrences of find_text with replace_text in all command strings.
        Returns the number of commands modified.
        """
        count = 0
        if not find_text:
            return 0
            
        for cmd in self.commands:
            if find_text in cmd['command']:
                cmd['command'] = cmd['command'].replace(find_text, replace_text)
                count += 1
        
        if count > 0:
            self.save_commands()
        return count
