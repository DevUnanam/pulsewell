#!/usr/bin/env bash

gunicorn wellness_platform.wsgi:application --bind 0.0.0.0:$PORT