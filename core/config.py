import os

from dotenv import load_dotenv

load_dotenv()


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def _get_bool(name: str, default: str = "true") -> bool:
    return os.getenv(name, default).lower() == "true"


AZURE_SUBSCRIPTION_ID = _require_env("AZURE_SUBSCRIPTION_ID")
DRY_RUN = _get_bool("DRY_RUN", "true")
CPU_LOOKBACK_MINUTES = int(os.getenv("CPU_LOOKBACK_MINUTES", "30"))
MIN_SAMPLE_COUNT = int(os.getenv("MIN_SAMPLE_COUNT", "10"))
PROTECTION_TAG_NAME = os.getenv("PROTECTION_TAG_NAME", "doNotShutdown")
PROTECTION_TAG_VALUE = os.getenv("PROTECTION_TAG_VALUE", "true").lower()
