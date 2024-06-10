# tests/test_generate_summary.py

import unittest
from unittest.mock import patch, MagicMock
from sigai.main import generate_summary


class TestGenerateSummary(unittest.TestCase):

    @patch('sigai.main.Github')
    @patch('sigai.main.requests.get')
    def test_generate_summary_mixed_files(self, mock_get, mock_github):
        mock_repo = MagicMock()
        mock_file1 = MagicMock()
        mock_file1.path = 'module1.py'
        mock_file1.download_url = 'https://example.com/module1.py'
        mock_file2 = MagicMock()
        mock_file2.path = 'tests/test_module.py'
        mock_file2.download_url = 'https://example.com/tests/test_module.py'
        mock_file3 = MagicMock()
        mock_file3.path = 'module/__init__.py'
        mock_file3.download_url = 'https://example.com/module/__init__.py'

        def mock_get_contents(path=""):
            return [mock_file1, mock_file2, mock_file3]

        mock_repo.get_contents.side_effect = mock_get_contents
        mock_github.return_value.get_repo.return_value = mock_repo

        mock_get.side_effect = [
            MagicMock(text="""
def func1(arg1, arg2):
    return arg1 + arg2

class MyClass:
    def method1(self, arg1):
        return arg1
"""),
            MagicMock(text="""
def test_func(arg1, arg2):
    return arg1 + arg2
"""),
            MagicMock(text=""),
            MagicMock(text="""
def func1(arg1, arg2):
    return arg1 + arg2

class MyClass:
    def method1(self, arg1):
        return arg1
"""),
            MagicMock(text="""
def test_func(arg1, arg2):
    return arg1 + arg2
"""),
            MagicMock(text="")
        ]

        repo_url = "https://github.com/your_username/mixed_repository"

        summary = generate_summary(repo_url, verbose=False)
        self.assertIn("module1.py", summary)
        self.assertIn("func1(arg1, arg2) -> None", summary)
        self.assertIn("MyClass", summary)
        self.assertIn("method1(self, arg1) -> None", summary)
        self.assertNotIn("tests/test_module.py", summary)
        self.assertNotIn("module/__init__.py", summary)

        summary_verbose = generate_summary(repo_url, verbose=True)
        self.assertIn("module1.py", summary_verbose)
        self.assertIn("func1(arg1, arg2) -> None", summary_verbose)
        self.assertIn("MyClass", summary_verbose)
        self.assertIn("method1(self, arg1) -> None", summary_verbose)
        self.assertIn("tests/test_module.py", summary_verbose)
        self.assertIn("test_func(arg1, arg2) -> None", summary_verbose)
        self.assertIn("module/__init__.py", summary_verbose)


if __name__ == '__main__':
    unittest.main()
