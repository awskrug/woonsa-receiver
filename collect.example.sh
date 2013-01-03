#!/bin/bash
W_ID=hello
W_HOST=localhost
W_PORT=12114
FI_NAME=woonsa.fifo
M_COUNT=10
M_TARGET=gae9.com
M_OPTS="--split -c $M_COUNT"
M_BIN=/usr/local/sbin/mtr

mkfifo $FI_NAME
nc $W_HOST $W_PORT < $FI_NAME | ( echo $W_ID > $FI_NAME; $M_BIN $M_OPTS $M_TARGET > $FI_NAME )
rm -rf $FI_NAME
