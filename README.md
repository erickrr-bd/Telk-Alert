# Telk-Alert

Easy alerting with Elasticsearch and Python.

Telk-Alert searches your Elasticsearch indexes periodically with the alert rules you define and sends the events found to Telegram. The suite has three components:

| Component | What it does | Runs as |
|---|---|---|
| **Telk-Alert-Tool** | Terminal interface (TUI) to configure the connection to Elasticsearch, the agent and the alert rules, and to manage the services. | `root` (`sudo telk-alert-tool`) |
| **Telk-Alert** | Service that runs every alert rule and sends the alerts to Telegram. | `telk_alert` (systemd: `telk-alert.service`) |
| **Telk-Alert-Agent** | Service that monitors Telk-Alert and notifies via Telegram when it stops working. | `telk_alert` (systemd: `telk-alert-agent.service`) |

**Version:** 4.2 - November 2026
**Author:** Erick Roberto Rodriguez Rodriguez ([erodriguez@tekium.mx](mailto:erodriguez@tekium.mx), [erickrr.tbd93@gmail.com](mailto:erickrr.tbd93@gmail.com))

---

## Table of contents

- [How it works](#how-it-works)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Telk-Alert-Tool](#telk-alert-tool)
- [Telk-Alert](#telk-alert-1)
- [Telk-Alert-Agent](#telk-alert-agent)
- [Files and permissions](#files-and-permissions)
- [Security](#security)
- [Troubleshooting](#troubleshooting)
- [Upgrading from 4.1](#upgrading-from-41)
- [Changelog](#changelog)

---

## How it works

```
                 sudo telk-alert-tool (root)
                            │ creates / modifies
                            ▼
   ┌─────────────────────────────────────────────────────────┐
   │ /opt/Telk-Alert-Suite                                   │
   │   Telk-Alert/configuration/telk_alert.yaml   (cluster)  │
   │   Telk-Alert/alert_rules/*.yaml              (rules)    │
   │   Telk-Alert-Agent/configuration/*.yaml      (agent)    │
   │   Telk-Alert/configuration/key               (key)      │
   └─────────────────────────────────────────────────────────┘
                 │ reads                         │ reads
                 ▼                               ▼
   ┌───────────────────────────┐     ┌───────────────────────────┐
   │ telk-alert.service        │     │ telk-alert-agent.service  │
   │  one thread per rule ─────┼──►  │  checks the service and   │
   │  searches Elasticsearch   │ heartbeat (/run/telk-alert)     │
   │  queues the alerts        │     │  the heartbeat            │
   │  one sender per chat ─────┼─┐   │  restarts it if needed ───┼─┐
   └───────────────────────────┘ │   └───────────────────────────┘ │
                 ▲               │                ▲              │
                 │               ▼                │              ▼
          Elasticsearch       Telegram     systemd (polkit)   Telegram
```

1. With **Telk-Alert-Tool** you configure the cluster, the agent and the alert rules. Credentials are stored encrypted.
2. **Telk-Alert** starts one thread per rule. Every *search time*, each rule searches its *range time* in Elasticsearch; if it finds at least *total events*, it groups the events in as few messages as possible and puts them in the sending queue of its Telegram chat.
3. One sender per chat delivers the messages at Telegram's pace (20 per minute), so the rules never wait for Telegram.
4. Telk-Alert writes a **heartbeat** every minute. **Telk-Alert-Agent** reads it: if a rule stops running, it restarts Telk-Alert; if the service is down or a rule couldn't start, it notifies you.

## Requirements

- Linux with **systemd** (Debian/Ubuntu, RHEL/Rocky/Alma/Fedora, SUSE or Arch).
- **Python 3.14** (the installer only accepts this version).
- **polkit >= 0.106** (JavaScript rules) for the agent to restart the service. Check it with `pkaction --version`.
- An **Elasticsearch 8.x or 9.x** cluster reachable from the server.
- A **Telegram bot** ([@BotFather](https://t.me/BotFather)) added to the chat, group or channel that will receive the alerts, and the chat ID.

The installer installs the system packages (`dialog`, `git`, `openssl`, `gcc`, libcurl and OpenSSL headers) and the Python dependencies in a virtual environment managed by Poetry:

| Dependency | Use |
|---|---|
| `elasticsearch` | Elasticsearch client (includes `elasticsearch.dsl`). **Its major version must match the cluster's** (see [Troubleshooting](#troubleshooting)). |
| `pycurl` | Telegram API (libPyTelegram). |
| `pycryptodomex`, `PyYAML`, `psutil`, `pythondialog` | Encryption, configuration files, processes and TUI. |
| [libPyUtils](https://github.com/erickrr-bd/libPyUtils), [libPyLog](https://github.com/erickrr-bd/libPyLog), [libPyDialog](https://github.com/erickrr-bd/libPyDialog), [libPyTelegram](https://github.com/erickrr-bd/libPyTelegram), [libPyConfiguration](https://github.com/erickrr-bd/libPyConfiguration), [libPyAgentConfiguration](https://github.com/erickrr-bd/libPyAgentConfiguration), [libPyElk](https://github.com/erickrr-bd/libPyElk) | Author's libraries. |

## Installation

```bash
git clone https://github.com/erickrr-bd/Telk-Alert.git
cd Telk-Alert
sudo ./telk_alert_installer.sh install
```

Expected layout next to the installer:

```
telk_alert_installer.sh
pyproject.toml              (and poetry.lock, recommended)
telk-alert.service
telk-alert-agent.service
50-telk-alert-agent.rules
Telk-Alert-Suite/           (Telk-Alert-Tool, Telk-Alert, Telk-Alert-Agent)
```

The installer:

1. Installs the system packages and checks Python 3.14.
2. Creates the `telk_alert` user and group (system account, no shell).
3. Copies the code to `/opt/Telk-Alert-Suite` and creates the virtual environment (`/opt/Telk-Alert-Suite/.venv`) with Poetry.
4. Migrates the key, configurations and rules of version 4.1 from `/etc/Telk-Alert-Suite`, if they exist (they are copied, never deleted).
5. Creates the folders and a random master key (`openssl rand -hex 32`) if there isn't one.
6. Applies the permissions, installs the `telk-alert-tool` command, the systemd units and the polkit rule.
7. Verifies that every dependency can be imported as `telk_alert`.

To update (code and dependencies; configuration, key and rules are never touched):

```bash
sudo ./telk_alert_installer.sh update
```

The services that were running are stopped (agent first) and started again at the end.

## Configuration

```bash
sudo telk-alert-tool
```

1. **Configuration → Telk-Alert → Create:** Elasticsearch hosts, CA certificate and authentication.
2. **Configuration → Telk-Alert-Agent → Create:** validation frequency, Telegram Bot Token and Chat ID for the agent's notifications.
3. **Alert Rules → Create alert rule:** one per detection.
4. Start the services:

```bash
sudo systemctl enable --now telk-alert.service telk-alert-agent.service
```

## Telk-Alert-Tool

| Menu | Options |
|---|---|
| **Configuration** | Create, modify or display the configuration of Telk-Alert or Telk-Alert-Agent. |
| **Alert Rules** | Create, modify, display, delete, disable/enable and list alert rules. |
| **Service** | Start, restart, stop or show the status of `telk-alert.service` / `telk-alert-agent.service`. |
| **About** | Version information. |

Pressing **Cancel/ESC** in any dialog returns to the main menu. **Ctrl+C** exits.

### Connection to Elasticsearch

| Setting | Description |
|---|---|
| **Hosts** | 1-10 master nodes (`https://host:port`). |
| **Certificate SSL** | CA certificate of the cluster (`.pem`/`.crt`). It is copied to `configuration/certs/ca.pem`. |
| **Authentication** | *HTTP Authentication* (user/password) or *API Key* (ID/key). Requires every host to use HTTPS. Values are typed hidden and stored encrypted; they are never displayed. |

Certificates are **always** verified: with the loaded CA, or with the public CAs (certifi) if there is none. If your cluster uses its own CA (for example, the one Elasticsearch generates when it is installed), load it.

### Alert rules

| Field | Description |
|---|---|
| **Name** | File name of the rule (`<name>.yaml`). It can't match an existing rule. |
| **Level** | `Low`, `Medium` or `High`. `High` alerts are sent first when the queue is busy. |
| **Index** | Index pattern (e.g. `winlogbeat-*`). |
| **Timestamp** | Date field used for the time range (e.g. `@timestamp` or `event.ingested`). |
| **Total Events** | Minimum number of events in the range to send the alert (1-100,000). |
| **Search Time** | How often the search is repeated (minutes ≤ 1440, hours ≤ 720, days ≤ 365). |
| **Range Time** | How far back the search looks. It must be greater than or equal to *Search Time*. |
| **Query** | Query string (e.g. `event.code: 4625`). |
| **Fields Selection** | Fields included in the message (up to 50). **Recommended:** it makes messages short, so several events fit in each one. |
| **Bot Token / Chat ID** | Telegram destination of the rule (typed hidden, stored encrypted). |

A disabled rule is renamed to `<name>.yaml.disabled` and Telk-Alert ignores it. Restart `telk-alert.service` after creating, modifying, deleting or enabling rules.

## Telk-Alert

### Alerts

Each alert contains the newest events of the range, grouped in as few messages as possible:

```
⚠️ Inicio_Fallido_Windows ⚠️

🚦 Alert level: High

⏰ Alert sent: Thu Nov 26 15:10:02 2026

17 event(s) were found (threshold: 1). New event(s) sent: 17.

EVENTS 1-17 OF 17 (1/1):

━━━━ Event 1 ━━━━
☑️ @timestamp = 2026-11-26T21:09:58Z
☑️ host.name = DC01
☑️ user.name = admin
...
```

- Events already sent are not sent again in the next cycles, even if the ranges overlap.
- If more than `MAX_EVENTS_PER_ALERT` events are found, the last message says how many were not sent.
- An event longer than a message is truncated and marked `(truncated)`.
- If the queue of a chat is full, lower-priority messages are dropped first and a notice tells how many.

### Settings (`Telk-Alert/modules/Constants_Class.py`)

| Constant | Default | Description |
|---|---|---|
| `MAX_EVENTS_PER_ALERT` | `50` | Events sent per alert. |
| `TELEGRAM_MAX_LENGTH` | `4000` | Maximum length of a message (Telegram's limit is 4096). |
| `TELEGRAM_SEND_INTERVAL` | `3.0` | Seconds between two messages to the same chat (20 per minute). |
| `MAX_QUEUE_SIZE` | `200` | Messages waiting per chat. |
| `MAX_SENT_IDS` | `5000` | Event IDs remembered per rule to avoid duplicates. |
| `HEARTBEAT_INTERVAL` | `60` | Seconds between heartbeat updates. |
| `RELAX_X509_STRICT` | `True` | Accept a cluster CA without RFC 5280 extensions (see [Troubleshooting](#troubleshooting)). |

### Behavior

- An error in one search (timeout, cluster restart) is logged and the rule keeps running in the next cycle.
- A rule that is invalid or whose credentials can't be decrypted is skipped (and reported by the agent); the others keep running.
- If no rule can start, the service exits with code 1 and systemd retries every 30 seconds.
- `systemctl stop` stops the rules cleanly; messages still in the queue are not sent (the log says how many).

## Telk-Alert-Agent

Every *frequency* (agent configuration), the agent checks:

| Situation | Notification | Action |
|---|---|---|
| Telk-Alert is not running | 🔴 | None: systemd restarts it after a failure (`Restart=on-failure`). A manual `systemctl stop` is respected. |
| A rule didn't run in 2 intervals + 1 minute, or the heartbeat is older than 3 minutes (2 consecutive checks) | 🟡 | Restarts Telk-Alert (polkit). |
| The restart failed | 🔴 | None (the message includes the error). |
| A rule couldn't start (invalid YAML, credentials) | 🟠 | None: fix the rule with Telk-Alert-Tool. |
| Everything works again | 🟢 | — |

Notifications are sent only when the status changes, so a long outage doesn't flood the chat.

Settings (`Telk-Alert-Agent/modules/Constants_Class.py`): `HEARTBEAT_MAX_AGE` (180 s) and `STALE_CHECKS_BEFORE_RESTART` (2).

## Files and permissions

| Path | Owner | Permissions | Content |
|---|---|---|---|
| `/opt/Telk-Alert-Suite/` (code, `.venv`) | `root:telk_alert` | read-only for the group | Code and virtual environment. The service can run them, never modify them. |
| `/opt/Telk-Alert-Suite/.poetry/` | `root:root` | `700` | Poetry (installer only). |
| `.../Telk-Alert/configuration/` | `telk_alert` | `700` / files `600` | `telk_alert.yaml`, `key`, `certs/ca.pem`. |
| `.../Telk-Alert-Agent/configuration/` | `telk_alert` | `700` / files `600` | `telk_alert_agent.yaml`. |
| `.../Telk-Alert/alert_rules/` | `telk_alert` | `750` / files `640` | Alert rules. |
| `/var/log/Telk-Alert/` | `telk_alert` | `750` | `telk-alert-log-<date>.log`, `telk-alert-agent-log-<date>.log`, `telk-alert-tool-log-<date>.log`. |
| `/run/telk-alert/heartbeat.yaml` | `telk_alert` | `600` | Heartbeat (created by systemd while the service runs). |
| `/etc/systemd/system/telk-alert*.service` | `root` | `644` | systemd units. |
| `/etc/polkit-1/rules.d/50-telk-alert-agent.rules` | `root` | `644` | Lets `telk_alert` restart `telk-alert.service` (only that). |
| `/usr/local/bin/telk-alert-tool` | `root` | `755` | Launcher of Telk-Alert-Tool. |

Logs are also available in journald: `journalctl -u telk-alert -f`, `journalctl -u telk-alert-agent -f`.

## Security

- **Encrypted secrets:** AES-256-GCM with a key derived by PBKDF2-HMAC-SHA256 (600,000 iterations) from the master key. Each secret is bound to its field (`telk_alert:api_key`, `telk_alert_rule:telegram_bot_token`, ...), so values can't be swapped inside or between files.
- **Secrets never displayed:** tokens, passwords and API Keys are typed hidden and, when modified, a new value is requested instead of showing the current one.
- **TLS always verified** and **authentication only over HTTPS**.
- **Least privilege:** the services run as `telk_alert` with systemd hardening (`NoNewPrivileges`, `ProtectSystem=strict`, no capabilities...). The only privileged action of the agent (restart Telk-Alert) is granted by polkit.
- **Code owned by root:** a compromised service can't modify the code that Telk-Alert-Tool later runs as root.
- **Validated input:** rule names can't escape the rules folder, files are validated on load and destructive operations never overwrite an existing rule.

## Troubleshooting

| Error | Cause | Solution |
|---|---|---|
| `media_type_header_exception ... Accept version must be either version 8 or 7, but found 9` | Client 9.x with an 8.x cluster. | In `pyproject.toml`: `elasticsearch = "^8.18.0"`, then `poetry lock` and `sudo ./telk_alert_installer.sh update`. |
| `elasticsearch-dsl (...) requires elasticsearch (>=8.0.0,<9.0.0)` (Poetry) | `elasticsearch-dsl` is no longer needed and conflicts with the 9.x client. | Remove `elasticsearch-dsl` from `pyproject.toml`. |
| `CERTIFICATE_VERIFY_FAILED ... unable to get local issuer certificate` | The cluster's CA isn't loaded. | Load it in **Configuration → Telk-Alert → Modify → Certificate SSL**. |
| `CERTIFICATE_VERIFY_FAILED ... CA cert does not include key usage extension` | Python ≥ 3.13 rejects CAs without RFC 5280 extensions. | Keep `RELAX_X509_STRICT = True`, or regenerate the CA with `keyUsage=keyCertSign,cRLSign`. |
| `Hostname mismatch, certificate is not valid for '...'` | The host in the configuration isn't in the certificate (e.g. `localhost`). | Use the name of the certificate; in a test machine, map it to `127.0.0.1` in `/etc/hosts`. |
| `Heartbeat not written ... /run/telk-alert/...` | Telk-Alert runs outside systemd, or the unit doesn't have `RuntimeDirectory=telk-alert`. | Install the unit of this version and run `systemctl daemon-reload`. |
| `Decryption / Authentication check failed: MAC check failed` | Credentials encrypted with another key or context. | Check the key file; type the credentials again with Telk-Alert-Tool. |
| Events that don't alert sometimes | They reach Elasticsearch after their `@timestamp` already left the range. | Use `event.ingested` as the rule's timestamp field (if your indexes have it), or a longer range time. |

Check the installed client version:

```bash
/opt/Telk-Alert-Suite/.venv/bin/python -m pip show elasticsearch | grep Version
```

## Upgrading from 4.1

```bash
sudo ./telk_alert_installer.sh update
```

- Code moves to a virtual environment in `/opt/Telk-Alert-Suite/.venv`; the key, configurations and rules of `/etc/Telk-Alert-Suite` are copied to `/opt/Telk-Alert-Suite`. Delete `/etc/Telk-Alert-Suite` manually once everything works.
- The `Telk-Alert-Tool` alias in `/root/.bashrc` is replaced by the `sudo telk-alert-tool` command.
- Secrets encrypted by 4.1 are still read (legacy format). Type them again with Telk-Alert-Tool to re-encrypt them with the new format.
- **Custom alert rules (Brute Force) were removed.** Existing ones run as normal rules: delete or convert them.
- The agent no longer starts Telk-Alert when it is stopped: systemd restarts it after a failure. Install the new units and the polkit rule.

## Changelog

### 4.2 - November 2026

**Telk-Alert**
- Credentials decrypted once per rule, with context; the passphrase is wiped from memory.
- An error in one search no longer stops the rule.
- One Telegram sending queue per chat, with priority by level and a bounded size.
- Events grouped in as few messages as possible, newest first, without duplicates between cycles.
- Exact total of events (alerts no longer depend on the number of documents retrieved).
- Validation of rules on load, clean shutdown (SIGTERM) and heartbeat for the agent.
- Runs as `telk_alert` with systemd hardening; no terminal interface dependencies.

**Telk-Alert-Agent**
- Heartbeat-based monitoring instead of counting threads (no more restart loops).
- Notifications only when the status changes, including the recovery.
- Restarts through polkit; no root privileges. APScheduler removed.

**Telk-Alert-Tool**
- Secrets typed hidden, validated and never displayed.
- Fixed: confirmations (yes/no), field forms and modification of rules with the new libraries.
- Rule names validated (no path traversal); existing rules are never overwritten.
- Range time validated against search time; limits for every number.
- Custom alert rules removed.

**Installer**
- Poetry-based virtual environment, Python 3.14, random master key, migration from 4.1 and `telk-alert-tool` command.
