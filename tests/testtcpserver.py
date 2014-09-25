#!/usr/bin/env python
#
#  python-unittest-skeleton helper which allows for creating TCP
#  servers that misbehave in certain ways, for testing code.
#
#===============
#  This is based on a skeleton test file, more information at:
#
#     https://github.com/linsomniac/python-unittest-skeleton

import sys
import threading

PY3 = sys.version > '3'


class FakeTCPServer:
    '''A simple socket server so that specific error conditions can be tested.
    This must be subclassed and implment the "server()" method.

    The server() method would be implemented to do :py:func:`socket.send` and
    :py:func:`socket.recv` calls to communicate with the client process.
    '''

    GROUP = 'fakeTestTCPServer'

    STOPPED = False

    def _perConn(self, count):
        connection, addr = self.s.accept()
        print('FTCP accepted %s' % str(addr))
        self.server(self.s, connection, count)
        count += 1

    def __init__(self):
        import socket

        def _setup(self, evt):

            FakeTCPServer.STOPPED = False

            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.settimeout(5)
            self.s.bind(('127.0.0.1', 2222))
            self.s.listen(1)
            self.port = self.s.getsockname()[1]

            print('setup port %s'%self.port)
            count = 0
            evt.set()
            while not self.STOPPED:
                self._perConn(count)
            print('setup OUT')
            #self.s.shutdown(socket.SHUT_RDWR)
            self.s.close()

        while [t for t in threading.enumerate() if t.name == self.GROUP]:
            pass
        evt = threading.Event()
        thd = threading.Thread(name=self.GROUP, target=lambda: _setup(self, evt))
        thd.start()
        evt.wait()

    def server(self, sock, conn, ct):
        raise NotImplementedError('implement .server method')


RECEIVE = None          # instruct the server to read data
STOP_SERVER = (None, None)


class CommandServer(FakeTCPServer):
    '''A convenience class that allows you to specify a set of TCP
    interactions that will be performed, providing a generic "server()"
    method for FakeTCPServer().

    For example, if you want to test what happens when your code sends some
    data, receives a "STORED" response, sends some more data and then the
    connection is closed:

    >>> fake_server = CommandServer(
    >>>     [RECEIVE, 'STORED\r\n', RECEIVE])
    >>> sc = memcached2.ServerConnection('memcached://127.0.0.1:{0}/'
    >>>         .format(fake_server.port))
    '''

    def __init__(self, commands):
        self.commands = commands
        FakeTCPServer.__init__(self)

    def server(self, sock, conn, count):
        for command in self.commands:
            if command == RECEIVE:
                conn.recv(1000)
            elif command == STOP_SERVER:
                FakeTCPServer.STOPPED = True
            else:
                if PY3:
                    conn.send(bytes(command, 'ascii'))
                else:
                    conn.send(bytes(command))
        conn.close()



class OneShotServer(CommandServer):

    def __init__(self, commands):
        self.commands = commands #[RECEIVE, command]
        FakeTCPServer.__init__(self)

    def _perConn(self, count):
        connection, addr = self.s.accept()
        print('OSS accepted %s' % str(addr))
        self.server(self.s, connection, count)
        FakeTCPServer.STOPPED = True

