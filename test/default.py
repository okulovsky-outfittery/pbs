"""Test module for pbs client."""
from mock import MagicMock


class TestDefault(object):

    """Test class for pbs.helpers."""

    error = {"action": "GET",
             "exception_cls": "NotFound",
             "exception_msg": "(NotFound)",
             "status": "failed",
             "status_code": 404,
             "target": "/api/project"}

    error_task = {"action": "GET",
                  "exception_cls": "NotFound",
                  "exception_msg": "(NotFound)",
                  "status": "failed",
                  "status_code": 404,
                  "target": "/api/task"}

    config = MagicMock()
    config.server = 'http://server'
    config.api_key = 'apikey'
    config.project = {'name': 'name',
                      'description': 'description',
                      'short_name': 'short_name'}

    def tearDown(self):
        """Tear down method."""
        self.error['status'] = 'failed'
