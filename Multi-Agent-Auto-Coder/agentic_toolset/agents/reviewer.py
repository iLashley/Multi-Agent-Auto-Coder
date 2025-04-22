# agents/reviewer.py

from agentic_toolset.utils.display import display_console
from agentic_toolset.config import REFINER_MODEL, BUGFIXER_MODEL

class CodeReviewerAgent:
    def __init__(self, client):
        self.client = client
        self.reviewer_model = REFINER_MODEL
        self.bugfixer_model = BUGFIXER_MODEL

    def review_code(self, code):
        prompt = f"""You are a senior code reviewer. Analyze the following Python code for correctness, quality, and bugs. Respond with a short summary of any issues or confirm it looks good.

# --- CODE START ---
{code}
# --- CODE END ---
"""
        try:
            response = self.client.chat(
                model=self.reviewer_model,
                messages=[{"role": "user", "content": prompt}]
            )
            response_text = response['message']['content']
            display_console(response_text, "Code Review Result", "magenta")
            return response_text
        except Exception as e:
            display_console(f"Error in Code Review: {e}", "Error", "red")
            return "Code review encountered an error."

    def fix_bugs(self, code):
        prompt = f"""You are a Python bug fixer. Analyze and fix any issues in this code. Return only the corrected code.

# --- CODE START ---
{code}
# --- CODE END ---
"""
        try:
            response = self.client.chat(
                model=self.bugfixer_model,
                messages=[{"role": "user", "content": prompt}]
            )
            response_text = response['message']['content']
            display_console(response_text, "Fixed Code Output", "red")
            return response_text
        except Exception as e:
            display_console(f"Error in Code Fixing: {e}", "Error", "red")
            return "Bug fixing encountered an error."

    def fix_from_error_log(self, code, stderr):
        prompt = f"""You are a Python bug fixer. The following Python script fails to run due to the error shown below. Fix the code so it executes correctly.

# --- ORIGINAL CODE ---
{code}

# --- ERROR OUTPUT ---
{stderr}

# --- END ---
Return only the fixed code, no explanation.
"""
        try:
            response = self.client.chat(
                model=self.bugfixer_model,
                messages=[{"role": "user", "content": prompt}]
            )
            response_text = response['message']['content']
            display_console(response_text, "Fixed from Error Log", "red")
            return response_text
        except Exception as e:
            display_console(f"Error in Traceback-Based Fixing: {e}", "Error", "red")
            return "Bug fix from traceback failed."
