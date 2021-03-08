from pathlib import Path
import os

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APP_DIR = ROOT_DIR.joinpath("parasut_cli")

env = {**os.environ}
