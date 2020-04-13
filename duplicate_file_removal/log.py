from os import path


class Log:
    _instance = None
    _log_file = 'dup_file_removal_log.txt'

    def __init__(self, log_file_dir: str = '\\'):
        if self._instance:
            pass
        else:
            if not path.isdir(log_file_dir):
                log_file_dir = '\\'
            self._instance = open(log_file_dir + "\\" + self._log_file, "a+")

    def report(self) -> str:
        return f"Log file location: {path.realpath(self._instance.name)}"
