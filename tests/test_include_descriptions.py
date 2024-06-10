# tests/test_include_descriptions.py

import unittest
from unittest.mock import patch, MagicMock
from sigai.main import generate_summary


class TestIncludeDescriptions(unittest.TestCase):

    @patch('sigai.main.Github')
    @patch('sigai.main.requests.get')
    def test_generate_summary_with_descriptions(self, mock_get, mock_github):
        mock_repo = MagicMock()
        mock_file1 = MagicMock()
        mock_file1.path = 'module1.py'
        mock_file1.download_url = 'https://example.com/module1.py'

        def mock_get_contents(path=""):
            return [mock_file1]

        mock_repo.get_contents.side_effect = mock_get_contents
        mock_github.return_value.get_repo.return_value = mock_repo

        mock_get.return_value.text = """
def func1(arg1, arg2):
    \"\"\"This is a test function\"\"\"
    return arg1 + arg2

class MyClass:
    \"\"\"This is a test class\"\"\"
    def method1(self, arg1):
        \"\"\"This is a test method\"\"\"
        return arg1
"""

        repo_url = "https://github.com/your_username/repository"

        summary = generate_summary(repo_url, include_descriptions=True)
        self.assertIn("func1(arg1, arg2) -> None - This is a test function", summary)
        self.assertIn("method1(self, arg1) -> None - This is a test method", summary)

        summary_no_descriptions = generate_summary(repo_url, include_descriptions=False)
        self.assertIn("func1(arg1, arg2) -> None", summary_no_descriptions)
        self.assertNotIn("func1(arg1, arg2) -> None - This is a test function", summary_no_descriptions)
        self.assertIn("method1(self, arg1) -> None", summary_no_descriptions)
        self.assertNotIn("method1(self, arg1) -> None - This is a test method", summary_no_descriptions)


if __name__ == '__main__':
    unittest.main()
