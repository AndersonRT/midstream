#!/bin/bash

#cd 3rdparty/Robinhood
python 3rdparty/Robinhood/setup.py sdist --dist-dir=3rdparty/Robindood/dist
cp 3rdparty/Robinhood/dist/* backend/pkgs
cp 3rdparty/Robinhood/dist/* scraper/pkgs
