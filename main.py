import socket
import json
import time

from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont

MARSTEK_IP = "192.168.10.141"   # pas aan naar jouw toestel
PORT = 30000

# JSON request (status batterij)
payload_1 = {
    "id": 1,
    "method": "Bat.GetStatus",
    "params": {"id": 0}
}

# JSON request (status batterij)
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

def update_display(data):
    serial = i2c(port=1, address=0x3C)
    device = ssd1306(serial)

    image = Image.new("1", (device.width, device.height))
    draw = ImageDraw.Draw(image)

    # veilige data extractie
    soc = data.get("soc", data.get("bat_soc", 0))
    temp = data.get("bat_temp", 0)
    cap = data.get("bat_capacity", data.get("bat_cap", 0))
    offgrid = data.get("offgrid_power", 0)

    # formatting
    cap_kwh = cap / 1000

    # layout (4 regels netjes verdeeld)
    draw.text((0, 0),  f"SOC: {soc}%", fill=255)
    draw.text((0, 16), f"Temp: {temp}C", fill=255)
    draw.text((0, 32), f"Cap: {cap_kwh:.2f} kWh", fill=255)
    draw.text((0, 48), f"Offgrid: {offgrid}W", fill=255)

    device.display(image)

update_display.last = None

while 1:
    time.sleep(10)

    combined = {}

    try:
        part_1 = retrieve_info(payload_1)
        if part_1 and "result" in part_1:
            combined.update(part_1["result"])
    except Exception as e:
        print(f"part_1 failed: {e}")

    try:
        part_2 = retrieve_info(payload_2)
        if part_2 and "result" in part_2:
            combined.update(part_2["result"])
    except Exception as e:
        print(f"part_2 failed: {e}")

    # veilige prints
    try:
        print(part_1, part_2)
        print(combined.get("soc"))
        # print(combined.get("bat_temp"))
        # print((combined.get("bat_capacity") or 0) / 1000)
        # print(combined.get("offgrid_power"))
        if update_display.last != combined:
            update_display.last = combined
            update_display(combined)
    except Exception as e:
        print(f"print failed: {e}")