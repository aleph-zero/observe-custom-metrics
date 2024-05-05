#!/usr/bin/env python3

import socket
import json
import time
import subprocess
import requests
import datetime
from typing import Iterable

from opentelemetry.sdk.resources import Resource
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
        ConsoleMetricExporter,
        PeriodicExportingMetricReader,
)
from opentelemetry.metrics import CallbackOptions, Observation
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from local_machine_resource_detector import LocalMachineResourceDetector

debug = False
sleep_time_seconds = 30
prometheus_scrape_port = 9092
sensors = ["/usr/bin/sensors", "-f", "-j"]

local_resource = LocalMachineResourceDetector().detect()

resource = local_resource.merge(
            Resource.create({
                "service.name": "cpu-temperature-monitor",
                "service.version": "0.1",}
                )
            )

reader = PeriodicExportingMetricReader(OTLPMetricExporter(), export_interval_millis=30000)
provider = MeterProvider(resource=resource, metric_readers=[reader])

metrics.set_meter_provider(provider)
meter = metrics.get_meter(name="cpu-package-temperature", version="0.1")

class TemperatureReading:
    def __init__(self, attributes):
        self.attributes = attributes

    def set_temperature(self, i):
        self.temperature = i

    def get_temperature(self):
        return self.temperature

def process(tr, tr_max, core_temp_inputs, package_name, package_id, data):

    fidx = 1
    isa = data[package_name]
    package = isa["Package id " + str(package_id)]
    package_temp_input = package["temp" + str(fidx) + "_input"]
    package_temp_max   = package["temp" + str(fidx) + "_max"]

    if debug:
        print("🌭🌭🌭🌭🌭")
        print("package: " + package_name + " temp input: " + str(package_temp_input))
        print("package: " + package_name + " temp max: "   + str(package_temp_max))

    tr.set_temperature(package_temp_input)
    tr_max.set_temperature(package_temp_max)

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
            corestr = "core " + str(i)
            core_temp_inputs[corestr].set_temperature(temp_input)
        except Exception as e:
            # expect to fail here as the core numbers are not sequential
            continue
    return


pkg0_core0_tr0  = TemperatureReading({"isa_adapter": "coretemp-isa-0000", "core": "core 0"})
pkg0_core1_tr0  = TemperatureReading({"isa_adapter": "coretemp-isa-0000", "core": "core 1"})
pkg0_core2_tr0  = TemperatureReading({"isa_adapter": "coretemp-isa-0000", "core": "core 2"})
pkg0_core3_tr0  = TemperatureReading({"isa_adapter": "coretemp-isa-0000", "core": "core 3"})
pkg0_core4_tr0  = TemperatureReading({"isa_adapter": "coretemp-isa-0000", "core": "core 4"})
pkg0_core5_tr0  = TemperatureReading({"isa_adapter": "coretemp-isa-0000", "core": "core 5"})
pkg0_core8_tr0  = TemperatureReading({"isa_adapter": "coretemp-isa-0000", "core": "core 8"})
pkg0_core9_tr0  = TemperatureReading({"isa_adapter": "coretemp-isa-0000", "core": "core 9"})
pkg0_core10_tr0 = TemperatureReading({"isa_adapter": "coretemp-isa-0000", "core": "core 10"})
pkg0_core11_tr0 = TemperatureReading({"isa_adapter": "coretemp-isa-0000", "core": "core 11"})
pkg0_core12_tr0 = TemperatureReading({"isa_adapter": "coretemp-isa-0000", "core": "core 12"})
pkg0_core13_tr0 = TemperatureReading({"isa_adapter": "coretemp-isa-0000", "core": "core 13"})

pkg0_core_temp_inputs = {}
pkg0_core_temp_inputs["core 0"]  = pkg0_core0_tr0
pkg0_core_temp_inputs["core 1"]  = pkg0_core1_tr0
pkg0_core_temp_inputs["core 2"]  = pkg0_core2_tr0
pkg0_core_temp_inputs["core 3"]  = pkg0_core3_tr0
pkg0_core_temp_inputs["core 4"]  = pkg0_core4_tr0
pkg0_core_temp_inputs["core 5"]  = pkg0_core5_tr0
pkg0_core_temp_inputs["core 8"]  = pkg0_core8_tr0
pkg0_core_temp_inputs["core 9"]  = pkg0_core9_tr0
pkg0_core_temp_inputs["core 10"] = pkg0_core10_tr0
pkg0_core_temp_inputs["core 11"] = pkg0_core11_tr0
pkg0_core_temp_inputs["core 12"] = pkg0_core12_tr0
pkg0_core_temp_inputs["core 13"] = pkg0_core13_tr0

def observable_gauge_pkg0_core0(options):
    yield metrics.Observation(pkg0_core0_tr0.get_temperature(), pkg0_core0_tr0.attributes)
def observable_gauge_pkg0_core1(options):
    yield metrics.Observation(pkg0_core1_tr0.get_temperature(), pkg0_core1_tr0.attributes)
def observable_gauge_pkg0_core2(options):
    yield metrics.Observation(pkg0_core2_tr0.get_temperature(), pkg0_core2_tr0.attributes)
def observable_gauge_pkg0_core3(options):
    yield metrics.Observation(pkg0_core3_tr0.get_temperature(), pkg0_core3_tr0.attributes)
def observable_gauge_pkg0_core4(options):
    yield metrics.Observation(pkg0_core4_tr0.get_temperature(), pkg0_core4_tr0.attributes)
def observable_gauge_pkg0_core5(options):
    yield metrics.Observation(pkg0_core5_tr0.get_temperature(), pkg0_core5_tr0.attributes)
def observable_gauge_pkg0_core8(options):
    yield metrics.Observation(pkg0_core8_tr0.get_temperature(), pkg0_core8_tr0.attributes)
def observable_gauge_pkg0_core9(options):
    yield metrics.Observation(pkg0_core9_tr0.get_temperature(), pkg0_core9_tr0.attributes)
def observable_gauge_pkg0_core10(options):
    yield metrics.Observation(pkg0_core10_tr0.get_temperature(), pkg0_core10_tr0.attributes)
def observable_gauge_pkg0_core11(options):
    yield metrics.Observation(pkg0_core11_tr0.get_temperature(), pkg0_core11_tr0.attributes)
def observable_gauge_pkg0_core12(options):
    yield metrics.Observation(pkg0_core12_tr0.get_temperature(), pkg0_core12_tr0.attributes)
def observable_gauge_pkg0_core13(options):
    yield metrics.Observation(pkg0_core13_tr0.get_temperature(), pkg0_core13_tr0.attributes)

pkg1_core0_tr0  = TemperatureReading({"isa_adapter": "coretemp-isa-0001", "core": "core 0"})
pkg1_core1_tr0  = TemperatureReading({"isa_adapter": "coretemp-isa-0001", "core": "core 1"})
pkg1_core2_tr0  = TemperatureReading({"isa_adapter": "coretemp-isa-0001", "core": "core 2"})
pkg1_core3_tr0  = TemperatureReading({"isa_adapter": "coretemp-isa-0001", "core": "core 3"})
pkg1_core4_tr0  = TemperatureReading({"isa_adapter": "coretemp-isa-0001", "core": "core 4"})
pkg1_core5_tr0  = TemperatureReading({"isa_adapter": "coretemp-isa-0001", "core": "core 5"})
pkg1_core8_tr0  = TemperatureReading({"isa_adapter": "coretemp-isa-0001", "core": "core 8"})
pkg1_core9_tr0  = TemperatureReading({"isa_adapter": "coretemp-isa-0001", "core": "core 9"})
pkg1_core10_tr0 = TemperatureReading({"isa_adapter": "coretemp-isa-0001", "core": "core 10"})
pkg1_core11_tr0 = TemperatureReading({"isa_adapter": "coretemp-isa-0001", "core": "core 11"})
pkg1_core12_tr0 = TemperatureReading({"isa_adapter": "coretemp-isa-0001", "core": "core 12"})
pkg1_core13_tr0 = TemperatureReading({"isa_adapter": "coretemp-isa-0001", "core": "core 13"})

pkg1_core_temp_inputs = {}
pkg1_core_temp_inputs["core 0"]  = pkg1_core0_tr0
pkg1_core_temp_inputs["core 1"]  = pkg1_core1_tr0
pkg1_core_temp_inputs["core 2"]  = pkg1_core2_tr0
pkg1_core_temp_inputs["core 3"]  = pkg1_core3_tr0
pkg1_core_temp_inputs["core 4"]  = pkg1_core4_tr0
pkg1_core_temp_inputs["core 5"]  = pkg1_core5_tr0
pkg1_core_temp_inputs["core 8"]  = pkg1_core8_tr0
pkg1_core_temp_inputs["core 9"]  = pkg1_core9_tr0
pkg1_core_temp_inputs["core 10"] = pkg1_core10_tr0
pkg1_core_temp_inputs["core 11"] = pkg1_core11_tr0
pkg1_core_temp_inputs["core 12"] = pkg1_core12_tr0
pkg1_core_temp_inputs["core 13"] = pkg1_core13_tr0

def observable_gauge_pkg1_core0(options):
    yield metrics.Observation(pkg1_core0_tr0.get_temperature(), pkg1_core0_tr0.attributes)
def observable_gauge_pkg1_core1(options):
    yield metrics.Observation(pkg1_core1_tr0.get_temperature(), pkg1_core1_tr0.attributes)
def observable_gauge_pkg1_core2(options):
    yield metrics.Observation(pkg1_core2_tr0.get_temperature(), pkg1_core2_tr0.attributes)
def observable_gauge_pkg1_core3(options):
    yield metrics.Observation(pkg1_core3_tr0.get_temperature(), pkg1_core3_tr0.attributes)
def observable_gauge_pkg1_core4(options):
    yield metrics.Observation(pkg1_core4_tr0.get_temperature(), pkg1_core4_tr0.attributes)
def observable_gauge_pkg1_core5(options):
    yield metrics.Observation(pkg1_core5_tr0.get_temperature(), pkg1_core5_tr0.attributes)
def observable_gauge_pkg1_core8(options):
    yield metrics.Observation(pkg1_core8_tr0.get_temperature(), pkg1_core8_tr0.attributes)
def observable_gauge_pkg1_core9(options):
    yield metrics.Observation(pkg1_core9_tr0.get_temperature(), pkg1_core9_tr0.attributes)
def observable_gauge_pkg1_core10(options):
    yield metrics.Observation(pkg1_core10_tr0.get_temperature(), pkg1_core10_tr0.attributes)
def observable_gauge_pkg1_core11(options):
    yield metrics.Observation(pkg1_core11_tr0.get_temperature(), pkg1_core11_tr0.attributes)
def observable_gauge_pkg1_core12(options):
    yield metrics.Observation(pkg1_core12_tr0.get_temperature(), pkg1_core12_tr0.attributes)
def observable_gauge_pkg1_core13(options):
    yield metrics.Observation(pkg1_core13_tr0.get_temperature(), pkg1_core13_tr0.attributes)


pkg_tr0     = TemperatureReading({"isa_adapter": "coretemp-isa-0000"})
pkg_tr0_max = TemperatureReading({"isa_adapter": "coretemp-isa-0000"})
pkg_tr1     = TemperatureReading({"isa_adapter": "coretemp-isa-0001"})
pkg_tr1_max = TemperatureReading({"isa_adapter": "coretemp-isa-0001"})

def observable_gauge_tr0(options):
    yield metrics.Observation(pkg_tr0.get_temperature(), pkg_tr0.attributes)

def observable_gauge_tr0_max(options):
    yield metrics.Observation(pkg_tr0_max.get_temperature(), pkg_tr0_max.attributes)

def observable_gauge_tr1(options):
    yield metrics.Observation(pkg_tr1.get_temperature(), pkg_tr1.attributes)

def observable_gauge_tr1_max(options):
    yield metrics.Observation(pkg_tr1_max.get_temperature(), pkg_tr1_max.attributes)

def main():

    g = meter.create_observable_gauge(
            name="cpu_package_temperature", 
            unit="degF",
            description="CPU Package Temperature",
            callbacks=[observable_gauge_tr0, observable_gauge_tr1])

    g = meter.create_observable_gauge(
            name="cpu_package_temperature_max", 
            unit="degF",
            description="CPU Package Temperature",
            callbacks=[observable_gauge_tr0_max, observable_gauge_tr1_max])

    g = meter.create_observable_gauge(
            name="cpu_temperature", 
            unit="degF",
            description="CPU Core Temperature",
            callbacks=[
                observable_gauge_pkg0_core0, 
                observable_gauge_pkg0_core1,
                observable_gauge_pkg0_core2,
                observable_gauge_pkg0_core3,
                observable_gauge_pkg0_core4,
                observable_gauge_pkg0_core5,
                observable_gauge_pkg0_core8,
                observable_gauge_pkg0_core9,
                observable_gauge_pkg0_core10,
                observable_gauge_pkg0_core11,
                observable_gauge_pkg0_core12,
                observable_gauge_pkg0_core13,

                observable_gauge_pkg1_core0, 
                observable_gauge_pkg1_core1,
                observable_gauge_pkg1_core2,
                observable_gauge_pkg1_core3,
                observable_gauge_pkg1_core4,
                observable_gauge_pkg1_core5,
                observable_gauge_pkg1_core8,
                observable_gauge_pkg1_core9,
                observable_gauge_pkg1_core10,
                observable_gauge_pkg1_core11,
                observable_gauge_pkg1_core12,
                observable_gauge_pkg1_core13
            ])

    while True:
        p = subprocess.Popen(sensors, stdout=subprocess.PIPE, universal_newlines=True)
        out = p.stdout.read()
        data = json.loads(out)

        process(pkg_tr0, pkg_tr0_max, pkg0_core_temp_inputs, "coretemp-isa-0000", 0, data)
        process(pkg_tr1, pkg_tr1_max, pkg1_core_temp_inputs, "coretemp-isa-0001", 1, data)

        time.sleep(sleep_time_seconds)


if __name__=="__main__":
    main()

