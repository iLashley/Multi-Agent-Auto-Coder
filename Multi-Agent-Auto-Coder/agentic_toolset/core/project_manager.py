# core/project_manager.py

import os
from agentic_toolset.utils.display import display_console

class ProjectManager:
    def __init__(self, client, overseer, architect, code_reviewer, venv_manager, consultant=None, coder=None):
        from agentic_toolset.config import ORCHESTRATOR_MODEL, SUBAGENT_MODEL
        self.client = client
        self.orchestrator_model = ORCHESTRATOR_MODEL
        self.subagent_model = SUBAGENT_MODEL
        self.overseer = overseer
        self.architect = architect
        self.code_reviewer = code_reviewer
        self.venv_manager = venv_manager
        self.consultant = consultant
        self.coder = coder
        self.task_log = []
        self.project_files = []
        self.output_dir = None  # Set dynamically based on the project

    def manage_task(self, objective, file_content=None, dry_run=False):
        display_console(f"Managing task: {objective}", "ProjectManager Init", "blue")

        # 🔧 Suggest output folder name using LLM
        folder_name = self.suggest_project_name(objective)
        self.output_dir = os.path.join("Projects", folder_name)
        os.makedirs(self.output_dir, exist_ok=True)

        # 🏗 Create project file structure
        project_type = self.architect.create_project_structure(objective, self.output_dir)
        self.project_files = self.architect.create_architecture(objective, project_type, self.output_dir)

        # 🛠 Prepare environment
        self.venv_manager.create_venv()
        self.venv_manager.install_libraries(["rich", "ollama"])

        previous_results = []
        task_complete = False

        while not task_complete:
            display_console("Breaking down task with Orchestrator...", "ProjectManager", "blue")
            response_text, file_content = self.call_orchestrator(objective, file_content, previous_results)

            # 🧠 Run code review before deciding finalization
            review_summary = self.code_reviewer.review_code(response_text)
            if any(k in review_summary.lower() for k in ["looks good", "no issues", "well written"]):
                task_complete = True

            if task_complete or self.is_task_finalized(objective, response_text):
                display_console("Finalizing and writing script...", "ProjectManager", "green")
                self.write_to_project_files(response_text)

                if dry_run:
                    display_console("Dry run: skipping execution of generated code.", "Dry Run", "yellow")
                    return "Dry run completed. Code written but not executed."

                final_output = self.execute_project()
                self.venv_manager.cleanup()
                return final_output

            # 🔁 Continue to next sub-task
            sub_task_result = self.delegate_task(response_text)
            previous_results.append(sub_task_result)
            self.task_log.append({"task": response_text, "result": sub_task_result})
            display_console(f"Sub-task completed: {sub_task_result}", "Sub-task", "cyan")

    def suggest_project_name(self, objective):
        try:
            response = self.client.chat(
                model=self.orchestrator_model,
                messages=[{
                    "role": "user",
                    "content": (
                        f"Given the project objective:\n\n'{objective}'\n\n"
                        "Suggest a short folder-safe name (3-5 words, lowercase, underscores only). "
                        "Only return the name. No explanation or formatting."
                    )
                }]
            )
            return response['message']['content'].strip().replace(" ", "_")
        except Exception as e:
            display_console(f"Folder naming error: {e}. Defaulting to fallback folder.", "Error", "red")
            return "default_project"

    def is_task_finalized(self, objective, response_text):
        return "def " in response_text and ("__main__" in response_text or "print" in response_text)

    def delegate_task(self, task_prompt):
        if "architecture" in task_prompt:
            return self.architect.create_architecture(task_prompt, "multi-file", self.output_dir)
        elif "review code" in task_prompt:
            return self.code_reviewer.review_code(task_prompt)
        elif "consult" in task_prompt and self.consultant:
            return self.consultant.provide_advice(task_prompt)
        elif "bug fix" in task_prompt:
            return self.code_reviewer.fix_bugs(task_prompt)
        elif self.coder:
            return self.coder.generate_code(task_prompt)
        else:
            return self.call_sub_agent(task_prompt)
    def write_to_project_files(self, content):
        # 🧹 Strip Markdown code fences if present
        if content.strip().startswith("```"):
            content = "\n".join(
                line for line in content.strip().splitlines()
                if not line.strip().startswith("```")
            )
    
        main_file = os.path.join(self.output_dir, "src", "main.py")
        os.makedirs(os.path.dirname(main_file), exist_ok=True)
        with open(main_file, "w") as f:
            f.write(content)
        display_console(
            f"Code written to: {main_file}\n\nContent size: {len(content)} characters",
            "File Write", "green"
        )

    def execute_project(self):
        main_script_path = os.path.join(self.output_dir, "src", "main.py")
        try:
            stdout, stderr = self.venv_manager.run_script(main_script_path)

            if stderr:
                display_console(f"Execution failed. Attempting to fix via reviewer...", "Execution Error", "red")
                fixed_code = self.code_reviewer.fix_bugs(stderr)
                self.write_to_project_files(fixed_code)
                return self.execute_project()  # Retry after fix

            display_console(stdout, "Execution Output", "green")
            return stdout

        except Exception as e:
            display_console(f"Script execution raised an exception:\n{str(e)}", "Fatal Error", "red")
            return None

    def call_orchestrator(self, objective, file_content, previous_results):
        try:
            response = self.client.chat(
                model=self.orchestrator_model,
                messages=[{
                    "role": "user",
                    "content": (
                        f"Objective: {objective}\n"
                        f"Previous sub-task results: {previous_results}\n"
                        "Please break down the objective into the next sub-task, and create a prompt for a sub-agent."
                    )
                }]
            )
            response_text = response['message']['content']
            display_console(response_text, "Orchestrator Output", "green")
            return response_text, file_content
        except Exception as e:
            display_console(f"Orchestrator Error: {e}", "Error", "red")
            return None, file_content

    def call_sub_agent(self, prompt):
        try:
            display_console("Calling Sub-agent...", "Sub-agent", "yellow")
            response = self.client.chat(
                model=self.subagent_model,
                messages=[{"role": "user", "content": prompt}]
            )
            response_text = response['message']['content']
            display_console(response_text, "Sub-agent Result", "blue")
            return response_text
        except Exception as e:
            display_console(f"Sub-agent Error: {e}", "Error", "red")
            return None
