# Weishaupt WCM-COM Integration for Home Assistant

This is a custom integration for connecting Weishaupt heating systems via the WCM-COM module to Home Assistant.

---

## Features

- Reads values such as:
  - Room temperature
  - Flow temperature
  - Outside temperature
  - Burner state, pump, flame, errors and more
- Works via:
  - YAML configuration
  - UI-based config flow
- Built with Home Assistant best practices (async, setup migration, etc.)
- 100% HACS compatible

---

## Installation

### Option 1: via HACS (recommended)

1. Add this repository as a custom integration in HACS:
   - Go to **HACS → Integrations → ⋮ → Custom repositories**
   - URL: `https://github.com/4gismo/HA-Weishaupt-WCM-COM`
   - Category: **Integration**

2. Install **Weishaupt WCM-COM**

3. Reboot Home Assistant

4. Go to **Settings → Devices & Services → Add Integration**

---

### Option 2: Manual install

1. Copy `custom_components/weishaupt_wcm_com/` to your Home Assistant config directory

2. Reboot Home Assistant

---

## Configuration

### UI (recommended)

After adding the integration, enter:

- Host (IP of your WCM-COM)
- Username
- Password

### YAML (legacy) 
Edit in `configuration.yaml`:

```yaml
weishaupt_wcm_com:
  host: 192.168.x.x
  username: myuser
  password: mypass
```

---

## Example Lovelace Dashboard

```yaml
type: vertical-stack
cards:
  - type: entities
    title: Weishaupt Heating
    entities:
      - entity: sensor.weishaupt_room_temperature
      - entity: sensor.weishaupt_flow_temperature
      - entity: sensor.weishaupt_outside_temperature
      - entity: sensor.weishaupt_flame
      - entity: sensor.weishaupt_error
  - type: history-graph
    title: Temperature history
    hours_to_show: 24
    entities:
      - entity: sensor.weishaupt_room_temperature
      - entity: sensor.weishaupt_flow_temperature
```

---

## Debugging

Enable logging in `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    custom_components.weishaupt_wcm_com: debug
```

You’ll then see logs under **Settings → System → Logs**

---

## License

This project is licensed under the Apache License 2.0.

See the [LICENSE](LICENSE) file for details.

Forked from [`phamels/HA-Weishaupt-WCM-COM`](https://github.com/phamels/HA-Weishaupt-WCM-COM).
