Python Embedded Test Server
========================

"faketcpserver.py" has code to create a fake TCP server which you can
provide a script to emulate certain send/receive/hangup behavior, to
simulate a TCP server that misbehaves or disconnects.  Examples are in

Usage
======


The server runs in it's own thread, and is very lightweight, so you can spin one up for
each distinct unit test.

    from embeddedserver import CommandServer, RECEIVE
    
    # create server
    srvr = CommandServer([RECEIVE, 'hello world'])
    
    # run client
    r = requests.get('http://localhost:%s/hello' % srvr.port)
    assert 'hello world' in r.text
    
    srvr.close()
    
    
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
  
  