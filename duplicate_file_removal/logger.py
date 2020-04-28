from logging import getLogger, FileHandler, DEBUG

logger = getLogger('project_logger')
logger.setLevel(DEBUG)
handler_ = FileHandler('..\\logs\\dup_log_file.txt')
handler_.setLevel(DEBUG)
logger.addHandler(handler_)
