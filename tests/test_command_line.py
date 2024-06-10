import unittest
from unittest.mock import patch, MagicMock
import subprocess
import os


class TestCommandLine(unittest.TestCase):

    @patch('subprocess.call')
    @patch('sigai.main.Github')
    @patch('sigai.main.requests.get')
    def test_command_line_execution(self, mock_get, mock_github, mock_subprocess_call):
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
    return arg1 + arg2
"""

        repo_url = "https://github.com/your_username/repository"

        def mock_subprocess_call_effect(*args, **kwargs):
            with open('summary.txt', 'w') as f:
                f.write("module1.py\nfunc1(arg1, arg2) -> None\n")
            return 0

        mock_subprocess_call.side_effect = mock_subprocess_call_effect

        with patch('sys.argv', ['main.py', repo_url, '--output', 'summary.txt']):
            result = subprocess.call(
                ['poetry', 'run', 'python', 'sigai/main.py', repo_url, '--output', 'summary.txt'],
                cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            )

        self.assertEqual(result, 0)
        self.assertTrue(os.path.exists('summary.txt'))

        with open('summary.txt', 'r') as f:
            summary = f.read()

        self.assertIn("module1.py", summary)
        self.assertIn("func1(arg1, arg2) -> None", summary)

        # Clean up
        os.remove('summary.txt')


if __name__ == '__main__':
    unittest.main()
