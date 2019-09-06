#!/bin/bash

#wget https://github.com/leonardt/fault/archive/2e80fa9eb445d144e906d0c8071d17128aa4518f.zip
#unzip 2e80fa9eb445d144e906d0c8071d17128aa4518f.zip
#cd fault-2e80fa9eb445d144e906d0c8071d17128aa4518f
git clone git@github.com:leonardt/fault.git
cd fault
pip install -e .
cd ..
#rm 2e80fa9eb445d144e906d0c8071d17128aa4518f.zip

