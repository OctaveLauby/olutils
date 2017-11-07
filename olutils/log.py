"""Utils to manage logs.

Log Levels are:
    DEBUG   10
    INFO    20
    WARNING 30
    ERROR   40
    FATAL   50
"""
import logging
import os


class LogClass(object):
    """Class with logger included.

    Use log of instance with:
        self.log.debug(msg)
        self.log.info(msg)
        self.log.warning(msg)
        self.log.error(msg)
        self.log.fatal(msg)
    """

    def __init__(self, name, loglvl="INFO", logpath=None):
        """Create instance.

        Args:
            name    (str):          name of logger
            loglvl  (str of int):   log level
            logpath (str, opt):     path to logs, dft is stdout
        """
        self.log = create_logger(
            name=name,
            lvl=loglvl,
            path=logpath,
        )
        self.log.debug("Logger created")

    def get_loglvl(self, explicit=False):
        """Return loglvl.

        Args:
            explicit (bool): to get explicit log level (string) instead of int
        """
        lvl_int = self.log.level
        if not explicit:
            return lvl_int
        if lvl_int <= 10:
            return 'DEBUG'
        elif lvl_int <= 20:
            return 'INFO'
        elif lvl_int <= 30:
            return 'WARNING'
        elif lvl_int <= 40:
            return 'ERROR'
        return 'FATAL'

    def set_loglvl(self, lvl):
        """Set level of logs."""
        self.log.setLevel(lvl)
        self.log.debug("Log Level set to %s", lvl)

    def __del__(self):
        close_logger(self.log)
        return super().__del__()


# --------------------------------------------------------------------------- #
# Management of loggers

def clear_loggers():
    """Close all loggers."""
    for logger in logging.Logger.manager.loggerDict.values():
        close_logger(logger)


def close_logger(log):
    """Close logger."""
    for handler in log.handlers:
        handler.close()
        log.removeHandler(handler)


def create_logger(name, lvl="INFO", path=None, overwrite=False):
    """Create a logger.

    Args:
        name (str): name of logger
        lvl (str): level of log you want for logger
            can be any argument accepted by logging.Loger.setLevel
        path (str): path to logs messages in
            set it to None if you want logs and stdout
        overwrite (bool): overwrite logger with with same name if exists
    """
    if not name:
        raise ValueError(
            "'%s' is not a valid name for a logger"
        )
    logger = logging.getLogger(name)

    # Overwrite existant logger
    while logger.hasHandlers():
        if not overwrite:
            raise ValueError(
                "'%s' logger already exists"
                ", use overwrite argument to overwrite it"
                % name
            )
        logger.removeHandler(logger.handlers[0])

    # Build path if necessary
    if path:
        # Create log file container if necessary
        log_dir = os.path.dirname(path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

    # Create handlers of logger
    log_sh = (
        logging.FileHandler(path, encoding="utf-8")
        if path else logging.StreamHandler()
    )
    formatter = logging.Formatter(
        "%(asctime)s: [%(levelname)s] %(name)s - %(message)s"
    )
    log_sh.setFormatter(formatter)
    logger.setLevel(lvl)
    logger.addHandler(log_sh)

    return logger


def get_loggers():
    """Return all loggers."""
    return {
        name: logger
        for name, logger in logging.Logger.manager.loggerDict.items()
        if logger.hasHandlers()
    }
