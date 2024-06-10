# tests/test_files_in_tests_directory.py

import unittest
from unittest.mock import patch, MagicMock
from sigai.main import fetch_files_from_github


class TestFilesInTestsDirectory(unittest.TestCase):

    @patch('sigai.main.Github')
    def test_fetch_files_in_tests_directory(self, mock_github):
        mock_repo = MagicMock()
        mock_file1 = MagicMock()
        mock_file1.path = 'tests/test_module.py'
        mock_file1.download_url = 'https://example.com/tests/test_module.py'

        def mock_get_contents(path=""):
            return [mock_file1]

        mock_repo.get_contents.side_effect = mock_get_contents
        mock_github.return_value.get_repo.return_value = mock_repo

        repo_url = "https://github.com/your_username/tests_repository"

        files = fetch_files_from_github(repo_url, verbose=False)
        self.assertEqual(len(files), 0)

        files_verbose = fetch_files_from_github(repo_url, verbose=True)
        self.assertEqual(len(files_verbose), 1)
        self.assertEqual(files_verbose[0].path, 'tests/test_module.py')


if __name__ == '__main__':
    unittest.main()
