Python Embedded Test Server
========================

"embeddedserver.py" has code to create a fake TCP server which you can
provide a script to emulate certain send/receive/hangup behavior, to
simulate a TCP server that misbehaves or disconnects.  

Based on linsomniac's python-unittest-skeleton

Usage of Embedded Server
===========================


The server runs in it's own thread, and is very lightweight, so you can spin one up for
each distinct unit test.

    from embeddedserver import CommandServer, RECEIVE
    
    # create server
    srvr = CommandServer([RECEIVE, 'hello world'])
    
    # run client
    r = requests.get('http://localhost:%s/hello' % srvr.port)
    assert 'hello world' in r.text
    
    srvr.stop()
    
    
The server processed the command list in order.  RECEIVE means read some bytes, and bytes or strings get sent. 
An integer means read at least that many bytes.   The CommandServer will make multiple connections (one at a time), 
and handle each of them with the same complete command sequence.


The server keeps the byte sequences received, in a .received attribute.  You can check whether what was received
was what was expected.

    # create server
    srvr = CommandServer([20, 'hello world'])
    
    r = requests.get('http://localhost:%s/hello' % srvr.port)
    
    allReceived = b''.join(srvr.received)
    assert b'GET' in allReceived
    
    
The server prints its good deeds to the console.  Provide a verbose=False parameter to constructor
to quiet it.  Passing a *str* for the command list is equivalent to \[RECEIVE, *str*].

The AsyncioCommandServer is like CommandServer, but it takes a couple of extra parameters, and provides 
the received data as a StreamReader.

    reader = asyncio.StreamReader()
    loop = asyncio.get_default_loop()
    
    srvr = AsyncioCommandServer([20, 'hello'], reader=reader, loop=loop)
    r = requests.get('http://localhost:%s/hello' % srvr.port)
    
    dataReceivedByServer = yield from reader.read()
    assert b'GET /hello' in dataReceivedByServer
    
    
 
 And lastly, the OneShotServer works like CommandServer, but quits after one client connection.
  
  
  
  
Usage of TestingSocket
===========================

This socket is for testing.  It is a true socket, and can be passed to select.select(..), or used with Asyncio, but 
it also has some features useful for testing network clients.


It tracks all data sent, and counts of send() and sendall() methods.  These are stored in 
a _data attribute.

    assert b'GET' in sock._data['data_out'], 'ok'
    assert sock._data['send_calls'] < 3, 'too many calls'
    assert sock._data['sendall_calls'] < 3, 'too many calls'
    
    
You can also simulate broken pipes or other transmission errors, with the breakOn method.  The signature
is breakOn(trigger_string, exception_to_raise)

    sock.breakOn('byte-me', OSError(errno.EPIPE, 'gotcha'))
    
The socket will raise the given error when the trigger string is found in the send() or sendall() data.



This product licensed under the MIT license.