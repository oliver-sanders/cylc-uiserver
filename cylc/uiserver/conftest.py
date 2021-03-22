# Copyright (C) NIWA & British Crown (Met Office) & Contributors.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pathlib import Path
from shutil import rmtree
from tempfile import TemporaryDirectory
from textwrap import dedent

import pytest


@pytest.fixture(scope='module')
def mod_tmp_path():
    """A tmp_path fixture with module-level scope."""
    path = Path(TemporaryDirectory().name)
    path.mkdir()
    yield path
    rmtree(path)


@pytest.fixture(scope='module')
def ui_build_dir(mod_tmp_path):
    """A dummy UI build tree containing three versions '1.0', '2.0' & '3.0'."""
    for version in range(1, 4):
        path = mod_tmp_path / f'{version}.0'
        path.mkdir()
        (path / 'index.html').touch()
    yield mod_tmp_path


@pytest.fixture
def mock_config(monkeypatch):
    """Mock the UIServer/Hub configuration file.

    This fixture auto-loads by setting a blank config.

    Call the fixture with config code to override.

    mock_config('''
        c.UIServer.my_config = 'my_value'
    ''')

    Can be called multiple times.

    Note the code you provide is exec'ed just like the real config file.

    """
    conf = ''

    def _write(string=''):
        nonlocal conf
        conf = dedent(string)

    def _read(obj, _):
        nonlocal conf
        exec(conf, {'c': obj.config})

    monkeypatch.setattr(
        'cylc.uiserver.main.CylcUIServer.load_config_file',
        _read
    )

    yield _write
