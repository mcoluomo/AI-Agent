import unittest

from functions.get_files_info import get_files_info


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


if __name__ == "__main__":
    unittest.main()
