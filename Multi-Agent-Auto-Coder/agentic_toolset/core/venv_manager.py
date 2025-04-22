# core/venv_manager.py

import os
import subprocess
import shutil
import ensurepip
from agentic_toolset.utils.display import display_console

class VenvManagerAgent:
    def __init__(self):
        self.venv_path = "project_venv"
        self.python_executable = self._find_python_executable()
        self.pip_command = [self.python_executable, "-m", "pip"]
        display_console(f"Initialized VenvManager with python executable: {self.python_executable}", "Venv Init", "blue")

    def _find_python_executable(self):
        unix_path = os.path.join(self.venv_path, "bin", "python")
        windows_path = os.path.join(self.venv_path, "Scripts", "python")
        if os.path.exists(unix_path):
            return unix_path
        elif os.path.exists(windows_path):
            return windows_path
        else:
            return "python"  # fallback if venv doesn't exist yet

    def create_venv(self):
        if not os.path.exists(self.venv_path):
            display_console("Creating virtual environment...", "VenvManager", "yellow")
            python_cmd = shutil.which("python3") or shutil.which("python") or "python"
            result = subprocess.run([python_cmd, "-m", "venv", self.venv_path])
            if result.returncode != 0:
                raise EnvironmentError("Failed to create virtual environment.")

        if not self._check_pip():
            display_console("Installing pip via ensurepip.", "VenvManager", "yellow")
            result = subprocess.run([self.python_executable, "-m", "ensurepip", "--upgrade"])
            if result.returncode != 0:
                raise EnvironmentError("Failed to install pip.")

    def _check_pip(self):
        try:
            subprocess.run(self.pip_command + ["--version"], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def install_libraries(self, libraries):
        for lib in libraries:
            if not self._is_library_installed(lib):
                display_console(f"Installing library: {lib}", "VenvManager", "yellow")
                result = subprocess.run(self.pip_command + ["install", lib], capture_output=True, text=True)
                if result.returncode == 0:
                    display_console(f"Installed: {lib}", "VenvManager", "green")
                else:
                    display_console(f"Error installing {lib}: {result.stderr}", "VenvManager", "red")
                    raise EnvironmentError(f"Failed to install {lib}: {result.stderr}")

    def _is_library_installed(self, library):
        result = subprocess.run([self.python_executable, "-c", f"import {library}"], capture_output=True, text=True)
        return result.returncode == 0

    def run_script(self, script_path):
        display_console(f"Running script: {script_path}", "VenvManager", "cyan")
        result = subprocess.run(
            [self.python_executable, script_path],
            capture_output=True,
            text=True
        )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        if stdout:
            display_console(stdout, "Script Output", "green")
        if stderr:
            display_console(stderr, "Script Error", "red")

        return stdout, stderr

    def cleanup(self):
        if os.path.exists(self.venv_path):
            display_console("Cleaning up virtual environment...", "VenvManager", "red")
            shutil.rmtree(self.venv_path, ignore_errors=True)
