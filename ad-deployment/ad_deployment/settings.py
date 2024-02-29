import os
from pathlib import Path
from typing import Union

from dotenv import load_dotenv

def find_project_root(start_path: Path = Path(__file__)) -> Path:
    """
    Traverse upwards from the start_path until a directory with the .env.default file is found.
    """
    current_dir = start_path.resolve()
    while not (current_dir / '.env.default').exists():
        if current_dir.parent == current_dir:
            raise FileNotFoundError("Couldn't find the .env.default file in any parent directories.")
        current_dir = current_dir.parent
    return current_dir


def load_env_vars(root_dir: Union[str, Path]) -> dict:
    """Load environment variables from .env.default and .env files.

    Args:
    ----
        root_dir: Root directory of the .env files.

    Returns:
    -------
        Dictionary with the environment variables.

    """
    if isinstance(root_dir, str):
        root_dir = Path(root_dir)

    print(f"Loading .env.default from: {root_dir / '.env.default'}")
    print(f"Loading .env from: {root_dir / '.env'}")
    load_dotenv(dotenv_path=root_dir / ".env.default")
    load_dotenv(dotenv_path=root_dir / ".env", override=True)

    return dict(os.environ)

AZURE_DEPLOYMENT_ROOT_DIR = find_project_root()

SETTINGS = load_env_vars(root_dir=AZURE_DEPLOYMENT_ROOT_DIR)
print(SETTINGS["DATABRICKS_DOMAIN"])