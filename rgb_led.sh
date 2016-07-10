#!/bin/sh

FIFO=led.fifo

case $1 in
    ("BLACK")
        echo "000" > $FIFO ;;
    ("BLUE")
        echo "001" > $FIFO ;;
    ("GREEN")
        echo "010" > $FIFO ;;
    ("CYAN")
        echo "011" > $FIFO ;;
    ("RED")
        echo "100" > $FIFO ;;
    ("MAGENTA")
        echo "101" > $FIFO ;;
    ("YELLOW")
        echo "110" > $FIFO ;;
    ("WHITE")
        echo "111" > $FIFO ;;
    (*)
        echo "Invalid input argument!" ;;
esac
