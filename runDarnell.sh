#!/bin/bash
/usr/bin/Xvfb :99 -screen 0 1024x768x24 &
export DISPLAY=:99
exec path/to/python3 path/to/main.py
