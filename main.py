import socket
import json
import time

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


while 1:
    time.sleep(1)

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
        print(combined.get("soc"))
        print(combined.get("bat_temp"))
        print((combined.get("bat_capacity") or 0) / 1000)
        print(combined.get("offgrid_power"))
    except Exception as e:
        print(f"print failed: {e}")