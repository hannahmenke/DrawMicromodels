#!/usr/bin/env bash
set -e

apt-get update
apt-get install -y python3-numpy python3-matplotlib python3-h5py

pip install --no-cache-dir numpy matplotlib h5py
