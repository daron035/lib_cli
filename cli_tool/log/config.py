from dataclasses import dataclass
from pathlib import Path


@dataclass
class LoggingConfig:
    level: str = "DEBUG"
    render_json_logs: bool = False
    path: Path | None = None
