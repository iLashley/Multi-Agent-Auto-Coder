# agents/coder.py

from agentic_toolset.utils.display import display_console
from agentic_toolset.config import CODER_MODEL

class CoderAgent:
    def __init__(self, client):
        self.client = client
        self.coder_model = CODER_MODEL
        self.coder_log = []

    def generate_code(self, prompt):
        try:
            response = self.client.chat(
                model=self.coder_model,
                messages=[{"role": "user", "content": prompt}]
            )
            response_text = response['message']['content']
            self.coder_log.append({"prompt": prompt, "response": response_text})
            display_console(response_text, "Generated Code", "cyan")
            return response_text
        except Exception as e:
            display_console(f"Error in Code Generation call: {e}", "Error", "red")
            return "Code generation encountered an error."
