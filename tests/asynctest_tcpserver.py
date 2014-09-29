#!/usr/bin/env python
#
#
#     https://github.com/rdbhost/python-embedded-test-server

import unittest
import requests
import socket
import asyncio

import sys

import testtcpserver
from testtcpserver import RECEIVE, CommandServer, OneShotServer, AsyncioCommandServer


class TestAsync(unittest.TestCase):

    def test0_Simulate_Web_Request(self):

        webResponse = \
"""HTTP/1.0 200 OK
Accept-Ranges:bytes
Age:341247
Content-Length:80949
Content-Type:text/html
Date:Wed, 24 Sep 2014 23:56:38 GMT
ETag:"541e091a-13c35"
Last-Modified:Sat, 20 Sep 2014 23:09:14 GMT
Server:Apache
Via:1.1 varnish
X-Cache:HIT
X-Cache-Hits:29
X-Served-By:cache-ord1721-ORD


"""
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        web_server = AsyncioCommandServer([RECEIVE, webResponse], loop=loop, reader=reader, host='127.0.0.1', port=2222)
        def _temp():
            yield None
            sc = requests.get('http://127.0.0.1:{0}'.format(web_server.port), verify=False)
            resp = yield from reader.read()
            self.assertTrue(b'GET' in resp, resp)

        loop.run_until_complete(_temp())
        web_server.stop()



if __name__ == '__main__':
    unittest.main()
