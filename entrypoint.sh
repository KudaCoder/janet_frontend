#!/usr/bin/env bash

cd src
flask db upgrade
python app.py
