## Edge Computing System with KubeEdge

📌 Project Overview

This project demonstrates the implementation of an Edge Computing infrastructure using KubeEdge, an open-source framework that extends Kubernetes orchestration to the edge. The system enables centralized container management from the Cloud to Edge devices while ensuring Edge Autonomy and seamless IoT device integration.

🏗️ Architecture & Environment

The deployment consists of two primary nodes communicating via WebSocket (Port 10000):

- Master Node (Cloud): Ubuntu-1 (192.168.26.150) running Kubernetes API Server and KubeEdge CloudCore.
- Edge Node (Device): Ubuntu-2 (192.168.26.151) running KubeEdge EdgeCore, Docker Engine, and Mosquitto MQTT Broker.

🚀 Key Demos & Features

We implemented four progressive laboratories to validate the system's capabilities:

- Pod Deployment: Remote container orchestration from Cloud to Edge using nodeSelector.
- Edge Autonomy: Proved self-healing capabilities during network partitions. The Edge Node uses a local SQLite database to maintain operations without Cloud connectivity.
- Device Management (CRDs): Managed hardware via Custom Resource Definitions, using a "Counter App" with a specialized Mapper (Driver).
- Advanced IoT (Traffic Light System): A full-stack integration featuring a Python-based virtual device, MQTT communication, and a Flask Web Dashboard for real-time control.

💡 Key Highlights

- Reliability: Edge nodes function independently during outages.
- Standardization: IoT hardware is managed as standard Kubernetes resources.
- Efficiency: Uses Delta updates over WebSocket to minimize bandwidth consumption.
- Extensibility: Seamless integration with external Web Apps and Python scripts via MQTT and K8s APIs.
