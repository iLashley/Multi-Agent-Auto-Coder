# main.py

import argparse
from agentic_toolset.config import OLLAMA_HOST
from agentic_toolset.core.venv_manager import VenvManagerAgent
from agentic_toolset.core.project_manager import ProjectManager
from agentic_toolset.agents.overseer import OverseerAgent
from agentic_toolset.agents.architect import ArchitectAgent
from agentic_toolset.agents.reviewer import CodeReviewerAgent
from agentic_toolset.agents.consultant import ConsultantAgent
from agentic_toolset.agents.coder import CoderAgent
from agentic_toolset.utils.display import display_console

from ollama import Client


def parse_args():
    parser = argparse.ArgumentParser(description="🧠 Agentic AI Code Tool")
    parser.add_argument(
        "--objective",
        type=str,
        help="Describe the coding task or project objective.",
    )
    parser.add_argument(
        "--no-cleanup",
        action="store_true",
        help="Do not remove the virtual environment after execution.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't execute generated code; just display it.",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    client = Client(host=OLLAMA_HOST)
    venv_manager = VenvManagerAgent()

    overseer = OverseerAgent(client)
    architect = ArchitectAgent()
    reviewer = CodeReviewerAgent(client)
    consultant = ConsultantAgent(client)
    coder = CoderAgent(client)

    project_manager = ProjectManager(
        client=client,
        overseer=overseer,
        architect=architect,
        code_reviewer=reviewer,
        venv_manager=venv_manager,
        consultant=consultant,
        coder=coder
    )

    # 🔽 Objective input
    objective = args.objective or input("🧠 What is your project goal or coding task? > ").strip()

    if not objective:
        print("⚠️ No objective provided. Exiting.")
        return

    # 🔽 Run the project workflow
    try:
        final_output = project_manager.manage_task(objective, dry_run=args.dry_run)

        if args.dry_run:
            display_console("Dry run mode enabled. Code generated, not executed.", "Dry Run", "yellow")
        else:
            display_console(f"\nFinal Output:\n{final_output}", "Execution Result", "green")

        if args.no_cleanup:
            display_console("Skipping venv cleanup (--no-cleanup set).", "Cleanup", "yellow")
        else:
            venv_manager.cleanup()

    except Exception as e:
        display_console(f"An error occurred:\n{str(e)}", "Fatal Error", "red")


if __name__ == "__main__":
    main()
