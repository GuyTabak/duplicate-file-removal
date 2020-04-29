from duplicate_file_removal.scanner import Scanner

from pytest import fixture



@fixture(scope="module")
def scanner():
    # Temporary Files\Directories are created in the 'AppData' path which is restricted in the code
    Scanner.RESTRICTED_DIRECTORIES.remove("AppData")
    yield Scanner
    Scanner.RESTRICTED_DIRECTORIES.append("AppData")