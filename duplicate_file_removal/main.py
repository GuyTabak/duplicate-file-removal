from duplicate_file_removal.processor import RecordsProcessor
from duplicate_file_removal.scanner import Scanner

if __name__ == "__main__":
    # result = Scanner.scan_multiple_paths("C:\\")
    result = Scanner.scan_by_file_extension(["lalala", "lalla2", "dat"], "C:\\")
    RecordsProcessor.remove_duplicates_simulation(result, [])
