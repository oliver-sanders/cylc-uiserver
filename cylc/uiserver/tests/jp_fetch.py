"""
Acknowledgment:
    The code in this file is a modification of code from the Jupyter Server
    project and retains the Jupyter Server license (3-Clause BSD).

Jupyter Server License:
    This project is licensed under the terms of the Modified BSD License
    (also known as New or Revised or 3-Clause BSD), as follows:

    - Copyright (c) 2001-2015, IPython Development Team
    - Copyright (c) 2015-, Jupyter Development Team

    All rights reserved.
"""

import urllib

from jupyter_server.utils import url_path_join
import pytest
import tornado
from tornado.escape import url_escape


@pytest.fixture
def jp_ws_fetch(
    jp_serverapp,
    http_server_client,
    jp_auth_header,
    jp_http_port,
    jp_base_url,
):
    """Sends a websocket request to a test server.

    The fixture is a factory; it can be called like
    a function inside a unit test. Here's a basic
    example of how use this fixture:

    .. code-block:: python

        async def my_test(jp_fetch, jp_ws_fetch):
            # Start a kernel
            r = await jp_fetch(
                'api', 'kernels',
                method='POST',
                body=json.dumps({
                    'name': "python3"
                })
            )
            kid = json.loads(r.body.decode())['id']

            # Open a websocket connection.
            ws = await jp_ws_fetch(
                'api', 'kernels', kid, 'channels'
            )
            ...
    """

    def client_fetch(*parts, headers=None, params=None, **kwargs):
        if not headers:
            headers = {}
        if not params:
            params = {}
        # Handle URL strings
        path_url = url_escape(url_path_join(*parts), plus=False)
        base_path_url = url_path_join(jp_base_url, path_url)
        urlparts = urllib.parse.urlparse(
            "ws://localhost:{}".format(jp_http_port)
        )
        urlparts = urlparts._replace(
            path=base_path_url,
            query=urllib.parse.urlencode(params)
        )
        url = urlparts.geturl()
        # Add auth keys to header
        headers.update(jp_auth_header)
        # Make request.
        req = tornado.httpclient.HTTPRequest(
            url,
            headers=headers,
            connect_timeout=120
        )
        return tornado.websocket.websocket_connect(req)

    return client_fetch
