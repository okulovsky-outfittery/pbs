from mock import MagicMock
import pbclient
class TestDefault(object):

    """Test class for pbs.helpers."""

    error = {"action": "GET",
             "exception_cls": "NotFound",
             "exception_msg": "(NotFound)",
             "status": "failed",
             "status_code": 404,
             "target": "/api/app"}

    config = MagicMock()
    config.server = 'http://server'
    config.api_key = 'apikey'
    config.pbclient = pbclient
    config.project = {'name': 'name',
                 'description': 'description',
                 'short_name': 'short_name'}

    def tearDown(self):
        self.error['status'] = 'failed'
