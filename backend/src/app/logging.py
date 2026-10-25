import logging
import sys
from collections.abc import MutableMapping
from typing import Any

import structlog

_SENSITIVE = ("password", "token")


def mask_secrets(
    _logger: Any,
    _method: str,
    event_dict: MutableMapping[str, Any],
) -> MutableMapping[str, Any]:
    """Safeguard to hide the values of fields with "secret" names."""
    for key in event_dict:
        if any(s in key.lower() for s in _SENSITIVE):
            event_dict[key] = "******"
    return event_dict


def setup_logging(*, json_logs: bool = False, level: int = logging.INFO) -> None:
    shared: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        mask_secrets,
    ]

    structlog.configure(
        processors=[*shared, structlog.stdlib.ProcessorFormatter.wrap_for_formatter],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    final: list[structlog.types.Processor] = [
        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
    ]
    if json_logs:
        final += [structlog.processors.format_exc_info, structlog.processors.JSONRenderer()]
    else:
        final += [structlog.dev.set_exc_info, structlog.dev.ConsoleRenderer()]

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(foreign_pre_chain=shared, processors=final)
    )

    root = logging.getLogger()
    root.handlers[:] = [handler]
    root.setLevel(level)

    logging.getLogger("httpx").setLevel(logging.WARNING)
