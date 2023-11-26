import psutil
import time
import json
import paho.mqtt.client as mqtt
# pip install psutil paho-mqtt


def get_disk_usage(path):
    usage = psutil.disk_usage(path)
    return usage.used / (1024 ** 3), usage.total / (1024 ** 3)  # Convert to GB


def send_mqtt_message(client, type, value):
    message = json.dumps({"host": "this.server", "type": type, "value": value})
    #client.publish("/my/queue", message)
    print(f"Message sent: {message}")


"""
This script sends the following information to an MQTT broker:
- CPU usage (every 5 seconds)
- Current memory usage (every 5 seconds)
- Current storage usage (every 10 minutes)
- Current NAS usage (every 10 minutes)
- Total storage (every 24 hours)
- Total NAS storage (every 24 hours)
- Total memory (every 24 hours)

The script is intended to be run on a server, but can be run on any computer.
It's a lazy approach for a simple monitoring solution. I just wanted the data so I could display it in a Grafana 
dashboard.
"""
def main(local_disk_path, nas_path):
    client = mqtt.Client()
    #client.connect("mqtt_broker_address", 1883, 60)  # Replace with your MQTT broker's address and port

    # Initialize last sent times
    last_sent_mem_total = last_sent_storage_total = last_sent_nas_total = None

    try:
        while True:
            current_time = time.time()

            # CPU and Current Memory Usage (every 5 seconds)
            if last_sent_mem_total is None or current_time - last_sent_mem_total >= 5:
                send_mqtt_message(client, "CPU", psutil.cpu_percent())
                mem = psutil.virtual_memory()
                send_mqtt_message(client, "MEM", mem.used / (1024 ** 3))  # Current usage in GB
                last_sent_mem_total = current_time

            # Storage and NAS Usage (every 10 minutes)
            if last_sent_storage_total is None or current_time - last_sent_storage_total >= 600:
                send_mqtt_message(client, "STORAGE CURRENT", get_disk_usage(local_disk_path)[0])  # Current storage "/"
                send_mqtt_message(client, "NAS CURRENT", get_disk_usage(nas_path)[0])  # Current NAS usage
                last_sent_storage_total = current_time

            # Total Memory, Storage, and NAS (every 24 hours)
            if last_sent_nas_total is None or current_time - last_sent_nas_total >= 86400:
                send_mqtt_message(client, "STORAGE TOTAL", get_disk_usage(local_disk_path)[1])  # Total storage "/"
                send_mqtt_message(client, "NAS TOTAL", get_disk_usage(nas_path)[1])  # Total NAS storage
                send_mqtt_message(client, "TOTAL MEM", mem.total / (1024 ** 3))  # Total memory in GB
                last_sent_nas_total = current_time

            time.sleep(1)  # Short sleep to prevent high CPU usage

    except KeyboardInterrupt:
        print("Script interrupted")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main(
        local_disk_path="/",  # Replace with your local disk path
        nas_path="/mnt/nas"  # Replace with your NAS path
    )
