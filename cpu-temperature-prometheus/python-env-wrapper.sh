#!/bin/bash
source /home/andrew/bin/miniconda3/etc/profile.d/conda.sh
conda activate python3-prometheus
python -u /home/andrew/src/observe-custom-metrics/cpu-temperature-prometheus/cpu-temperature.py
