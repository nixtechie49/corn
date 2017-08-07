#!/usr/bin/env bash

npm -dd run build
echo 'npm end'
echo 'start corn...'
./venv/bin/python server.py
