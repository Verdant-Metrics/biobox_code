import network
import time
import webrepl

# Replace with your network credentials
SSID = 'Stew_wifi'
PASSWORD = 'badbitchesonly'

def connect_wifi():
    print('started')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(SSID, PASSWORD)
        timeout = 15  # seconds
        for _ in range(timeout):
            if wlan.isconnected():
                break
            time.sleep(1)
    if wlan.isconnected():
        print("✅ Connected:", wlan.ifconfig())
    else:
        print("⚠️ Failed to connect.")

def main():
    time.sleep(5)
    connect_wifi()
    webrepl.start()
    print("🌐 WebREPL started.")

main()