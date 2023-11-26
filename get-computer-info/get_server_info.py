import psutil
import time
import json
import os
import paho.mqtt.client as mqtt
from simple_log_factory.log_factory import log_factory

# pip install psutil paho-mqtt simple-log-factory

# Environment variables
local_disk_path = os.getenv('LOCAL_DISK_PATH')
nas_path = os.getenv('NAS_PATH')
mqtt_server = os.getenv('MQTT_SERVER')
mqtt_queue = os.getenv('MQTT_QUEUE')
mqtt_port = int(os.getenv('MQTT_PORT', 1883))

logger = log_factory("net-monitor", unique_handler_types=True)


def get_disk_usage(path):
    logger.debug("Getting disk usage")
    usage = psutil.disk_usage(path)
    return usage.used / (1024 ** 3), usage.total / (1024 ** 3)  # Convert to GB


def send_mqtt_message(client, msg_type, value):
    message = json.dumps({"host": "my.host", "type": msg_type, "value": value})
    logger.debug(f"Sending message: {message}")
    client.publish(mqtt_queue, message)


def main():
    logger.debug("Starting script")

    required_env_vars = [local_disk_path, nas_path, mqtt_server, mqtt_queue]
    if any([x is None for x in required_env_vars]):
        logger.error("Missing required environment variable")
        exit(1)

    client = mqtt.Client()

    logger.debug(f"Connecting to MQTT broker at {mqtt_server}")
    client.connect(mqtt_server, mqtt_port, 60)

    # Initialize last sent times
    last_sent_mem_total = last_sent_storage_total = last_sent_nas_total = None

    try:
        while True:
            current_time = time.time()

            # CPU and Current Memory Usage (every 5 seconds)
            if last_sent_mem_total is None or current_time - last_sent_mem_total >= 5:
                logger.debug("Sending CPU and memory usage")
                send_mqtt_message(client, "CPU", psutil.cpu_percent())
                mem = psutil.virtual_memory()
                send_mqtt_message(client, "MEM", mem.used / (1024 ** 3))  # Current usage in GB
                last_sent_mem_total = current_time

            # Storage and NAS Usage (every 10 minutes)
            if last_sent_storage_total is None or current_time - last_sent_storage_total >= 600:
                logger.debug("Sending storage and NAS usage")
                send_mqtt_message(client, "STORAGE CURRENT", get_disk_usage(local_disk_path)[0])  # Current storage "/"
                send_mqtt_message(client, "NAS CURRENT", get_disk_usage(nas_path)[0])  # Current NAS usage
                last_sent_storage_total = current_time

            # Total Memory, Storage, and NAS (every 24 hours)
            if last_sent_nas_total is None or current_time - last_sent_nas_total >= 86400:
                logger.debug("Sending total memory, storage, and NAS")
                send_mqtt_message(client, "STORAGE TOTAL", get_disk_usage(local_disk_path)[1])  # Total storage "/"
                send_mqtt_message(client, "NAS TOTAL", get_disk_usage(nas_path)[1])  # Total NAS storage
                send_mqtt_message(client, "TOTAL MEM", mem.total / (1024 ** 3))  # Total memory in GB
                last_sent_nas_total = current_time

            time.sleep(1)  # Short sleep to prevent high CPU usage

    except KeyboardInterrupt:
        logger.debug("Stopping script")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
