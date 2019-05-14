import logging


def init_logger(name: str, log_level: str = 'DEBUG') -> logging.Logger:
    logger = logging.getLogger(name)
    c_handler = logging.StreamHandler()
    try:
        logger.setLevel(log_level)
        c_handler.setLevel(log_level)
    except ValueError as error:
        logger.setLevel(logging.DEBUG)
        c_handler.setLevel(logging.DEBUG)
        print(f'Error: Wrong log_level: {error}')

    formatter = logging.Formatter('%(asctime)s %(levelname)s in %(name)s: %(message)s')
    c_handler.setFormatter(formatter)

    logger.addHandler(c_handler)

    return logger
