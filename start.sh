#!/usr/bin/env bash

npm -dd run build

./venv/bin/python server.py
