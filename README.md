# Pironman 5 Home Assistant

A local Home Assistant custom integration for the SunFounder Pironman 5 and Pironman 5 Max.

The integration communicates directly with the local Pironman REST API. No MQTT broker, cloud service or additional software is required.

## Features

### Monitoring

* CPU temperature
* GPU temperature
* CPU usage
* CPU frequency
* Memory usage
* Memory used
* NVMe usage
* Network download speed
* Network upload speed
* Fan speed
* Fan running status

### Control

* Fan mode

  * Always On
  * Performance
  * Cool
  * Balanced
  * Quiet
* RGB on/off
* RGB brightness
* RGB color
* RGB effects
* RGB effect speed

### OLED

The integration provides local control of the Pironman 5 Max OLED display.

Currently supported:

- Enable / disable OLED display
- Local control through Home Assistant
- Automatic state synchronization with the Pironman API

More OLED controls such as page selection, rotation and sleep timeout can be added incrementally.

## Requirements

* Home Assistant
* SunFounder Pironman 5 or Pironman 5 Max
* Pironman software with the local REST API
* Prerequisite: Pironman 5 must have its local Dashboard/API running on port 34001.

The integration communicates with the local Pironman API on port `34001` by default.

## Installation

### HACS

Install the integration through HACS.

If the repository is not yet available in the default HACS store, add this repository as a custom repository in HACS:

```text
https://github.com/ChristophKomenda/pironman5-homeassistant
```

Select **Integration** as the repository type.

After installation:

1. Restart Home Assistant.
2. Go to **Settings → Devices & services**.
3. Select **Add Integration**.
4. Search for **Pironman 5**.
5. Enter the Pironman API host and port.

### Manual installation

Copy the `pironman5` directory into:

```text
/config/custom_components/pironman5
```

Restart Home Assistant and add the integration through **Settings → Devices & services**.

## Configuration

The integration provides a configuration flow where the Pironman API host and port can be configured.

Default configuration:

```text
Host: 127.0.0.1
Port: 34001
```

For a Home Assistant Container installation using host networking, `127.0.0.1:34001` can be used when the Pironman service is running directly on the Raspberry Pi host.

For Home Assistant installations where the Pironman service runs on another device, enter the IP address of that device instead.

## Local API

The integration uses the Pironman local REST API:

```text
http://<host>:34001/api/v1.0/
```

No cloud connection is required.

## Supported Hardware

Currently tested with:

* SunFounder Pironman 5 Max

Other Pironman 5 variants may work if they provide the same REST API.

## Troubleshooting

### The integration cannot connect

Check that the Pironman service is running:

```bash
systemctl status pironman5
```

You can also test the API directly:

```bash
curl http://127.0.0.1:34001/api/v1.0/get-data
```

A successful response should contain:

```json
{
  "status": true
}
```

### RGB control does not work

Make sure RGB is enabled in the Pironman configuration and that the Pironman service is running.

## License

MIT License
