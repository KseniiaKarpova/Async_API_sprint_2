import logging

logger = logging.getLogger('tests')
logger.setLevel(logging.INFO)


formatter = logging.Formatter(
    '%(asctime)s %(levelname)-8s [%(filename)-16s:%(lineno)-5d] %(message)s'
)
