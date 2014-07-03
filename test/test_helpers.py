"""Test module for pbs client."""
import pbclient
import json
from default import TestDefault
from helpers import *
from mock import patch, MagicMock
from nose.tools import assert_raises
from requests import exceptions


class TestHelpers(TestDefault):

    """Test class for pbs.helpers."""

    @patch('pbclient.find_app')
    def test_find_app_by_short_name(self, mock):
        """Test find_app_by_short_name returns a project."""
        mock.return_value = ['project']
        project = find_app_by_short_name('project', pbclient)
        err_msg = "It shoul return: project"
        assert project == 'project', err_msg

    @patch('pbclient.find_app')
    def test_find_app_by_short_name_connection_error(self, mock):
        """Test find_app_by_short_name connection_error is raised."""
        mock.side_effect = exceptions.ConnectionError
        assert_raises(exceptions.ConnectionError,
                      find_app_by_short_name,
                      'project',
                      pbclient)

    @patch('helpers.format_error')
    @patch('pbclient.find_app')
    def test_find_app_by_short_name_error(self, mock, mock2):
        """Test find_app_by_short_name error is printed."""
        mock.return_value = self.error
        find_app_by_short_name('project', pbclient)
        mock2.assert_called_with('pbclient.find_app', self.error)

    def test_check_api_error_raises_exception(self):
        """Test check_api_error raises HTTPError exception."""
        assert_raises(exceptions.HTTPError, check_api_error, self.error)

    def test_check_api_error_returns_none(self):
        """Test check_api_error returns none."""
        error = self.error
        error['status'] = 'wrong'
        check_api_error(error)
        error = 'not_a_dict'
        check_api_error(error)

    @patch('pbclient.find_app')
    def test_format_error(self, mock):
        """Test format_error works."""
        mock.return_value = ['project']
        assert_raises(SystemExit, format_error, 'pbclient.find_app', ['error'])
        assert_raises(SystemExit, format_error, 'pbclient.find_app', self.error)

    def test_format_json_task(self):
        """Test format_json_task works."""
        tmp = {'key': 'value'}
        res = format_json_task(json.dumps(tmp))
        err_msg = "It should return a JSON object"
        assert type(res) == dict, err_msg
        assert res['key'] == tmp['key'], err_msg

        tmp = "key: value"
        res = format_json_task(tmp)
        err_msg = "It should return a string"
        assert type(res) == str, err_msg
        assert res == tmp, err_msg


    @patch('helpers.find_app_by_short_name')
    def test_update_project_create(self, find_mock):
        """Test update_project works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        task_presenter = MagicMock()
        task_presenter.read.return_value = "presenter"

        tutorial = MagicMock()
        tutorial.read.return_value = "tutorial"

        long_description = MagicMock()
        long_description.read.return_value = "long_description"

        pbclient = MagicMock()
        pbclient.update_app.return_value = {'short_name': 'short_name'}
        self.config.pbclient = pbclient
        res = _update_project(self.config, task_presenter,
                              long_description, tutorial)
        assert res == 'Project short_name updated!', res

    @patch('helpers.find_app_by_short_name')
    def test_update_project_connection_error(self, find_mock):
        """Test update_project connection error works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        task_presenter = MagicMock()
        task_presenter.read.return_value = "presenter"

        tutorial = MagicMock()
        tutorial.read.return_value = "tutorial"

        long_description = MagicMock()
        long_description.read.return_value = "long_description"

        pbclient = MagicMock()
        pbclient.update_app.side_effect = exceptions.ConnectionError
        self.config.pbclient = pbclient
        res = _update_project(self.config, task_presenter,
                              long_description, tutorial)
        assert res == "Connection Error! The server http://server is not responding", res

    @patch('helpers.find_app_by_short_name')
    def test_update_project_another_error(self, find_mock):
        """Test update_project another error works."""
        project = MagicMock()
        project.name = 'name'
        project.short_name = 'short_name'
        project.description = 'description'
        project.info = dict()

        find_mock.return_value = project

        task_presenter = MagicMock()
        task_presenter.read.return_value = "presenter"

        tutorial = MagicMock()
        tutorial.read.return_value = "tutorial"

        long_description = MagicMock()
        long_description.read.return_value = "long_description"

        pbclient = MagicMock()
        pbclient.update_app.return_value = self.error
        self.config.pbclient = pbclient
        assert_raises(SystemExit, _update_project, self.config,
                      task_presenter, long_description, tutorial)
