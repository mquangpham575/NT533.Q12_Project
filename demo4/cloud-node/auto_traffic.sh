#!/bin/bash

echo "=== BẮT ĐẦU HỆ THỐNG ĐÈN TỰ ĐỘNG ==="
echo "Nhấn Ctrl+C để dừng lại"

while true
do
    # 1. Bật Đèn Xanh
    echo "[Time: $(date +%T)] -> Chuyển sang xanh (GREEN)"
    kubectl patch device light-01 --type='merge' -p '{"status": {"twins": [{"propertyName": "color", "desired": {"value": "GREEN", "metadata": {"type": "string"}}}]}}' > /dev/null
    sleep 4

    # 2. Bật Đèn Đỏ
    echo "[Time: $(date +%T)] -> Chuyển sang đỏ (RED)"
    kubectl patch device light-01 --type='merge' -p '{"status": {"twins": [{"propertyName": "color", "desired": {"value": "RED", "metadata": {"type": "string"}}}]}}' > /dev/null
    sleep 4

    # 3. Bật Đèn Vàng
    echo "[Time: $(date +%T)] -> Chuyển sang vàng (YELLOW)"
    kubectl patch device light-01 --type='merge' -p '{"status": {"twins": [{"propertyName": "color", "desired": {"value": "YELLOW", "metadata": {"type": "string"}}}]}}' > /dev/null
    sleep 4
done