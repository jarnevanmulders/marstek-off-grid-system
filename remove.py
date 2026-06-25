from influxdb_client import InfluxDBClient
from datetime import datetime, timedelta

def delete_battery_measurement(config, influxdb_server):
    client = InfluxDBClient(
        url=config[influxdb_server]['url'],
        token=config[influxdb_server]['write_token'],
        org=config[influxdb_server]['org']
    )

    delete_api = client.delete_api()

    bucket = config[influxdb_server]['bucket']
    org = config[influxdb_server]['org']

    # delete ALL battery data (safety: adjust time range if needed)
    start = "1970-01-01T00:00:00Z"
    stop = datetime.utcnow().isoformat() + "Z"

    predicate = 'measurement="battery"'

    try:
        delete_api.delete(
            bucket=bucket,
            org=org,
            start=start,
            stop=stop,
            predicate=predicate
        )
        print("✓ battery measurement deleted")
    except Exception as e:
        print(f"[ERROR] delete failed: {e}")

    client.close()