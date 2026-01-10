#!/bin/bash
set -e

DATASET_PORT = 8001

echo "\nStarting dataset HTTP server on ${DATASET_PORT}..."
python3 -m http.server ${DATASET_PORT} --directory /label-studio/data/dataset
echo "Dataset HTTP server started!\n"