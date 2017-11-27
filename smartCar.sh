#!/bin/bash

#Inititalize bluetooth connection to OBD scanner
sudo modprobe rfcomm
sudo rfcomm bind rfcomm0 00:1D:A5:1B:66:74

#Run Smart Car system
python smartCar.py

#Run analysis
python smartCarAnalysis.py
