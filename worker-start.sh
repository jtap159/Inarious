#! /usr/bin/env bash
set -e

celery -A worker worker -l info -Q main-queue -c 1
