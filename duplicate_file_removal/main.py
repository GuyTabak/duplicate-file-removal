from duplicate_file_removal.scanner import Scanner


if __name__ == "__main__":
    result = Scanner.scan_and_generate_records("C:\\")
    with open("C:\\Users\\Guy\\dup_log1.txt", "w+") as f:
        for items in result.dict_.values():
            if len(items) > 1:
                f.write(str([i.full_path for i in items]) + "\n")
