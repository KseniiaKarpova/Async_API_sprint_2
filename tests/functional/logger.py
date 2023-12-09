import logging

logger = logging.getLogger('tests')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s [%(filename)-16s:%(lineno)-5d] %(message)s'
)
ch.setFormatter(formatter)
logger.addHandler(ch)
