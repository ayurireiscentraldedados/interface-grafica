from __future__ import annotations

import os
from pathlib import Path


def db_path() -> Path:
    return Path(os.getenv("ROAD_SAFETY_DB_PATH", "data/ceara_road_safety_api.duckdb"))


def access_log_path() -> Path:
    return Path(os.getenv("ACCESS_LOG_PATH", "logs/access.csv"))
