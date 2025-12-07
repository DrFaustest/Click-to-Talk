"""
Tests for setup.py
"""

import importlib
from unittest.mock import mock_open, patch


class TestSetup:
    @patch('setuptools.setup')
    def test_setup_reads_files_and_invokes_setup(self, mock_setup):
        req_data = 'packageA==1.0.0\npackageB==2.0.0'
        readme_data = '# Click-to-Talk\nDescription'

        def open_mock(path, *args, **kwargs):
            if path == "requirements.txt":
                return mock_open(read_data=req_data)()
            if path == "README.md":
                return mock_open(read_data=readme_data)()
            raise FileNotFoundError(path)

        with patch('builtins.open', open_mock):
            import setup as setup_module
            importlib.reload(setup_module)

        assert mock_setup.call_count >= 1
        kwargs = mock_setup.call_args.kwargs
        assert kwargs['install_requires'] == req_data.split('\n')
        assert kwargs['long_description'] == readme_data
