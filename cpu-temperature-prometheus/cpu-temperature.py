#!/usr/bin/env python3

import json
import time
import subprocess
import requests
import datetime
from prometheus_client import start_http_server, Gauge

debug = False
sleep_time_seconds = 30
prometheus_scrape_port = 9092
sensors = ["/usr/bin/sensors", "-f", "-j"]

g_temp     = Gauge('cpu_temperature',             'CPU Temperature',                 ['isa_adapter', 'core'])
g_max      = Gauge('cpu_temperature_max',         'CPU Temperature Maximum',         ['isa_adapter', 'core'])
g_temp_pkg = Gauge('cpu_package_temperature',     'CPU Package Temperature',         ['isa_adapter'])
g_max_pkg  = Gauge('cpu_package_temperature_max', 'CPU Package Temperature Maximum', ['isa_adapter'])

def process(package_name, package_id, data):

    fidx = 1
    isa = data[package_name]
    package = isa["Package id " + str(package_id)]
    package_temp_input = package["temp" + str(fidx) + "_input"]
    package_temp_max   = package["temp" + str(fidx) + "_max"]

    if debug:
        print("🌭🌭🌭🌭🌭")
        print("package: " + package_name + " temp input: " + str(package_temp_input))
        print("package: " + package_name + " temp max: "   + str(package_temp_max))

    try:
        g_temp_pkg.labels(isa_adapter=package_name).set(package_temp_input)
        g_max_pkg.labels(isa_adapter=package_name).set(package_temp_max)
    except Exception as e:
        print(e)

    for i in range(14):
        try:
            core = isa["Core " + str(i)]
            temp_input = core["temp" + str(fidx + 1) + "_input"]
            temp_max   = core["temp" + str(fidx + 1) + "_max"]

            if debug:
                print(core)
                print("temp" + str(fidx + 1) + "_input: " + str(temp_input))
                print("temp" + str(fidx + 1) + "_max: "   + str(temp_max))

            fidx += 1
        except Exception as e:
            # expect to fail here as the core numbers are not sequential
            continue

        try:
            g_temp.labels(isa_adapter=package_name, core="core " + str(i)).set(temp_input)
            g_max.labels(isa_adapter=package_name, core="core " + str(i)).set(temp_max)
        except Exception as e:
            print(e)

    return

def main():

    while True:
        p = subprocess.Popen(sensors, stdout=subprocess.PIPE, universal_newlines=True)
        out = p.stdout.read()
        data = json.loads(out)

        process("coretemp-isa-0000", 0, data)
        process("coretemp-isa-0001", 1, data)

        time.sleep(sleep_time_seconds)


if __name__=="__main__":
    start_http_server(prometheus_scrape_port)
    main()

