#!/bin/sh

gunicorn --config gunicorn.conf.py falcon_reversi:api -D
