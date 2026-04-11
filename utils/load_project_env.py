from pathlib import Path
from dotenv import load_dotenv


def load_project_env(env_name: str = ".env"):
    """
    Recursively searches for the .env file starting from the caller's directory
    and moving upwards. Once found, it loads it into the environment.
    """
    # Start looking from the directory of the script that called this function
    current_dir = Path.cwd()

    # Climb up until we find the .env file
    while current_dir != current_dir.parent:
        env_path = current_dir / env_name
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
            return env_path
        current_dir = current_dir.parent

    return None
