import functools
import logging


def optimize_log(log):
    logger: logging.Logger = log.__self__

    def get_level(level) -> int:
        if log is logger.log and isinstance(level, int):
            return level

        match log:
            case logger.debug:
                level = logging.DEBUG
            case logger.info:
                level = logging.INFO
            case logger.warning:
                level = logging.WARNING
            case logger.error:
                level = logging.ERROR
            case logger.critical:
                level = logging.CRITICAL
            case _:
                raise ValueError

        return level

    @functools.wraps(log)
    def optimize(*args, **kwargs):
        if logger.isEnabledFor(get_level(args[0])):
            log(*args, **kwargs)

    return optimize
