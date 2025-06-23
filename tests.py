import unittest

from functions.get_files_info import get_file_content, get_files_info


class TestGetFilesInfo(unittest.TestCase):
    def test_get_files_info(self):
        print("get_files_info('calculator', '.'):")
        print(get_files_info("calculator", "."))
        print("\nget_files_info('calculator', 'pkg'):")
        print(get_files_info("calculator", "pkg"))
        print("\nget_files_info('calculator', '/bin'):")
        print(get_files_info("calculator", "/bin"))
        print("\nget_files_info('calculator', '../'):")
        print(get_files_info("calculator", "../"))

    def test_get_file_content(self):
        print("get_file_content('calculator', 'main.py'):")
        print(get_file_content("calculator", "main.py"))
        print("\nget_file_content('calculator', 'pkg/calculator.py'):")
        print(get_file_content("calculator", "pkg/calculator.py"))
        print("\nget_file_content('calculator', '/bin/cat'):")
        print(get_file_content("calculator", "/bin/cat"))


if __name__ == "__main__":
    unittest.main()
