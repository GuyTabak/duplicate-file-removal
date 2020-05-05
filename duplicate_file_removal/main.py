from duplicate_file_removal.processor import RecordsProcessor
from duplicate_file_removal.scanner import Scanner

if __name__ == "__main__":
    result = Scanner.scan_multiple_paths("C:\\")
    RecordsProcessor.remove_duplicates_simulation(result, [])
