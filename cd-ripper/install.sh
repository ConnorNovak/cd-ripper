#!/bin/sh

# Check that poetry is installed
err=$(poetry --version 2>&1 >/dev/null)
if [ "$err" != "" ]; then
	echo "Poetry not installed: Installing"
	curl -sSL https://install.python-poetry.org | python3 -
	echo "PATH=\$PATH:/home/$USER/.local/bin" >> ~/.bashrc
fi

# Install bash dependencies
sudo apt install -y ffmpeg python3-mutagen

# Install project into poetry virtual environment
poetry install
