#!/bin/bash
gunicorn Bot:app --bind 0.0.0.0:$PORT
