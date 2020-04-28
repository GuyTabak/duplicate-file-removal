from duplicate_file_removal.scanner import Scanner


if __name__ == "__main__":
    result = Scanner.scan_multiple_paths("C:\\", "F:\\")
    with open("C:\\Users\\Guy\\dup_log.txt", "w+") as f:
        for items in result.dict_.values():
            if len(items) > 1:
                f.write(str([i.full_path.encode("utf-8") for i in items]) + "\n")
