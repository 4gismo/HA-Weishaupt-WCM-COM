# Weishaupt WCM-COM Integration for Home Assistant

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/v/release/4gismo/HA-Weishaupt-WCM-COM)](https://github.com/4gismo/HA-Weishaupt-WCM-COM/releases)
[![License](https://img.shields.io/github/license/4gismo/HA-Weishaupt-WCM-COM)](LICENSE)

A Home Assistant custom integration for Weishaupt heating systems equipped with the **WCM-COM** network module. Reads live process values directly from the device over your local network — no cloud, no subscription.

> Forked from [phamels/HA-Weishaupt-WCM-COM](https://github.com/phamels/HA-Weishaupt-WCM-COM)

---

## Requirements

- Weishaupt heating system with **WCM-COM** network module
- WCM-COM reachable on your local network (IP address required)
- WCM-COM login credentials (username / password from the device label or set by your installer)

---

## Features

- **23 sensor entities** with proper device classes, units, and history tracking
- **Polling pause switch** — temporarily stops HA from querying the device so you can log in directly via browser (WCM-COM only allows one active user at a time)
- Local polling via HTTP — no cloud dependency
- HACS compatible
- UI-based setup (Config Flow) and legacy YAML support

---

## Sensors

### Temperatures
| Entity | Description | Unit |
|---|---|---|
| Weishaupt Flow Temperature | Supply line temperature (Vorlauf) | °C |
| Weishaupt Outside Temperature | Outside sensor | °C |
| Weishaupt Warm Water Temperature | Domestic hot water | °C |
| Weishaupt Flue Gas Temperature | Exhaust / flue gas | °C |
| Weishaupt Room Temperature | Room sensor | °C |
| Weishaupt Mixed External Temperature | Mixed external circuit | °C |
| Weishaupt Heat Demand | Current heat demand setpoint | °C |
| Weishaupt Damped Outside Temperature | Damped / averaged outside temp | °C |
| Weishaupt Buffer Sensor B10 | Buffer tank sensor (if installed) | °C |

### Burner & Operation
| Entity | Description | Unit |
|---|---|---|
| Weishaupt Load Setting | Current burner load | kW |
| Weishaupt Burner Hours | Total burner operating hours | h |
| Weishaupt Burner Starts | Total burner ignition cycles | — |
| Weishaupt Time Since Last Service | Hours since last maintenance | h |
| Weishaupt Oil Meter | Oil consumption counter | L |
| Weishaupt Operating Mode | Current operation mode | — |
| Weishaupt Operating Phase | Current operation phase | — |

### Status
| Entity | Description |
|---|---|
| Weishaupt Flame | Burner flame active |
| Weishaupt Pump | Circulation pump active |
| Weishaupt Heating | Heating circuit active |
| Weishaupt Warm Water | Hot water circuit active |
| Weishaupt Gas Valve 1 | Gas valve 1 state |
| Weishaupt Gas Valve 2 | Gas valve 2 state |
| Weishaupt Error | Active error code |

### Switch
| Entity | Description |
|---|---|
| Weishaupt Polling | Pause / resume HA polling of the device |

---

## Installation

### Option 1: HACS (recommended)

1. In HACS, go to **Integrations → ⋮ → Custom repositories**
2. Add `https://github.com/4gismo/HA-Weishaupt-WCM-COM` as category **Integration**
3. Install **Weishaupt WCM-COM** and restart Home Assistant
4. Go to **Settings → Devices & Services → Add Integration** and search for *Weishaupt*

### Option 2: Manual

1. Copy the `custom_components/weishaupt_wcm_com/` folder into your HA config directory
2. Restart Home Assistant
3. Go to **Settings → Devices & Services → Add Integration** and search for *Weishaupt*

---

## Configuration

### UI (recommended)

After adding the integration, enter:

| Field | Description |
|---|---|
| Host | IP address of your WCM-COM module |
| Username | WCM-COM login username |
| Password | WCM-COM login password |

### YAML (legacy)

```yaml
weishaupt_wcm_com:
  host: 192.168.1.100
  username: user
  password: secret
```

---

## Polling Pause

The WCM-COM module only allows **one active user at a time**. If Home Assistant is polling the device, you cannot log in through the browser simultaneously.

Use the **Weishaupt Polling** switch to pause HA's polling:
- Switch **off** → HA stops sending requests → browser login works
- Switch **on** → normal polling resumes

Since there is no persistent session (every request re-authenticates via HTTP Digest Auth), turning off polling is sufficient — no explicit logout is needed.

---

## Example Lovelace Dashboard

```yaml
type: vertical-stack
cards:
  - type: entities
    title: Weishaupt Heating
    entities:
      - entity: sensor.weishaupt_flow_temperature
      - entity: sensor.weishaupt_outside_temperature
      - entity: sensor.weishaupt_warm_water_temperature
      - entity: sensor.weishaupt_load_setting
      - entity: sensor.weishaupt_flame
      - entity: sensor.weishaupt_error
      - entity: switch.weishaupt_polling
  - type: history-graph
    title: Temperatures (24h)
    hours_to_show: 24
    entities:
      - entity: sensor.weishaupt_flow_temperature
      - entity: sensor.weishaupt_outside_temperature
      - entity: sensor.weishaupt_warm_water_temperature
```

---

## Debugging

Enable detailed logging in `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    custom_components.weishaupt_wcm_com: debug
```

Logs are visible under **Settings → System → Logs**. With debug level you will see each polling cycle and the raw data received from the device.

---

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| `WCM-COM not reachable` | Wrong IP address, device offline, or firewall blocking port 80 |
| `WCM-COM auth or HTTP error` | Wrong username or password |
| `WCM-COM request timed out` | Device is busy or unreachable — default timeout is 5 seconds |
| `WCM-COM returned unexpected response format` | Firmware version mismatch or protocol change |
| Sensors show `unavailable` | Check logs for the specific error above |
| Cannot log in via browser | Turn off the **Weishaupt Polling** switch first |

---

## License

Apache License 2.0 — see [LICENSE](LICENSE)
