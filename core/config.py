import os

from dotenv import load_dotenv

load_dotenv()


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


AZURE_SUBSCRIPTION_ID = _require_env("AZURE_SUBSCRIPTION_ID")
DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"
CPU_LOOKBACK_MINUTES = int(os.getenv("CPU_LOOKBACK_MINUTES", "30"))
