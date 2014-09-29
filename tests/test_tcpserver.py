#!/usr/bin/env python
#
#  XXX  Identifying information about tests here.
#
#===============
#  This is based on a skeleton test file, more information at:
#
#     https://github.com/linsomniac/python-unittest-skeleton

#raise NotImplementedError(
#        'To customize, remove this line and customize where it says XXX')

import unittest
import requests
import socket

import sys

import testtcpserver
from testtcpserver import RECEIVE, CommandServer, OneShotServer


class TestAll(unittest.TestCase):

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
        web_server = OneShotServer([RECEIVE, webResponse])
        sc = requests.get('http://127.0.0.1:{0}'.format(web_server.port), verify=False)

    def test1_Simulate_Socket_Read(self):

        receive_then_disconnect_server = OneShotServer([RECEIVE, 'STORED\r\n'])
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('127.0.0.1', receive_then_disconnect_server.port))
        sock.sendall(b'HELLO')
        data = sock.recv(1024)
        sock.close()
        self.assertTrue(b'STORED' in data)

    def test2_Command(self):

        receive_then_disconnect_server = CommandServer([RECEIVE, 'STORED\r\n'])
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('127.0.0.1', receive_then_disconnect_server.port))
        sock.sendall(b'HELLO')
        data = sock.recv(1024)
        sock.close()
        self.assertTrue(b'STORED' in data)

        self.assertFalse(receive_then_disconnect_server.STOPPED)

        receive_then_disconnect_server.stop()
        self.assertTrue(receive_then_disconnect_server.STOPPED)



if __name__ == '__main__':
    unittest.main()
