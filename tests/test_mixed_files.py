# tests/test_mixed_files.py

import unittest
from unittest.mock import patch, MagicMock
from sigai.main import fetch_files_from_github


class TestMixedFiles(unittest.TestCase):

    @patch('sigai.main.Github')
    def test_fetch_mixed_files(self, mock_github):
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

        repo_url = "https://github.com/your_username/mixed_repository"

        files = fetch_files_from_github(repo_url, verbose=False)
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].path, 'module1.py')

        files_verbose = fetch_files_from_github(repo_url, verbose=True)
        self.assertEqual(len(files_verbose), 3)
        self.assertEqual(files_verbose[0].path, 'module1.py')
        self.assertEqual(files_verbose[1].path, 'tests/test_module.py')
        self.assertEqual(files_verbose[2].path, 'module/__init__.py')


if __name__ == '__main__':
    unittest.main()
