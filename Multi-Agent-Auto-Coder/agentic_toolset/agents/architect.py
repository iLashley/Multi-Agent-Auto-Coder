# agents/architect.py

import os
from agentic_toolset.utils.display import display_console

class ArchitectAgent:
    def __init__(self):
        self.output_dir = None  # will be set dynamically per project

    def create_project_structure(self, objective, output_dir):
        """Determines and creates a project structure based on the objective."""
        self.output_dir = output_dir

        if any(k in objective for k in ["class", "utils", "configuration", "module"]):
            display_console("Detected complex project, creating multi-file structure.", "Architect", "cyan")
            os.makedirs(os.path.join(self.output_dir, "src"), exist_ok=True)
            os.makedirs(os.path.join(self.output_dir, "utils"), exist_ok=True)
            os.makedirs(os.path.join(self.output_dir, "config"), exist_ok=True)
            return "multi-file"

        else:
            display_console("Detected simple project, creating single-file structure.", "Architect", "cyan")
            os.makedirs(os.path.join(self.output_dir, "src"), exist_ok=True)
            return "single-file"

    def create_architecture(self, objective, project_type, output_dir):
        """Generates the appropriate project files based on the project type."""
        self.output_dir = output_dir
        files = []

        if project_type == "single-file":
            path = os.path.join(self.output_dir, "src", "main.py")
            files.append(self._create_file(path, "# Main script for project"))

        elif project_type == "multi-file":
            files += [
                self._create_file(os.path.join(self.output_dir, "src", "main.py"), "# Main script"),
                self._create_file(os.path.join(self.output_dir, "utils", "helpers.py"), "# Helper functions"),
                self._create_file(os.path.join(self.output_dir, "config", "settings.py"), "# Configuration settings")
            ]
            display_console("Multi-file project structure initialized.", "Architect", "cyan")

        return files

    def _create_file(self, path, content):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(content + "\n")
        display_console(f"Created file: {path}", "Architect", "green")
        return path
