import csv
import socket

from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.rest import ApiException
from datetime import datetime, timezone
import os
import re
import shutil
import glob

def debug(debug_name, string):
    print(f"{debug_name} {string}")

def send_energy_system_influxdb(influxdb_server, config, debug_name, ts, dict_data):

    client = InfluxDBClient(
        url=config[influxdb_server]['url'],
        token=config[influxdb_server]['write_token'],
        org=config[influxdb_server]['org']
    )

    write_api = client.write_api(write_options=SYNCHRONOUS)

    if ts is None:
        ts = datetime.now()

    data = dict_data["result"]

    point = (
        Point("energy_system")
        .time(ts)
        .tag("source", dict_data["src"])
        .field("system_id", int(data["id"]))
        .field("soc", int(data["bat_soc"]))
        .field("capacity", int(data["bat_cap"]))
        .field("pv_power", int(data["pv_power"]))
        .field("ongrid_power", int(data["ongrid_power"]))
        .field("offgrid_power", int(data["offgrid_power"]))
        .field("total_pv_energy", int(data["total_pv_energy"]))
        .field("total_grid_output_energy", int(data["total_grid_output_energy"]))
        .field("total_grid_input_energy", int(data["total_grid_input_energy"]))
        .field("total_load_energy", int(data["total_load_energy"]))
    )

    try:
        write_api.write(
            bucket=config[influxdb_server]['bucket'],
            org=config[influxdb_server]['org'],
            record=point
        )
        debug(debug_name, "✓ Energy system data sent.")
    except Exception as e:
        debug(debug_name, f"[Warning] Could not write energy system to InfluxDB: {e}")
        client.close()
        return False

    client.close()
    return True

# def send_energy_system_status_influxdb(influxdb_server, config, debug_name, ts, dict_data):

#     client = InfluxDBClient(url=config[influxdb_server]['url'], token=config[influxdb_server]['write_token'], org=config[influxdb_server]['org'])

#     write_api = client.write_api(write_options=SYNCHRONOUS)

#     # Timestamp
#     ts = datetime.now()

#     center = int(dict_data["center"])
#     span = int(dict_data["span"])

#     # Create point
#     point = (
#         Point("vna_configuration")
#         .time(ts)
#         .tag("radar", config['fixed_configurations']['radar_name'])
#         .field("center", int(dict_data["center"]))
#         .field("span", int(dict_data["span"]))
#         .field("start", int(center - span // 2))
#         .field("stop", int(center + span // 2))
#         .field("power", int(dict_data["power"]))
#         .field("sweeps", int(dict_data["sweeps"]))
#         .field("points", int(dict_data["points"]))
#         .field("ifbw", int(dict_data["ifbw"]))
#         .field("parameter", int(dict_data["parameter"][1:]))
#     )

#     # Write data in batch
#     try:
#         write_api.write(bucket=config[influxdb_server]['bucket'], org=config[influxdb_server]['org'], record=point)
#         debug(debug_name, f"✓ Configuration data sended.")
#     except Exception as e:
#         debug(debug_name, f"[Warning] Could not write to InfluxDB: {e}")
#         client.close()
#         return False

#     client.close()

#     return True


def send_battery_status_influxdb(influxdb_server, config, debug_name, ts, dict_data):

    client = InfluxDBClient(
        url=config[influxdb_server]['url'],
        token=config[influxdb_server]['write_token'],
        org=config[influxdb_server]['org']
    )

    write_api = client.write_api(write_options=SYNCHRONOUS)

    # Gebruik meegegeven timestamp of huidige tijd
    if ts is None:
        ts = datetime.now()

    battery = dict_data["result"]

    point = (
        Point("battery")
        .time(ts)
        .tag("source", dict_data["src"])
        .field("battery_id", int(battery["id"]))
        .field("soc", int(battery["soc"]))
        .field("charge_flag", int(battery["charg_flag"]))
        .field("discharge_flag", int(battery["dischrg_flag"]))
        .field("temperature", float(battery["bat_temp"]))
        .field("capacity", float(battery["bat_capacity"]))
        .field("rated_capacity", float(battery["rated_capacity"]))
    )

    try:
        write_api.write(
            bucket=config[influxdb_server]['bucket'],
            org=config[influxdb_server]['org'],
            record=point
        )
        debug(debug_name, "✓ Battery data sent.")
    except Exception as e:
        debug(debug_name, f"[Warning] Could not write to InfluxDB: {e}")
        client.close()
        return False

    client.close()
    return True

# def send_battery_status_influxdb(influxdb_server, config, debug_name, ts, dict_data):

#     client = InfluxDBClient(url=config[influxdb_server]['url'], token=config[influxdb_server]['write_token'], org=config[influxdb_server]['org'])

#     write_api = client.write_api(write_options=SYNCHRONOUS)

#     # Timestamp
#     ts = datetime.now()

#     center = int(dict_data["center"])
#     span = int(dict_data["span"])

#     # Create point
#     point = (
#         Point("vna_configuration")
#         .time(ts)
#         .tag("radar", config['fixed_configurations']['radar_name'])
#         .field("center", int(dict_data["center"]))
#         .field("span", int(dict_data["span"]))
#         .field("start", int(center - span // 2))
#         .field("stop", int(center + span // 2))
#         .field("power", int(dict_data["power"]))
#         .field("sweeps", int(dict_data["sweeps"]))
#         .field("points", int(dict_data["points"]))
#         .field("ifbw", int(dict_data["ifbw"]))
#         .field("parameter", int(dict_data["parameter"][1:]))
#     )

#     # Write data in batch
#     try:
#         write_api.write(bucket=config[influxdb_server]['bucket'], org=config[influxdb_server]['org'], record=point)
#         debug(debug_name, f"✓ Configuration data sended.")
#     except Exception as e:
#         debug(debug_name, f"[Warning] Could not write to InfluxDB: {e}")
#         client.close()
#         return False

#     client.close()

#     return True

