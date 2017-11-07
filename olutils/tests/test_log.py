import os
import pytest
import shutil

from olutils import log

# --------------------------------------------------------------------------- #
# Parameters

TMP_DIR = "tmp"
EXPECTED_LOGS = [
    "[DEBUG] {} - debug",
    "[INFO] {} - info",
    "[WARNING] {} - warning",
    "[ERROR] {} - error",
    "[CRITICAL] {} - fatal",
]


def log_levels(logger):
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.fatal("fatal")


# --------------------------------------------------------------------------- #
# Setup / Teardown

def setup_function(function):
    if os.path.exists(TMP_DIR):
        shutil.rmtree("tmp")


def teardown_function(function):
    if os.path.exists(TMP_DIR):
        shutil.rmtree("tmp")


# --------------------------------------------------------------------------- #
# Tests

def test_create_logger():
    path1 = os.path.join(TMP_DIR, "1.log")
    path2 = os.path.join(TMP_DIR, "2.log")

    log1 = log.create_logger("LogOne", lvl="DEBUG", path=path1)
    log2 = log.create_logger("LogTwo", path=path2)  # default lvl = INFO
    log3 = log.create_logger("LogThree", lvl="ERROR", path=path2)

    log_levels(log1)
    log_levels(log2)
    log_levels(log3)

    log.close_logger(log1)
    log.close_logger(log2)
    log.close_logger(log3)

    with open(path1) as file1:
        lines = file1.readlines()
        assert len(lines) == len(EXPECTED_LOGS)
        for line, expected_log in zip(lines, EXPECTED_LOGS):
            assert expected_log.format("LogOne") in line

    with open(path2) as file2:
        lines = file2.readlines()
        assert len(lines) == 4 + 2
        for line, expected_log in zip(lines[:4], EXPECTED_LOGS[-4:]):
            assert expected_log.format("LogTwo") in line
        for line, expected_log in zip(lines[4:], EXPECTED_LOGS[-2:]):
            assert expected_log.format("LogThree") in line

    # Invalid names

    with pytest.raises(ValueError):
        log.create_logger(None)

    with pytest.raises(TypeError):
        log.create_logger(1)

    with pytest.raises(ValueError):
        log.create_logger("")

    # Existant logger

    log4 = log.create_logger("LogFour")
    with pytest.raises(ValueError):
        log.create_logger("LogFour")
    log4 = log.create_logger("LogFour", overwrite=True)

    assert log4.level == 20


def test_removal():

    log.clear_loggers()
    assert len(log.get_loggers()) == 0

    log1 = log.create_logger("test1")
    log.create_logger("test2")
    assert len(log.get_loggers()) == 2

    # Close one logger
    with pytest.raises(ValueError):
        log.create_logger("test1")
    log.close_logger(log1)
    assert len(log.get_loggers()) == 1
    log.create_logger("test1")
    assert len(log.get_loggers()) == 2

    # Close all loggers
    with pytest.raises(ValueError):
        log.create_logger("test1")
    with pytest.raises(ValueError):
        log.create_logger("test2")
    log.clear_loggers()
    assert len(log.get_loggers()) == 0
    log.create_logger("test2")
    assert len(log.get_loggers()) == 1


def test_logclass():
    instance = log.LogClass(name="myLogInstance", loglvl="ERROR")

    assert instance.get_loglvl(explicit=True) == "ERROR"
    instance.set_loglvl("INFO")
    assert instance.get_loglvl(explicit=True) == "INFO"
    instance.set_loglvl("DEBUG")
    assert instance.get_loglvl(explicit=True) == "DEBUG"
    assert instance.get_loglvl() == 10

    # Delete (make sure logger becomes available)
    with pytest.raises(ValueError):
        log.LogClass(name="myLogInstance")
    del instance
    instance = log.LogClass(name="myLogInstance")
    assert instance.get_loglvl(explicit=True) == "INFO"

    # Default loglvl
    assert instance.get_loglvl(explicit=True) == "INFO"
