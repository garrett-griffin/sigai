import unittest
from unittest.mock import patch, MagicMock
from sigai.main import fetch_files_from_github


class TestSigai(unittest.TestCase):

    @patch('sigai.main.Github')
    def test_fetch_files_from_github(self, mock_github):
        # Mock GitHub repository contents
        mock_repo = MagicMock()
        mock_file1 = MagicMock()
        mock_file1.path = 'module1.py'
        mock_file1.download_url = 'https://example.com/module1.py'
        mock_file2 = MagicMock()
        mock_file2.path = 'tests/test_module.py'
        mock_file2.download_url = 'https://example.com/tests/test_module.py'

        # Mock the get_contents method
        def mock_get_contents(path=""):
            if path == "":
                return [mock_file1, mock_file2]
            return []

        mock_repo.get_contents.side_effect = mock_get_contents

        mock_github.return_value.get_repo.return_value = mock_repo

        repo_url = "https://github.com/your_username/your_repository"

        # Fetch files without verbose
        files = fetch_files_from_github(repo_url, verbose=False)
        print("Files fetched without verbose:", [f.path for f in files])
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].path, 'module1.py')

        # Fetch files with verbose
        files_verbose = fetch_files_from_github(repo_url, verbose=True)
        print("Files fetched with verbose:", [f.path for f in files_verbose])
        self.assertEqual(len(files_verbose), 2)
        self.assertEqual(files_verbose[0].path, 'module1.py')
        self.assertEqual(files_verbose[1].path, 'tests/test_module.py')


if __name__ == '__main__':
    unittest.main()
