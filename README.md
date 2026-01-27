# KubeEdge Distributed Computing System Demo

> **University:** University of Information Technology (UIT) - VNU-HCM
> **Course:** Distributed Computing Systems (Hệ Tính Toán Phân Bố)
> **Project Type:** Educational / Research Mockup
> **Topic:** Edge Computing Infrastructure with KubeEdge

## Introduction

This project serves as a practical demonstration of **Edge Computing** principles using **KubeEdge**, an open-source system extending native containerized application orchestration capabilities to hosts at the Edge.

The goal is to showcase how a **Cloud-Edge** architecture works in a distributed environment, ensuring reliability, autonomy, and efficient data processing closer to the source of data (IoT devices).

## System Architecture

The system mimics a real-world distributed scenario with two primary layers:

1.  **Cloud Layer (Master Node)**
    *   **Role**: Central control plane.
    *   **Components**: Kubernetes API Server, KubeEdge `CloudCore`, Web Dashboard.
    *   **Function**: Manages the cluster, issues commands, and monitors device status.

2.  **Edge Layer (Edge Node)**
    *   **Role**: Execution unit closer to devices.
    *   **Components**: KubeEdge `EdgeCore`, MQTT Broker (Mosquitto), Docker Engine.
    *   **Function**: Executes application pods, manages local devices, and ensures autonomous operation even when disconnected from the cloud.

---

## Demos & Features

This repository contains code and configurations for **4 progressive laboratories**, demonstrating different aspects of the KubeEdge system.

### 1. Basic Pod Deployment (`demo1`)
Demonstrates the fundamental capability of KubeEdge to schedule and deploy applications from the Cloud to a specific Edge Node.
*   **What it does**: Deploys a lightweight **Nginx** server exclusively to the edge node.
*   **Key Concept**: `nodeSelector` in Kubernetes allows precise placement of workloads on edge devices.
*   **File**: `demo1/nginx-edge.yaml`

### 2. Edge Autonomy (Resilience Test)
*Concept demonstration (No specific code folder - observed behavior)*
*   **Scenario**: We simulate a network failure by disconnecting the Edge Node from the Cloud.
*   **Result**: The applications running on the edge continue to function normally without control plane connectivity. This proves the **Edge Autonomy** feature of KubeEdge (local persistence via SQLite).

### 3. Device Management with CRDs (`demo3`)
Demonstrates how to manage physical/logical devices using Kubernetes Custom Resource Definitions (CRDs): `DeviceModel` and `DeviceInstance`.
*   **Application**: A "Counter App" that increments a value.
*   **Workflow**:
    1.  **Model**: Defines the attributes/properties of a "Counter" device.
    2.  **Instance**: Represents the actual device.
    3.  **Mapper**: A driver that talks to the device and syncs data with the Cloud.
*   **Key Concept**: "Kubernetes-native" way of managing IoT devices.

### 4. Advanced IoT: Smart Traffic Light System (`demo4`)
A full-stack implementation of a smart city component. This is the most complex demo involving bi-directional communication (Cloud <-> Edge <-> Device).

**Components:**
*   **Cloud Node**:
    *   `dashboard.py`: A Flask web interface to view traffic status and manually switch lights.
    *   `auto_traffic.sh`: Automation scripts.
    *   `device*.yaml`: Device definitions for the Traffic Light.
*   **Edge Node**:
    *   `smart_device.py`: A Python script simulating the Traffic Light hardware. It listens for MQTT messages to change lights and reports current state back to the Cloud.

**Workflow**:
1.  User clicks "Green Light" on **Cloud Dashboard**.
2.  Command sent via K8s API -> CloudCore -> EdgeCore -> **MQTT Broker**.
3.  **Edge Device (`smart_device.py`)** receives MQTT message -> changes light color.
4.  Device reports new status -> MQTT -> EdgeCore -> CloudCore -> **Dashboard updates**.

---

## Tech Stack

*   **Orchestration**: Kubernetes (K8s) v1.2x
*   **Edge Framework**: KubeEdge v1.1x
*   **Container Runtime**: Docker / Containerd
*   **Messaging**: MQTT (Eclipse Mosquitto)
*   **Programming**: Python (Flask, Paho-MQTT), Shell Scripting
*   **OS**: Ubuntu Linux (Virtual Machines)

## Prerequisites to Run

To replicate this setup, you need:
1.  **Two VM/Physical Nodes**: One for Cloud (Master), one for Edge.
2.  **OS**: Linux (Ubuntu 20.04 recommended).
3.  **Ports**: Open port `10000-10004` (CloudCore) and `1883` (MQTT).
4.  **Dependencies**:
    *   Install generic Kubernetes tools (`kubectl`, `kubeadm`) on Cloud.
    *   Install `keadm` (KubeEdge installer) on both nodes.

## Usage Guide (Demo 4)

1.  **Setup Device Model & Instance** (on Cloud):
    ```bash
    kubectl apply -f demo4/cloud-node/device-model.yaml
    kubectl apply -f demo4/cloud-node/device-instance.yaml
    ```
2.  **Start Edge Device Simulator** (on Edge):
    ```bash
    python3 demo4/edge-node/smart_device.py
    ```
3.  **Run Dashboard** (on Cloud):
    ```bash
    python3 demo4/cloud-node/dashboard.py
    ```
4.  Access the web interface at `http://<cloud-ip>:5000` to control the traffic lights.

---
*Created for the "He Tinh Toan Phan Bo" Course Project at UIT HCM.*
