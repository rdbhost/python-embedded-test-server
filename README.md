Python Unittest Skeleton
========================

This is a skeleton Python unittest file to allow it to be grabbed and
filled in, instead of having to remember the structure.

The "test_faketcpserver.py" includes sample code which uses the
faketcpserver module, mentioned below, to test code reaction to
misbehaving TCP servers.

"faketcpserver.py" has code to create a fake TCP server which you can
provide a script to emulate certain send/receive/hangup behavior, to
simulate a TCP server that misbehaes or disconnects.  Examples are in
"test_skeleton.py".

Usage
-----

To use:

  * Check out repository.

  * Copy "tests/test_skeleton.py" into your "test" directory.

  * Rename "test_skeleton.py" to something more descriptive.  (Note: It
    should keep the "test_" prefix, so that "make" will run the tests).

  * Edit this file and search for "XXX".

  * Copy "Makefile" into your tests directory.  It should work without
    modification.

  * If you are doing bootle web development, copy "test_bottle.py" into
    your "tests" directory and rename it to something more useful.

  * If you have a CLI program, use the "cli_skeleton" in the top level
    directory instead.
