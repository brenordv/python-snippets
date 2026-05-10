"""Collect basic computer health metrics and publish them to an MQTT broker.

Monitors CPU, memory, disk, NAS, and network usage at regular intervals.
If ``dry_run`` is enabled, metrics are logged instead of being sent to MQTT.

Requires: psutil, paho-mqtt, simple-log-factory
"""

import json
import os
import time
from dataclasses import dataclass, asdict

import paho.mqtt.client as mqtt
import psutil
from simple_log_factory.log_factory import log_factory

# Environment variables
LOCAL_DISK_PATH: str | None = os.getenv("LOCAL_DISK_PATH")
NAS_PATH: str | None = os.getenv("NAS_PATH")
MQTT_SERVER: str | None = os.getenv("MQTT_SERVER")
MQTT_QUEUE: str | None = os.getenv("MQTT_QUEUE")
MQTT_PORT: int = int(os.getenv("MQTT_PORT", "1883"))
DRY_RUN: bool = os.getenv("DRY_RUN", "").lower() in ("1", "true", "yes")

logger = log_factory("net-monitor", unique_handler_types=True)

BYTES_PER_GB = 1024**3
STORAGE_REFRESH_SECONDS = 600   # 10 minutes
TOTAL_REFRESH_SECONDS = 86_400  # 24 hours
POLL_INTERVAL_SECONDS = 5


class DryRunMqttMock:
    """Stand-in MQTT client that logs messages instead of publishing them."""

    def __init__(self) -> None:
        self._logger = log_factory("DryRunMqttMock", unique_handler_types=True)

    def publish(self, topic: str, message: str) -> None:
        self._logger.info(f"[MQTT Client] Publishing to topic {topic}: {message}")

    def disconnect(self) -> None:
        pass


@dataclass
class ServerMetrics:
    """Container for the server health metrics sent over MQTT."""

    cpu_percent: float | None = None
    mem_used: float | None = None
    mem_total: float | None = None
    storage_used: float | None = None
    storage_total: float | None = None
    nas_used: float | None = None
    nas_total: float | None = None
    net_upload: int | None = None
    net_download: int | None = None


def _bytes_to_gb(value: float) -> float:
    return value / BYTES_PER_GB


def _get_disk_usage_gb(path: str) -> tuple[float, float]:
    """Return (used_gb, total_gb) for *path*."""
    usage = psutil.disk_usage(path)
    return _bytes_to_gb(usage.used), _bytes_to_gb(usage.total)


def _check_env_vars(dry_run: bool) -> bool:
    if dry_run:
        return True
    required = [LOCAL_DISK_PATH, NAS_PATH, MQTT_SERVER, MQTT_QUEUE]
    if any(v is None for v in required):
        logger.error("Missing required environment variable")
        return False
    return True


def _get_mqtt_client(dry_run: bool) -> mqtt.Client | DryRunMqttMock:
    if dry_run:
        return DryRunMqttMock()
    client = mqtt.Client()
    logger.debug(f"Connecting to MQTT broker at {MQTT_SERVER}")
    client.connect(MQTT_SERVER, MQTT_PORT, 60)
    return client


def _send_mqtt_message(
    client: mqtt.Client | DryRunMqttMock, metrics: ServerMetrics
) -> None:
    message = json.dumps(asdict(metrics))
    logger.debug(f"Sending message: {message}")
    client.publish(MQTT_QUEUE, message)


def main(dry_run: bool = False) -> None:
    """Main monitoring loop."""
    logger.debug("Starting script")

    if not _check_env_vars(dry_run):
        raise SystemExit(1)

    client = _get_mqtt_client(dry_run)
    metrics = ServerMetrics()

    last_storage_update: float | None = None
    last_total_update: float | None = None

    try:
        net_io_last = psutil.net_io_counters()
        time.sleep(POLL_INTERVAL_SECONDS)

        while True:
            now = time.time()

            metrics.cpu_percent = psutil.cpu_percent() or metrics.cpu_percent
            mem = psutil.virtual_memory()
            metrics.mem_used = _bytes_to_gb(mem.used)

            net_io = psutil.net_io_counters()
            upload = net_io.bytes_sent - net_io_last.bytes_sent
            download = net_io.bytes_recv - net_io_last.bytes_recv
            if upload:
                metrics.net_upload = upload
            if download:
                metrics.net_download = download
            net_io_last = net_io

            # Refresh used-disk metrics every 10 minutes
            if last_storage_update is None or now - last_storage_update >= STORAGE_REFRESH_SECONDS:
                metrics.storage_used = _get_disk_usage_gb(LOCAL_DISK_PATH)[0]
                metrics.nas_used = _get_disk_usage_gb(NAS_PATH)[0]
                last_storage_update = now

            # Refresh total-disk/memory metrics every 24 hours
            if last_total_update is None or now - last_total_update >= TOTAL_REFRESH_SECONDS:
                metrics.storage_total = _get_disk_usage_gb(LOCAL_DISK_PATH)[1]
                metrics.nas_total = _get_disk_usage_gb(NAS_PATH)[1]
                metrics.mem_total = _bytes_to_gb(mem.total)
                last_total_update = now

            _send_mqtt_message(client, metrics)
            time.sleep(POLL_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        logger.debug("Stopping script")
    finally:
        client.disconnect()


if __name__ == "__main__":
    main(dry_run=DRY_RUN)
