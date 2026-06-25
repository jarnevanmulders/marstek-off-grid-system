import socket
import json
import time

import RPi.GPIO as GPIO
import time

from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont

from influxdb import *
from configuration import *

# BCM pinnummering gebruiken
GPIO.setmode(GPIO.BCM)

PV_RELAY_PIN = 24
LOAD_RELAY_PIN = 25

soc = None

output_pv = False
output_load = False

GPIO.setup(PV_RELAY_PIN, GPIO.OUT)
GPIO.setup(LOAD_RELAY_PIN, GPIO.OUT)

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

MARSTEK_IP = "192.168.10.141"   # pas aan naar jouw toestel
PORT = 30000

# JSON request (status Battery)
payload_1 = {
    "id": 1,
    "method": "Bat.GetStatus",
    "params": {"id": 0}
}

# JSON request (status Energy System)
payload_2 = {
    "id": 2,
    "method": "ES.GetStatus",
    "params": {"id": 0}
}


def retrieve_info(payload):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2)

    try:
        # stuur request
        sock.sendto(json.dumps(payload).encode(), (MARSTEK_IP, PORT))

        # ontvang response
        data, addr = sock.recvfrom(4096)

        response = json.loads(data.decode())
        return response
        # print("Response:", response)

    except socket.timeout:
        print("Geen antwoord (timeout)")
        return None

    finally:
        sock.close()

heartbeat = False


def update_display(data, counter):

    global heartbeat

    image = Image.new("1", (device.width, device.height))
    draw = ImageDraw.Draw(image)

    # veilige data extractie
    soc = data.get("soc", data.get("bat_soc", 0))
    temp = data.get("bat_temp", 0)
    cap = data.get("bat_capacity", data.get("bat_cap", 0))
    offgrid = data.get("offgrid_power", 0)

    # formatting
    cap_kwh = cap / 1000
    
    # if offgrid > 32767:
    #     offgrid -= 65536

    # layout (4 regels netjes verdeeld)
    draw.text((0, 0),  f"SOC: {soc}%", fill=255)
    draw.text((0, 16), f"Temp: {temp}C", fill=255)
    draw.text((0, 32), f"Cap: {cap_kwh:.2f} kWh", fill=255)
    draw.text((0, 48), f"Offgrid: {offgrid}W", fill=255)

    heartbeat = not heartbeat

    if heartbeat:
        draw.rectangle((120, 0, 127, 7), fill=255)
        draw.text((120, 10), f"{counter}", fill=255)

    device.display(image)

update_display.last = None

def update_relay(pin, state):
    try:
        if state:
            GPIO.output(pin, GPIO.HIGH)
        else:
            GPIO.output(pin, GPIO.LOW)

    except KeyboardInterrupt:
        pass

    # finally:
    #     GPIO.cleanup()

def update_relays():
    update_relay(PV_RELAY_PIN, output_pv)
    time.sleep(0.5)
    update_relay(LOAD_RELAY_PIN, output_load)
    
combined = {}

counter = 29

last_output_pv = False
last_output_load = False

config = retrieve_yaml_file()

try:
    while 1:
        time.sleep(1)

        counter = counter + 1

        if counter > 30:
            counter = 0

            try:
                part_1 = retrieve_info(payload_1)
                if part_1 and "result" in part_1:
                    combined.update(part_1["result"])

                    send_battery_status_influxdb("influxdb_local", config, "Battery", None, part_1)

            except Exception as e:
                print(f"part_1 failed: {e}")

            try:
                part_2 = retrieve_info(payload_2)
                if part_2 and "result" in part_2:
                    combined.update(part_2["result"])

                    # check offgrid power
                    offgrid = part_2.get("offgrid_power", 0)
                    if offgrid > 32767:
                        offgrid -= 65536
                    part_1["offgrid_power"] = offgrid

                    send_energy_system_influxdb("influxdb_local", config, "Energy System", None, part_2)

            except Exception as e:
                print(f"part_2 failed: {e}")

            if soc != None:
                soc = combined.get("soc")

                # Check SoC and determine load and pv relay
                if output_pv and soc >= 99:
                    output_pv = False
                elif not output_pv and soc <= 90:
                    output_pv = True

                # Load hysterese
                if output_load and soc <= 30:
                    output_load = False
                elif not output_load and soc >= 40:
                    output_load = True
                
            print(output_pv, output_load)


            # Update relays
            if output_pv != last_output_pv or output_load != last_output_load:
                update_relays()

                last_output_pv = output_pv
                last_output_load = output_load

        # veilige prints
        try:
            # print(part_1, part_2)

            soc = combined.get("soc")

            print(f"SOC: {soc}")
            # print(combined.get("bat_temp"))
            # print((combined.get("bat_capacity") or 0) / 1000)
            # print(combined.get("offgrid_power"))
            # if update_display.last != combined:
            #     update_display.last = combined
            print(counter)
            update_display(combined, counter)
        except Exception as e:
            print(f"print failed: {e}")

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
