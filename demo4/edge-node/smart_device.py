import paho.mqtt.client as mqtt
import json
import time
import threading
import os

# --- ANSI COLOR CODES ---
# Constants for terminal GUI styling
class Colors:
    RED_ON = '\033[91m\033[1m'
    RED_OFF = '\033[31m\033[2m'
    GREEN_ON = '\033[92m\033[1m'
    GREEN_OFF = '\033[32m\033[2m'
    YELLOW_ON = '\033[93m\033[1m'
    YELLOW_OFF = '\033[33m\033[2m'
    WHITE = '\033[97m\033[1m'
    RESET = '\033[0m'
    BORDER = '\033[90m'

# --- CONFIGURATION ---
DEVICE_ID = "light-01"
# Topic to receive commands from Cloud (Cloud -> Edge)
TOPIC_SUBSCRIBE = f"$hw/events/device/{DEVICE_ID}/twin/update/document"
# Topic to report actual status to Cloud (Edge -> Cloud)
TOPIC_PUBLISH = f"$hw/events/device/{DEVICE_ID}/twin/update"

current_color = "WAITING"

# --- UI RENDERER ---
# Simulates physical hardware display using Terminal Graphics
def draw_ui(current_color):
    os.system('cls' if os.name == 'nt' else 'clear')
    c = current_color.upper()
    
    # Determine icon states based on current color
    if "RED" in c:
        r_icon, r_text = f"{Colors.RED_ON}●{Colors.RESET}", f"{Colors.RED_ON}ĐỎ  {Colors.RESET}"
    else:
        r_icon, r_text = f"{Colors.RED_OFF}○{Colors.RESET}", f"{Colors.RED_OFF}ĐỎ  {Colors.RESET}"

    if "YELLOW" in c:
        y_icon, y_text = f"{Colors.YELLOW_ON}●{Colors.RESET}", f"{Colors.YELLOW_ON}VÀNG{Colors.RESET}"
    else:
        y_icon, y_text = f"{Colors.YELLOW_OFF}○{Colors.RESET}", f"{Colors.YELLOW_OFF}VÀNG{Colors.RESET}"

    if "GREEN" in c:
        g_icon, g_text = f"{Colors.GREEN_ON}●{Colors.RESET}", f"{Colors.GREEN_ON}XANH{Colors.RESET}"
    else:
        g_icon, g_text = f"{Colors.GREEN_OFF}○{Colors.RESET}", f"{Colors.GREEN_OFF}XANH{Colors.RESET}"

    # Draw Interface Frame
    print(f"{Colors.BORDER}╔════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.BORDER}║{Colors.WHITE}         KUBEEDGE TRAFFIC LIGHT         {Colors.BORDER}║{Colors.RESET}")
    print(f"{Colors.BORDER}╠════════════════════════════════════════╣{Colors.RESET}")
    print(f"{Colors.BORDER}║                                        ║{Colors.RESET}")
    print(f"{Colors.BORDER}║            [ {r_icon} ]  {r_text}                 {Colors.BORDER}║{Colors.RESET}")
    print(f"{Colors.BORDER}║            [ {y_icon} ]  {y_text}                 {Colors.BORDER}║{Colors.RESET}")
    print(f"{Colors.BORDER}║            [ {g_icon} ]  {g_text}                 {Colors.BORDER}║{Colors.RESET}")
    print(f"{Colors.BORDER}║                                        ║{Colors.RESET}")
    print(f"{Colors.BORDER}╠════════════════════════════════════════╣{Colors.RESET}")
    
    status_text = f" TRẠNG THÁI: {c}"
    padding = 40 - len(status_text) # Dynamic padding for alignment
    print(f"{Colors.BORDER}║{Colors.WHITE}{status_text}{' ' * padding}{Colors.BORDER}║{Colors.RESET}")
    print(f"{Colors.BORDER}╚════════════════════════════════════════╝{Colors.RESET}")
    print(f"\n>>> Đang đồng bộ với Dashboard...")

# --- STATUS REPORTER (Background Thread) ---
# Periodically pushes 'actual' state to KubeEdge Core
def report_status(client):
    while True:
        try:
            # Construct KubeEdge-compliant JSON payload
            payload = {
                "event_id": str(time.time()),
                "timestamp": int(time.time() * 1000),
                "twin": {
                    "color": {
                        "actual": {"value": current_color},
                        "metadata": {"type": "string"}
                    }
                }
            }
            # Publish to local MQTT broker
            client.publish(TOPIC_PUBLISH, json.dumps(payload))
            draw_ui(current_color)
            time.sleep(3) # Sync interval: 3 seconds
        except Exception:
            pass

# --- MQTT EVENT HANDLERS ---
def on_connect(client, userdata, flags, rc):
    client.subscribe(TOPIC_SUBSCRIBE)
    # Start the reporting loop in a separate daemon thread
    threading.Thread(target=report_status, args=(client,), daemon=True).start()

def on_message(client, userdata, msg):
    global current_color
    try:
        data = json.loads(msg.payload.decode())
        # Parse 'desired' value from nested JSON structure
        twin = data.get('twin', {}).get('color', {})
        val = None
        
        # Robust parsing for different KubeEdge versions
        if 'current' in twin and 'expected' in twin['current']:
            val = twin['current']['expected']['value']
        elif 'expected' in twin:
            val = twin['expected']['value']
        elif 'desired' in twin:
            val = twin['desired']['value']
            
        if val:
            current_color = val
            # Note: UI update is handled by the report_status loop
    except:
        pass

# --- MAIN ENTRY POINT ---
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    # Connect to local MQTT Broker (Edge Node)
    client.connect("127.0.0.1", 1883, 60)
    client.loop_forever()
except:
    print("MQTT Connection Error: Ensure Mosquitto is running.")