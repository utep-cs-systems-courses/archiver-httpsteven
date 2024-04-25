#! /usr/bin/env bash     

TARPGM=../mytar.py
rm foogoo.tar
rm -rf dst
mkdir dst
(cd src; $TARPGM o c ../foogoo.tar foo.txt goo.gif)

(cd dst; $TARPGM o x ../foogoo.tar)
if diff -r src dst
then
    echo "success outband" >&2		# error msg to stdout
    rm -rf dst			# clean up
else
    echo "failure" >&2
    exit 1			# return failure
fi    
rm foogoo.tar
rm -rf dst
mkdir dst
(cd src; $TARPGM i c ../foogoo.tar foo.txt goo.gif)

(cd dst; $TARPGM i x ../foogoo.tar)
if diff -r src dst
then
    echo "success inband" >&2		# error msg to stdout
    rm -rf dst			# clean up
    exit 0			# return success
else
    echo "failure" >&2
    exit 1			# return failure
fi
