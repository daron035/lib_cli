from dataclasses import dataclass, field

from .log import LoggingConfig


@dataclass
class Config:
    logging: LoggingConfig = field(default_factory=LoggingConfig)
