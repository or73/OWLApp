"""
File Path: application/modules/aux_funcs/logs.py
Description: setup logs of the App
This will have the function to create the logs of the App.
Copyright (c) 2019. This Application has been developed by OR73.
"""
import logging
from colorlog import ColoredFormatter
from logging.handlers import TimedRotatingFileHandler


def init_logger(dunder_name, testing_mode) -> logging.Logger:
    # Log
    log_format = ("\n------- START LOG MESSAGE -------\n"
                  "Level: %(levelname)-8s\n"
                  "Message: %(message)s\n"
                  "Name: %(name)s\n"
                  "FuncName: %(funcName)s\n"
                  "Time: %(asctime)s\n"
                  "Path Name: %(pathname)s : %(lineno)d\n"
                  "------- END LOG MESSAGE -------\n")
    date_format = '%d/%m/%Y %H:%M:%S'
    bold_seq = '\033[1m'
    color_log_format = (
        f'{bold_seq}'
        '%(log_color)s'
        f'{log_format}'
    )
    # colorlog.basicConfig(format=color_log_format)
    logger = logging.getLogger(dunder_name)

    if testing_mode:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    file_formatter = ColoredFormatter(fmt=log_format,
                                      datefmt=date_format,
                                      reset=False,
                                      log_colors={
                                          'DEBUG': 'cyan',
                                          'INFO': 'green',
                                          'WARNING': 'yellow',
                                          'ERROR': 'purple',
                                          'CRITICAL': 'red'
                                      },
                                      secondary_log_colors={
                                          'message': {
                                              'ERROR': 'purple',
                                              'CRITICAL': 'bold_red'
                                          }
                                      },
                                      style='%')

    # --------------------- Output FULL log
    # Create a file for each day.  Delete logs over 30 days old.
    file_handler = TimedRotatingFileHandler('0.owl_app.log', when='D', backupCount=30)
    # file_formatter = logging.Formatter(log_format)
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)
    print('Full LOG\t\t- ', file_handler)
    logger.addHandler(file_handler)

    # --------------------- Output WARNING log
    # Create a file for each day. Delete logs over 30 days old
    file_handler = TimedRotatingFileHandler('1.owl_app.warning.log', when='D', backupCount=30)
    # file_formatter = logging.Formatter(log_format)
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.WARNING)
    print('WARNING LOG\t\t- ', file_handler)
    logger.addHandler(file_handler)

    # --------------------- Output ERROR log
    # Create a file for each day. Delete logs over 30 days old
    file_handler = TimedRotatingFileHandler('2.owl_app.error.log', when='D', backupCount=30)
    # file_formatter = logging.Formatter(log_format)
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.ERROR)
    print('ERROR LOG\t\t- ', file_handler)
    logger.addHandler(file_handler)

    # --------------------- Output CRITICAL log
    # Create a file for each day. Delete logs over 30 days old
    file_handler = TimedRotatingFileHandler('3.owl_app.critical.log', when='D', backupCount=30)
    # file_formatter = logging.Formatter(log_format)
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.CRITICAL)
    print('CRITICAL LOG\t- ', file_handler)
    logger.addHandler(file_handler)

    return logger
