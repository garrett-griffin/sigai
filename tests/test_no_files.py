# tests/test_no_files.py

import unittest
from unittest.mock import patch, MagicMock
from sigai.main import fetch_files_from_github


class TestNoFiles(unittest.TestCase):

    @patch('sigai.main.Github')
    def test_fetch_no_files(self, mock_github):
        mock_repo = MagicMock()

        def mock_get_contents(path=""):
            return []

        mock_repo.get_contents.side_effect = mock_get_contents
        mock_github.return_value.get_repo.return_value = mock_repo

        repo_url = "https://github.com/your_username/empty_repository"

        files = fetch_files_from_github(repo_url, verbose=False)
        self.assertEqual(len(files), 0)

        files_verbose = fetch_files_from_github(repo_url, verbose=True)
        self.assertEqual(len(files_verbose), 0)


if __name__ == '__main__':
    unittest.main()
