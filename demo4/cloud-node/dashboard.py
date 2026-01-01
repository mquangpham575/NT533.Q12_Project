from flask import Flask, render_template_string, redirect, url_for
from kubernetes import client, config
import datetime

app = Flask(__name__)

# K8s API Configuration
config.load_kube_config()
api = client.CustomObjectsApi()

# KubeEdge Device CRD Constants
GROUP = "devices.kubeedge.io"
VERSION = "v1alpha2"
NAMESPACE = "default"
PLURAL = "devices"
DEVICE_NAME = "light-01"

# Status Translation Map (English -> Vietnamese)
COLOR_MAP = {
    'RED': 'ĐỎ',
    'GREEN': 'XANH',
    'YELLOW': 'VÀNG',
    'OFF': 'TẮT',
    'WAITING': 'ĐANG KHỞI ĐỘNG'
}

# Global cache to prevent UI flicker during sync
last_known_color = "OFF"

# Dashboard UI Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Điều Khiển Đèn Giao Thông</title>
    <meta http-equiv="refresh" content="1"> 
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #212529; color: white; padding-top: 50px; font-family: sans-serif; }
        .traffic-light {
            background-color: #333; width: 150px; padding: 20px; border-radius: 30px; margin: 0 auto;
            border: 5px solid #555;
        }
        .bulb {
            width: 100px; height: 100px; background-color: #444; border-radius: 50%; margin: 20px auto;
            transition: background-color 0.2s; 
            box-shadow: inset 0 0 20px #000;
            opacity: 0.3;
        }
        /* Active states */
        .bulb.red.active { background-color: #ff0000; box-shadow: 0 0 50px #ff0000; opacity: 1; }
        .bulb.yellow.active { background-color: #ffcc00; box-shadow: 0 0 50px #ffcc00; opacity: 1; }
        .bulb.green.active { background-color: #00ff00; box-shadow: 0 0 50px #00ff00; opacity: 1; }
        
        .card { background-color: #343a40; border-color: #454d55; }
        .status-text { font-size: 1.2rem; font-weight: bold; margin-top: 15px; min-height: 1.5em; text-transform: uppercase;}
    </style>
</head>
<body>
    <div class="container text-center">
        <h2 class="mb-4">🚦 HỆ THỐNG ĐÈN GIAO THÔNG</h2>
        
        <div class="row justify-content-center">
            <div class="col-md-4 mb-4">
                <div class="traffic-light">
                    <div class="bulb red {{ 'active' if 'RED' in display_color else '' }}"></div>
                    <div class="bulb yellow {{ 'active' if 'YELLOW' in display_color else '' }}"></div>
                    <div class="bulb green {{ 'active' if 'GREEN' in display_color else '' }}"></div>
                </div>
                
                <div class="mt-3">
                    <div class="status-text" style="color: {{ text_color }}">
                        {{ display_text }}
                    </div>
                    <small class="text-muted">Cập nhật: {{ time }}</small>
                </div>
            </div>

            <div class="col-md-4">
                <div class="card p-4">
                    <h4 class="mb-4 text-white">Bảng Điều Khiển</h4>
                    <div class="d-grid gap-3">
                        <a href="/set/RED" class="btn btn-danger btn-lg">🔴 Bật Đèn Đỏ</a>
                        <a href="/set/YELLOW" class="btn btn-warning btn-lg">🟡 Bật Đèn Vàng</a>
                        <a href="/set/GREEN" class="btn btn-success btn-lg">🟢 Bật Đèn Xanh</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    global last_known_color 
    
    try:
        # Fetch device twins from K8s API
        device = api.get_namespaced_custom_object(GROUP, VERSION, NAMESPACE, PLURAL, DEVICE_NAME)
        twins = device.get('status', {}).get('twins', [])
        
        actual_val = None
        desired_val = None

        for twin in twins:
            if twin['propertyName'] == 'color':
                actual_val = twin.get('reported', {}).get('value')
                desired_val = twin.get('desired', {}).get('value')

        # Update cache if reported value exists
        if actual_val:
            last_known_color = actual_val
        
        # Translate status to Vietnamese for display
        vn_status = COLOR_MAP.get(last_known_color, last_known_color)
        
        display_color = last_known_color
        display_text = f"Trạng thái: {vn_status}"
        text_color = "white"

        # Handle pending synchronization state
        if desired_val and desired_val != last_known_color:
            vn_desired = COLOR_MAP.get(desired_val, desired_val)
            display_text = f"Đang chuyển sang {vn_desired}..."
            text_color = "#ffc107" 
        
        return render_template_string(HTML_TEMPLATE, 
                                      display_color=display_color,
                                      display_text=display_text,
                                      text_color=text_color,
                                      time=datetime.datetime.now().strftime("%H:%M:%S"))
    except Exception as e:
        return f"K8s Error: {e}"

@app.route('/set/<color>')
def set_color(color):
    # Construct KubeEdge payload
    body = {
        "status": {
            "twins": [{"propertyName": "color", "desired": {"value": color, "metadata": {"type": "string"}}}]
        }
    }
    try:
        # Patch desired state to K8s
        api.patch_namespaced_custom_object(GROUP, VERSION, NAMESPACE, PLURAL, DEVICE_NAME, body)
    except Exception as e:
        print(f"Patch Error: {e}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)