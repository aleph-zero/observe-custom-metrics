#!/bin/bash
source /home/andrew/bin/miniconda3/etc/profile.d/conda.sh
conda activate python3-opentelemetry
python -u /home/andrew/src/observe-custom-metrics/cpu-temperature-otel/cpu-temperature.py
