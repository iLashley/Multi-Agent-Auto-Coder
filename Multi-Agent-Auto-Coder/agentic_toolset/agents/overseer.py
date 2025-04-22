# agents/overseer.py

from agentic_toolset.utils.display import display_console

class OverseerAgent:
    def __init__(self, client):
        self.client = client
        self.log = []

    def review_final_result(self, result):
        self.log.append({"final_result": result})
        display_console("Overseer has reviewed the final result.", "Overseer Review", "green")

    def compile_project(self, refined_task):
        display_console("Overseer is compiling the project...", "Overseer Compilation", "blue")
        return f"# Final compiled project output\n{refined_task}"
