from duplicate_file_removal.processor import RecordsProcessor
from duplicate_file_removal.scanner import Scanner

if __name__ == "__main__":
    result = Scanner.scan_multiple_paths("Path_A", "Path_B", "etc...")
    RecordsProcessor.remove_duplicates(result)
