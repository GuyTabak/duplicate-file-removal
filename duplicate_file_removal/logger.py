from logging import getLogger, FileHandler, DEBUG, INFO
from pathlib import Path

# General usage logger
logger = getLogger('project_logger')
logger.setLevel(DEBUG)
Path('..\\logs').mkdir(parents=True, exist_ok=True)
handler_ = FileHandler('..\\logs\\dup_log_file.txt')
handler_.setLevel(DEBUG)
logger.addHandler(handler_)

# Results logger
res_logger = getLogger('results_logger')
logger.setLevel(INFO)
res_handler = FileHandler('..\\Logs\\res_log_file.txt')
res_handler.setLevel(INFO)
res_logger.addHandler(res_handler)
