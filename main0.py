import socket
import json

MARSTEK_IP = "192.168.10.141"   # pas aan naar jouw toestel
PORT = 30000

# JSON request (status batterij)
payload = {
    "id": 0,
    "method": "Marstek.GetStatus",
    "params":{"ble_mac":"0"}
}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)

try:
    # stuur request
    sock.sendto(json.dumps(payload).encode(), (MARSTEK_IP, PORT))

    # ontvang response
    data, addr = sock.recvfrom(4096)

    response = json.loads(data.decode())
    print("Response:", response)

except socket.timeout:
    print("Geen antwoord (timeout)")

finally:
    sock.close()