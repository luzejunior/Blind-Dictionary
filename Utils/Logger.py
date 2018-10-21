import logging
import sys

loggers = {}


def my_logger(logger_name):
    if loggers.get(logger_name):
        return loggers.get(logger_name)
    else:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.handlers.clear()
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        loggers[logger_name] = logger

    return logger


#
# class Logger:
#     _logger = None
#
#     def __init__(self, logger_name):
#         if (self._logger and (logger_name != self._logger.name)) or not self._logger:
#             self._logger = logging.getLogger(logger_name)
#             self._logger.setLevel(logging.DEBUG)
#             self._logger.handlers.clear()
#             ch = logging.StreamHandler(sys.stdout)
#             ch.setLevel(logging.DEBUG)
#             formatter = logging.Formatter('[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s')
#             ch.setFormatter(formatter)
#             self._logger.addHandler(ch)
#
#     def get_logger(self):
#         return self._logger