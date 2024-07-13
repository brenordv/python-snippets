"""
get_server_info.py - Script to get computer information and send it to an MQTT broker. If dry_run is set to True, will
just log the messages (as info) instead of sending them to the MQTT broker.

The idea is to use this as a very simple, basic and lightweight way to monitor a computer's health. I use this in my
home lab to keep track of how my server is doing. (and yes, I know there are ready-made solutions for this, but I
wanted something super basic and all options I looked at were way too much.)
"""
import psutil
import time
import json
import os
import paho.mqtt.client as mqtt
from simple_log_factory.log_factory import log_factory

# pip install psutil paho-mqtt simple-log-factory

# Environment variables
LOCAL_DISK_PATH = os.getenv('LOCAL_DISK_PATH')
NAS_PATH = os.getenv('NAS_PATH')
MQTT_SERVER = os.getenv('MQTT_SERVER')
MQTT_QUEUE = os.getenv('MQTT_QUEUE')
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))
DRY_RUN = bool(os.getenv('DRY_RUN', False))

logger = log_factory("net-monitor", unique_handler_types=True)


class DryRunMqttMock(object):
    def __init__(self):
        self._logger = log_factory("DryRunMqttMock", unique_handler_types=True)

    def publish(self, topic, message):
        self._logger.info(f"[MQTT Client] Publishing to topic {topic}: {message}")

    def disconnect(self):
        return


class MqttMessage(object):
    def __init__(self):
        self._cpu_percent = None
        self._mem_used = None
        self._mem_total = None
        self._storage_used = None
        self._storage_total = None
        self._nas_used = None
        self._nas_total = None
        self._net_upload = None
        self._net_download = None

    def to_dict(self):
        return {
            "cpu_percent": self._cpu_percent,
            "mem_used": self._mem_used,
            "mem_total": self._mem_total,
            "storage_used": self._storage_used,
            "storage_total": self._storage_total,
            "nas_used": self._nas_used,
            "nas_total": self._nas_total,
            "net_upload": self._net_upload,
            "net_download": self._net_download
        }

    @staticmethod
    def _can_update_value(value):
        return value is not None and value != 0

    @staticmethod
    def _convert_value_to_gb(value):
        return value / (1024 ** 3)

    def update_cpu_percent(self, cpu_percent):
        if not self._can_update_value(cpu_percent):
            return
        self._cpu_percent = cpu_percent

    def update_mem_used(self, mem_used):
        if not self._can_update_value(mem_used):
            return
        self._mem_used = self._convert_value_to_gb(mem_used)

    def update_mem_total(self, mem_total):
        if not self._can_update_value(mem_total):
            return
        self._mem_total = self._convert_value_to_gb(mem_total)

    def update_storage_used(self, storage_used):
        if storage_used is None or storage_used == 0:
            return
        self._storage_used = storage_used

    def update_storage_total(self, storage_total):
        if storage_total is None or storage_total == 0:
            return
        self._storage_total = storage_total

    def update_nas_used(self, nas_used):
        if nas_used is None or nas_used == 0:
            return
        self._nas_used = nas_used

    def update_nas_total(self, nas_total):
        if nas_total is None or nas_total == 0:
            return
        self._nas_total = nas_total

    def update_net_upload(self, net_upload):
        if net_upload is None or net_upload == 0:
            return
        self._net_upload = net_upload

    def update_net_download(self, net_download):
        if net_download is None or net_download == 0:
            return
        self._net_download = net_download


def _get_disk_usage(path):
    logger.debug("Getting disk usage")
    usage = psutil.disk_usage(path)
    return usage.used / (1024 ** 3), usage.total / (1024 ** 3)  # Convert to GB


def _send_mqtt_message(client, message_obj):
    message = json.dumps(message_obj.to_dict())
    logger.debug(f"Sending message: {message}")
    client.publish(MQTT_QUEUE, message)


def _check_env_var(dry_run):
    if dry_run:
        return True

    required_env_vars = [LOCAL_DISK_PATH, NAS_PATH, MQTT_SERVER, MQTT_QUEUE]

    if any([x is None for x in required_env_vars]):
        logger.error("Missing required environment variable")
        return False

    return True


def _get_mqtt_client(dry_run):
    if dry_run:
        return DryRunMqttMock()

    client = mqtt.Client()

    logger.debug(f"Connecting to MQTT broker at {MQTT_SERVER}")
    client.connect(MQTT_SERVER, MQTT_PORT, 60)
    return client


def main(dry_run=False):
    logger.debug("Starting script")

    if not _check_env_var(dry_run):
        exit(1)

    client = _get_mqtt_client(dry_run)

    # Initialize last sent times
    last_sent_storage_total = None
    last_sent_nas_total = None

    try:
        server_info = MqttMessage()
        net_io_last = psutil.net_io_counters()
        time.sleep(5)  # Wait a bit to let the network usage "settle"

        while True:
            current_time = time.time()

            logger.debug("Setting CPU usage")
            server_info.update_cpu_percent(psutil.cpu_percent())

            mem = psutil.virtual_memory()
            logger.debug("Setting memory usage")
            server_info.update_mem_used(mem.used)

            logger.debug("Getting network usage")
            net_io_current = psutil.net_io_counters()

            logger.debug("Setting network usage - upload")
            upload_rate = net_io_current.bytes_sent - net_io_last.bytes_sent
            server_info.update_net_upload(upload_rate)

            logger.debug("Setting network usage - download")
            download_rate = net_io_current.bytes_recv - net_io_last.bytes_recv
            server_info.update_net_download(download_rate)

            net_io_last = net_io_current

            # Update data every 10 minutes
            if last_sent_storage_total is None or current_time - last_sent_storage_total >= 600:
                logger.debug("Setting local storage usage")
                server_info.update_storage_used(_get_disk_usage(LOCAL_DISK_PATH)[0])

                logger.debug("Setting NAS usage")
                server_info.update_nas_used(_get_disk_usage(NAS_PATH)[0])

                last_sent_storage_total = current_time

            # Update data every 24 hours
            if last_sent_nas_total is None or current_time - last_sent_nas_total >= 86400:
                logger.debug("Setting total local storage")
                server_info.update_storage_total(_get_disk_usage(LOCAL_DISK_PATH)[1])

                logger.debug("Setting total NAS")
                server_info.update_nas_total(_get_disk_usage(NAS_PATH)[1])

                logger.debug("Setting total memory")
                server_info.update_mem_total(mem.total)

                last_sent_nas_total = current_time

            _send_mqtt_message(client, server_info)

            time.sleep(5)

    except KeyboardInterrupt:
        logger.debug("Stopping script")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main(dry_run=DRY_RUN)
