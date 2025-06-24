import unittest

from functions.get_files_info import (
    get_file_content,
    get_files_info,
    run_python_file,
    write_file,
)


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

    def test_write_file(self):
        print("write_file('calculator', 'lorem.txt', 'wait, this isn't lorem ipsum'):")
        print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
        print(
            "\nwrite_file('calculator', 'pkg/morelorem.txt', 'lorem ipsum dolor sit amet'):",
        )
        print(
            write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
        )
        print(
            "\nwrite_file('calculator', '/tmp/temp.txt', 'this should not be allowed'):",
        )
        print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

    def test_run_python_file(self):
        print("run_python_file('calculator', 'main.py'):")
        print(run_python_file("calculator", "main.py"))
        print("\nrun_python_file('calculator', 'tests.py'):")
        print(run_python_file("calculator", "tests.py"))
        print("\nrun_python_file('calculator', '../main.py'):")
        print(run_python_file("calculator", "../main.py"))
        print("\nrun_python_file('calculator', 'nonexistent.py'):")
        print(run_python_file("calculator", "nonexistent.py"))

    def test_run_python_file_with_args(self):
        print("run_python_file('calculator', 'main.py', ['2 + 2']):")
        print(run_python_file("calculator", "main.py", ["2 + 2"]))
        print("\nrun_python_file('calculator', 'main.py', ['3 * 4 + 5']):")
        print(run_python_file("calculator", "main.py", ["3 * 4 + 5"]))
        print(
            "\nrun_python_file('calculator', 'main.py', ['2 * 3 - 8 / 2 + 5']):",
        )
        print(
            run_python_file(
                "calculator",
                "main.py",
                ["2 * 3 - 8 / 2 + 5"],
            ),
        )


if __name__ == "__main__":
    unittest.main()
