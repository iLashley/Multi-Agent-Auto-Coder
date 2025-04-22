# agents/consultant.py

from agentic_toolset.utils.display import display_console
from agentic_toolset.config import CONSULTANT_MODEL

class ConsultantAgent:
    def __init__(self, client):
        self.client = client
        self.consultant_model = CONSULTANT_MODEL
        self.consultant_log = []

    def provide_advice(self, prompt):
        try:
            response = self.client.chat(
                model=self.consultant_model,
                messages=[{"role": "user", "content": prompt}]
            )
            response_text = response['message']['content']
            self.consultant_log.append({"prompt": prompt, "response": response_text})
            display_console(response_text, "Consultant Advice", "green")
            return response_text
        except Exception as e:
            display_console(f"Error in Consultant call: {e}", "Error", "red")
            return "Consultant encountered an error."
