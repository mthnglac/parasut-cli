from pathlib import Path
from dotenv import dotenv_values

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APP_DIR = ROOT_DIR.joinpath("parasut_cli")

env = {
    **dotenv_values(f"{ROOT_DIR}/.envs/.env.shared"),
    **dotenv_values(f"{ROOT_DIR}/.envs/.env.secret"),
}
