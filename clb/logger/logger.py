import logging


def init_logger(name: str, log_level: str) -> logging.Logger:
    logger = logging.getLogger(name)
    c_handler = logging.StreamHandler()
    try:
        logger.setLevel(log_level)
        c_handler.setLevel(log_level)
    except ValueError as e:
        logger.setLevel(logging.DEBUG)
        c_handler.setLevel(logging.DEBUG)
        print(f'Error: Wrong log_level: {e}')

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    c_handler.setFormatter(formatter)

    logger.addHandler(c_handler)

    return logger
