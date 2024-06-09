import unittest
from unittest.mock import patch, MagicMock
from sigai.main import generate_summary


class TestSigai(unittest.TestCase):

    @patch('sigai.main.Github')
    @patch('sigai.main.requests.get')
    def test_generate_summary(self, mock_get, mock_github):
        # Mock GitHub repository contents
        mock_repo = MagicMock()
        mock_file1 = MagicMock()
        mock_file1.path = 'module1.py'
        mock_file1.download_url = 'https://example.com/module1.py'
        mock_file2 = MagicMock()
        mock_file2.path = 'tests/test_module.py'
        mock_file2.download_url = 'https://example.com/tests/test_module.py'

        mock_repo.get_contents.return_value = [mock_file1, mock_file2]
        mock_github.return_value.get_repo.return_value = mock_repo

        # Mock file content
        mock_get.return_value.text = """
def func1(arg1, arg2):
    return arg1 + arg2

class MyClass:
    def method1(self, arg1):
        return arg1
"""

        repo_url = "https://github.com/your_username/your_repository"
        summary = generate_summary(repo_url)

        expected_summary = (
            "module1.py\n"
            "func1(arg1, arg2) -> None\n"
            "MyClass\n"
            "  method1(self, arg1) -> None"
        )

        self.assertEqual(summary.strip(), expected_summary)

    @patch('sigai.main.Github')
    @patch('sigai.main.requests.get')
    def test_generate_summary_verbose(self, mock_get, mock_github):
        # Mock GitHub repository contents
        mock_repo = MagicMock()
        mock_file1 = MagicMock()
        mock_file1.path = 'module1.py'
        mock_file1.download_url = 'https://example.com/module1.py'
        mock_file2 = MagicMock()
        mock_file2.path = 'tests/test_module.py'
        mock_file2.download_url = 'https://example.com/tests/test_module.py'

        mock_repo.get_contents.return_value = [mock_file1, mock_file2]
        mock_github.return_value.get_repo.return_value = mock_repo

        # Mock file content
        mock_get.return_value.text = """
def func1(arg1, arg2):
    return arg1 + arg2

class MyClass:
    def method1(self, arg1):
        return arg1
"""

        repo_url = "https://github.com/your_username/your_repository"
        summary = generate_summary(repo_url, verbose=True)

        expected_summary = (
            "module1.py\n"
            "func1(arg1, arg2) -> None\n"
            "MyClass\n"
            "  method1(self, arg1) -> None\n\n"
            "tests/test_module.py\n"
            "func1(arg1, arg2) -> None\n"
            "MyClass\n"
            "  method1(self, arg1) -> None"
        )

        self.assertEqual(summary.strip(), expected_summary)


if __name__ == '__main__':
    unittest.main()
