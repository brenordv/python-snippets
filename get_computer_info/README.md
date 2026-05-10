# Get Computer Info

A lightweight system-health monitor that periodically collects CPU, memory, disk, NAS, and network metrics using `psutil` and publishes them as JSON to an MQTT broker. Set the `DRY_RUN` environment variable to log metrics locally instead of publishing.

## Usage

```bash
# Set required env vars (or set DRY_RUN=true to skip MQTT)
export LOCAL_DISK_PATH="/" NAS_PATH="/mnt/nas"
export MQTT_SERVER="mqtt.local" MQTT_QUEUE="server/metrics"
export DRY_RUN=true

python get_server_info.py
```
