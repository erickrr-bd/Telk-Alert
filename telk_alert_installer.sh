#!/usr/bin/env bash
set -euo pipefail

# Date: 26/09/2025 (Poetry-based installation: 24/11/2026)
# Author: Erick Roberto Rodriguez Rodriguez
# Installation script. Installs or updates Telk-Alert-Tool, Telk-Alert and Telk-Alert-Agent
# in a Poetry-managed virtual environment, so it does not depend on the system's Python packages.
#
# Usage: $ sudo ./telk_alert_installer.sh [install|update]
#
# Expected layout next to this script:
#   telk_alert_installer.sh
#   pyproject.toml          (and poetry.lock, recommended)
#   README.md               (optional)
#   telk-alert.service
#   telk-alert-agent.service
#   50-telk-alert-agent.rules
#   Telk-Alert-Suite/       (Telk-Alert-Tool, Telk-Alert, Telk-Alert-Agent)

if [ "$(id -u)" -ne 0 ]; then
	echo -e "\e[0;31m[-] Error: This script must be run as root or with sudo.\e[0m" >&2
	exit 1
fi

umask 022
clear 2>/dev/null || true

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$SCRIPT_DIR/Telk-Alert-Suite"

BASE_DIR="/opt/Telk-Alert-Suite"
TELK_ALERT_CONFIGURATION="$BASE_DIR/Telk-Alert/configuration"
TELK_ALERT_AGENT_CONFIGURATION="$BASE_DIR/Telk-Alert-Agent/configuration"
ALERT_RULES_FOLDER="$BASE_DIR/Telk-Alert/alert_rules"
TELK_ALERT_LOGS="/var/log/Telk-Alert"
TELK_ALERT_KEY="$TELK_ALERT_CONFIGURATION/key"

# Layout of versions <= 4.1 (configuration, key and alert rules under /etc). Migrated once, never deleted.
LEGACY_DIR="/etc/Telk-Alert-Suite"

SERVICE_USER="telk_alert"
SERVICE_GROUP="telk_alert"
SERVICES=("telk-alert-agent.service" "telk-alert.service")   # Stop order: agent first, so it doesn't restart the service.

VENV_DIR="$BASE_DIR/.venv"
VENV_PYTHON="$VENV_DIR/bin/python"
POETRY_HOME="$BASE_DIR/.poetry"                              # Private Poetry installation (root only).
POETRY_SPEC="poetry>=2.0.0,<3.0.0"
PYTHON_BIN="python3.14"                                      # Only this interpreter is used. Keep in sync with requires-python in pyproject.toml.

TOOL_ENTRY="$BASE_DIR/Telk-Alert-Tool/Telk_Alert_Tool.py"
TOOL_LAUNCHER="/usr/local/bin/telk-alert-tool"
SYSTEMD_DIR="/etc/systemd/system"
POLKIT_DIR="/etc/polkit-1/rules.d"

# Unit files and polkit rule of the project (next to this script).
TELK_ALERT_UNIT="$SCRIPT_DIR/telk-alert.service"
TELK_ALERT_AGENT_UNIT="$SCRIPT_DIR/telk-alert-agent.service"
POLKIT_RULE="$SCRIPT_DIR/50-telk-alert-agent.rules"

ok()   { echo -e "[*] \e[0;32m$*\e[0m"; }
warn() { echo -e "[*] \e[0;33m$*\e[0m"; }
fail() { echo -e "\e[0;31m[-] $*\e[0m" >&2; exit 1; }

trap 'echo -e "\e[0;31m[-] The installation stopped because of an error (line $LINENO).\e[0m" >&2' ERR

banner()
{
	echo "+------------------------------------------+"
	printf "| %-40s |\n" "$(date)"
	echo "|                                          |"
	printf "|\e[1m %-40s \e[0m|\n" "$@"
	echo "+------------------------------------------+"
}

show_header()
{
	# Box with the logo (centered) and the project's information. Only ASCII inside, so the padding is exact.
	local width=66 line left right border
	local logo=(
		" _____    _ _           _    _           _   "
		"|_   _|__| | | __      / \  | | ___ _ __| |_ "
		"  | |/ _ \ | |/ /____ / _ \ | |/ _ \ '__| __|"
		"  | |  __/ |   <_____/ ___ \| |  __/ |  | |_ "
		"  |_|\___|_|_|\_\   /_/   \_\_|\___|_|   \__|"
	)
	local labels=("Version" "Author" "Email" "GitHub")
	local values=("Telk-Alert v4.2 - November 2026" "Erick Roberto Rodriguez Rodriguez" "erodriguez@tekium.mx, erickrr.tbd93@gmail.com" "https://github.com/erickrr-bd/Telk-Alert")

	border="$(printf '═%.0s' $(seq 1 "$width"))"
	local Y="\e[1;33m" C="\e[1;36m" B="\e[1m" R="\e[0m"

	echo -e "${Y}╔${border}╗${R}"
	printf "${Y}║${R}%*s${Y}║${R}\n" "$width" ""
	# The logo is centered as a block (all its lines share the same left margin).
	local logo_width=0
	for line in "${logo[@]}"; do
		(( ${#line} > logo_width )) && logo_width=${#line}
	done
	left=$(( (width - logo_width) / 2 ))
	for line in "${logo[@]}"; do
		right=$(( width - left - ${#line} ))
		printf "${Y}║${R}%*s${C}%s${R}%*s${Y}║${R}\n" "$left" "" "$line" "$right" ""
	done
	line="Installer"
	left=$(( (width - ${#line}) / 2 ))
	right=$(( width - ${#line} - left ))
	printf "${Y}║${R}%*s${B}%s${R}%*s${Y}║${R}\n" "$left" "" "$line" "$right" ""
	printf "${Y}║${R}%*s${Y}║${R}\n" "$width" ""
	echo -e "${Y}╟$(printf '─%.0s' $(seq 1 "$width"))╢${R}"
	for i in "${!labels[@]}"; do
		printf "${Y}║${R}  ${B}%-8s${R}: %-*s${Y}║${R}\n" "${labels[$i]}" "$(( width - 12 ))" "${values[$i]}"
	done
	echo -e "${Y}╚${border}╝${R}"
	echo ''
}

show_header


# --- Helpers ------------------------------------------------------------------------------------

check_source()
{
	[ -d "$SRC_DIR" ] || fail "Folder not found: $SRC_DIR (run the installer from the downloaded project)."
	[ -f "$SCRIPT_DIR/pyproject.toml" ] || fail "File not found: $SCRIPT_DIR/pyproject.toml"
	if [ ! -f "$SCRIPT_DIR/poetry.lock" ]; then
		warn "poetry.lock not found: dependencies will be resolved now and may differ from other installations."
	fi
}

install_system_packages()
{
	# dialog: terminal interface. git: dependencies are installed from GitHub. gcc, headers and libcurl/OpenSSL: may be needed to build PycURL.
	if command -v apt-get > /dev/null 2>&1; then
		DEBIAN_FRONTEND=noninteractive apt-get update -qq
		DEBIAN_FRONTEND=noninteractive apt-get install -y -qq dialog git openssl gcc libcurl4-openssl-dev libssl-dev
		DEBIAN_FRONTEND=noninteractive apt-get install -y -qq python3.14 python3.14-venv python3.14-dev || warn "Python 3.14 is not available in the configured repositories."
	elif command -v dnf > /dev/null 2>&1; then
		dnf install -y -q dialog git openssl gcc libcurl-devel openssl-devel
		dnf install -y -q python3.14 python3.14-devel || warn "Python 3.14 is not available in the configured repositories."
	elif command -v yum > /dev/null 2>&1; then
		yum install -y -q dialog git openssl gcc libcurl-devel openssl-devel
		yum install -y -q python3.14 python3.14-devel || warn "Python 3.14 is not available in the configured repositories."
	elif command -v zypper > /dev/null 2>&1; then
		zypper --non-interactive install dialog git openssl gcc libcurl-devel libopenssl-devel
		zypper --non-interactive install python314 python314-devel || warn "Python 3.14 is not available in the configured repositories."
	elif command -v pacman > /dev/null 2>&1; then
		pacman -S --noconfirm --needed dialog git openssl gcc curl
		warn "Arch: install Python 3.14 (python or an AUR package) if it is not your default."
	else
		warn "Package manager not recognised. Make sure these are installed: dialog, git, openssl, gcc, Python 3.14 with its headers, libcurl and OpenSSL headers."
	fi
	for command_name in dialog git openssl; do
		command -v "$command_name" > /dev/null 2>&1 || fail "\"$command_name\" is required and is not installed."
	done
}

find_python()
{
	# Only Python 3.14 is accepted.
	if command -v "$PYTHON_BIN" > /dev/null 2>&1 && "$PYTHON_BIN" -c "import sys; sys.exit(0 if sys.version_info[:2] == (3, 14) else 1)" 2> /dev/null; then
		command -v "$PYTHON_BIN"
		return 0
	fi
	return 1
}

create_user()
{
	if getent group "$SERVICE_GROUP" > /dev/null; then
		warn "\"$SERVICE_GROUP\" group already exists"
	else
		groupadd -r "$SERVICE_GROUP"
		ok "\"$SERVICE_GROUP\" group created"
	fi
	if id -u "$SERVICE_USER" &> /dev/null; then
		warn "\"$SERVICE_USER\" user already exists"
	else
		useradd -r -M -s /bin/nologin -g "$SERVICE_GROUP" -d "$BASE_DIR" "$SERVICE_USER"
		ok "\"$SERVICE_USER\" user created"
	fi
}

deploy_code()
{
	# Copies the applications. The configuration and alert rules folders (and therefore the secrets) are never touched.
	mkdir -p "$BASE_DIR"
	tar -C "$SRC_DIR" --exclude='configuration' --exclude='alert_rules' --exclude='__pycache__' -cf - . | tar -C "$BASE_DIR" --no-same-owner -xf -
	cp -f "$SCRIPT_DIR/pyproject.toml" "$BASE_DIR/pyproject.toml"
	if [ -f "$SCRIPT_DIR/poetry.lock" ]; then
		cp -f "$SCRIPT_DIR/poetry.lock" "$BASE_DIR/poetry.lock"
	fi
	if [ -f "$SCRIPT_DIR/README.md" ]; then
		cp -f "$SCRIPT_DIR/README.md" "$BASE_DIR/README.md"
	fi
}

ensure_poetry()
{
	# Poetry is installed in its own virtual environment (no "curl | sh", no changes to the system's Python).
	if [ ! -x "$POETRY_HOME/bin/poetry" ]; then
		"$PYTHON" -m venv "$POETRY_HOME"
		"$POETRY_HOME/bin/python" -m pip install --quiet --upgrade pip
		"$POETRY_HOME/bin/python" -m pip install --quiet "$POETRY_SPEC"
	fi
}

run_poetry()
{
	(
		cd "$BASE_DIR"
		export POETRY_VIRTUALENVS_IN_PROJECT=true POETRY_VIRTUALENVS_CREATE=true POETRY_NO_INTERACTION=1
		"$POETRY_HOME/bin/poetry" "$@"
	)
}

install_python_dependencies()
{
	# $1 = install (uses poetry.lock when present) | update (updates the lock, including the libraries from GitHub).
	ensure_poetry
	run_poetry env use "$PYTHON" > /dev/null
	if [ "$1" = "update" ]; then
		run_poetry update --only main
	else
		run_poetry install --only main --no-root
	fi
	[ -x "$VENV_PYTHON" ] || fail "The virtual environment was not created: $VENV_PYTHON"
}

migrate_legacy_layout()
{
	# Versions <= 4.1 kept the key, the configurations and the alert rules under /etc/Telk-Alert-Suite.
	# They are copied (only if they don't exist yet in the new location) so the existing secrets can still be decrypted.
	[ -d "$LEGACY_DIR" ] || return 0
	local migrated=0 source_file target_file
	mkdir -p "$TELK_ALERT_CONFIGURATION" "$TELK_ALERT_AGENT_CONFIGURATION" "$ALERT_RULES_FOLDER"
	for pair in \
		"$LEGACY_DIR/Telk-Alert/configuration/key:$TELK_ALERT_KEY" \
		"$LEGACY_DIR/Telk-Alert/configuration/telk_alert.yaml:$TELK_ALERT_CONFIGURATION/telk_alert.yaml" \
		"$LEGACY_DIR/Telk-Alert-Agent/configuration/telk_alert_agent.yaml:$TELK_ALERT_AGENT_CONFIGURATION/telk_alert_agent.yaml"; do
		source_file="${pair%%:*}"
		target_file="${pair#*:}"
		if [ -f "$source_file" ] && [ ! -e "$target_file" ]; then
			cp -p "$source_file" "$target_file"
			migrated=$((migrated + 1))
		fi
	done
	if [ -d "$LEGACY_DIR/Telk-Alert/alert_rules" ]; then
		for source_file in "$LEGACY_DIR/Telk-Alert/alert_rules"/*.yaml "$LEGACY_DIR/Telk-Alert/alert_rules"/*.yaml.disabled; do
			[ -f "$source_file" ] || continue
			target_file="$ALERT_RULES_FOLDER/$(basename "$source_file")"
			if [ ! -e "$target_file" ]; then
				cp -p "$source_file" "$target_file"
				migrated=$((migrated + 1))
			fi
		done
	fi
	if [ "$migrated" -gt 0 ]; then
		ok "$migrated file(s) migrated from $LEGACY_DIR"
		warn "Check that everything works and then delete $LEGACY_DIR manually."
	fi
}

remove_legacy_alias()
{
	# Versions <= 4.1 created an alias in root's .bashrc (replaced by the telk-alert-tool command).
	if [ -f /root/.bashrc ] && grep -q "^alias Telk-Alert-Tool=" /root/.bashrc; then
		sed -i "/^alias Telk-Alert-Tool=/d" /root/.bashrc
		ok "Old \"Telk-Alert-Tool\" alias removed (use: sudo telk-alert-tool)"
	fi
}

create_folders_and_key()
{
	mkdir -p "$TELK_ALERT_CONFIGURATION" "$TELK_ALERT_AGENT_CONFIGURATION" "$ALERT_RULES_FOLDER" "$TELK_ALERT_LOGS"
	if [ ! -f "$TELK_ALERT_KEY" ]; then
		( umask 077; openssl rand -hex 32 > "$TELK_ALERT_KEY" )
		ok "Master key created securely"
	else
		warn "Master key file already exists, skipping generation"
	fi
}

apply_permissions()
{
	# Code and virtual environment: owned by root (the service user can read and run them, never modify them).
	chown -R root:"$SERVICE_GROUP" "$BASE_DIR"
	chmod -R g-w,o-rwx "$BASE_DIR"
	if [ -d "$POETRY_HOME" ]; then
		chown -R root:root "$POETRY_HOME"
		chmod -R go-rwx "$POETRY_HOME"
	fi

	# Configuration (secrets): only the service user (and root).
	chown -R "$SERVICE_USER":"$SERVICE_GROUP" "$TELK_ALERT_CONFIGURATION" "$TELK_ALERT_AGENT_CONFIGURATION"
	chmod 700 "$TELK_ALERT_CONFIGURATION" "$TELK_ALERT_AGENT_CONFIGURATION"
	find "$TELK_ALERT_CONFIGURATION" "$TELK_ALERT_AGENT_CONFIGURATION" -type f -exec chmod 600 {} +

	# Alert rules (encrypted Telegram credentials): service user, group can read (same permissions Telk-Alert-Tool applies).
	chown -R "$SERVICE_USER":"$SERVICE_GROUP" "$ALERT_RULES_FOLDER"
	chmod 750 "$ALERT_RULES_FOLDER"
	find "$ALERT_RULES_FOLDER" -type f -exec chmod 640 {} +

	# Logs.
	chown -R "$SERVICE_USER":"$SERVICE_GROUP" "$TELK_ALERT_LOGS"
	chmod 750 "$TELK_ALERT_LOGS"
}

install_launcher_and_units()
{
	# Command to open the configuration tool.
	cat > "$TOOL_LAUNCHER" <<LAUNCHER
#!/bin/sh
# Telk-Alert-Tool launcher (generated by telk_alert_installer.sh)
if [ "\$(id -u)" -ne 0 ]; then
	echo "Telk-Alert-Tool must be run as root: sudo telk-alert-tool" >&2
	exit 1
fi
exec "$VENV_PYTHON" "$TOOL_ENTRY" "\$@"
LAUNCHER
	chmod 755 "$TOOL_LAUNCHER"

	# systemd units: copied as they are from the project's files. Their ExecStart must use the virtual environment's Python.
	local unit_file
	for unit_file in "$TELK_ALERT_UNIT" "$TELK_ALERT_AGENT_UNIT"; do
		[ -f "$unit_file" ] || fail "Unit file not found: $unit_file"
		grep -q "^ExecStart=$VENV_PYTHON " "$unit_file" || fail "$unit_file must start with ExecStart=$VENV_PYTHON <script> (the dependencies are installed in that environment)."
		install -m 644 -o root -g root "$unit_file" "$SYSTEMD_DIR/$(basename "$unit_file")"
	done
	systemctl daemon-reload

	# polkit rule: lets the agent restart telk-alert.service (and only that unit).
	if [ -d "$POLKIT_DIR" ] && [ -f "$POLKIT_RULE" ]; then
		install -m 644 -o root -g root "$POLKIT_RULE" "$POLKIT_DIR/$(basename "$POLKIT_RULE")"
	else
		warn "polkit rule not installed: the agent will notify when Telk-Alert is down but will not be able to restart it."
	fi
}

verify_installation()
{
	# Imports every dependency as the service user, which also verifies the permissions.
	runuser -u "$SERVICE_USER" -- "$VENV_PYTHON" -I -c "import yaml, psutil, pycurl, dialog, Cryptodome, elasticsearch, elasticsearch.dsl, libPyUtils, libPyDialog, libPyLog, libPyTelegram, libPyConfiguration, libPyAgentConfiguration, libPyElk" \
		|| fail "A dependency could not be imported. Check the output above and that the libraries' repositories contain their pyproject.toml."
	ok "Dependencies verified"
}


# --- Main ---------------------------------------------------------------------------------------

opc="${1:-}"
if [ -z "$opc" ]; then
	read -r -p "Do you want to install or update Telk-Alert? (I/U): " opc
fi

case "${opc,,}" in
	i|install)
		check_source

		banner "Installing system packages"
		echo ''
		install_system_packages
		PYTHON="$(find_python)" || fail "Python 3.14 (python3.14) was not found. Install it (Ubuntu: ppa:deadsnakes/ppa; Fedora: dnf install python3.14) and run the installer again."
		"$PYTHON" -c "import venv, ensurepip" 2> /dev/null || fail "The \"venv\" module of $PYTHON is not available (Debian/Ubuntu: apt install python3.14-venv)."
		ok "Using $PYTHON ($("$PYTHON" -V 2>&1))"
		echo ''

		banner "Creating user and group"
		echo ''
		create_user
		echo ''

		banner "Installing Telk-Alert"
		echo ''
		deploy_code
		ok "Installation files copied"
		install_python_dependencies install
		ok "Python environment created: $VENV_DIR"
		echo ''

		banner "Creation of folders and files"
		echo ''
		migrate_legacy_layout
		create_folders_and_key
		ok "Folders and files created"
		echo ''

		banner "Change of permissions and owner"
		echo ''
		apply_permissions
		install_launcher_and_units
		remove_legacy_alias
		verify_installation
		ok "Permissions applied successfully"
		echo ''

		echo -e "[*] Next steps:"
		echo -e "    1. Configure Telk-Alert, the agent and the alert rules:   \e[1msudo telk-alert-tool\e[0m"
		echo -e "    2. Start the services from the tool, or: \e[1msudo systemctl enable --now telk-alert.service telk-alert-agent.service\e[0m\n"
		;;
	u|update)
		check_source
		[ -d "$BASE_DIR" ] || fail "Telk-Alert is not installed in $BASE_DIR. Choose the install option."

		banner "Updating Telk-Alert"
		echo ''
		install_system_packages
		PYTHON="$(find_python)" || fail "Python 3.14 (python3.14) was not found. Install it (Ubuntu: ppa:deadsnakes/ppa; Fedora: dnf install python3.14) and run the installer again."
		create_user

		# Remember which services were running, stop them and start them again at the end.
		ACTIVE_SERVICES=()
		for unit in "${SERVICES[@]}"; do
			if systemctl is-active --quiet "$unit"; then
				ACTIVE_SERVICES+=("$unit")
			fi
		done
		for unit in ${ACTIVE_SERVICES[@]+"${ACTIVE_SERVICES[@]}"}; do
			systemctl stop "$unit"
		done

		deploy_code
		ok "Installation files updated (configuration, key and alert rules were not modified)"
		install_python_dependencies update
		ok "Python environment updated"
		migrate_legacy_layout
		create_folders_and_key
		apply_permissions
		install_launcher_and_units
		remove_legacy_alias
		verify_installation

		# Start in the reverse order of the stop: service first, then the agent.
		for ((i=${#ACTIVE_SERVICES[@]}-1; i>=0; i--)); do
			systemctl start "${ACTIVE_SERVICES[$i]}"
			ok "${ACTIVE_SERVICES[$i]} started"
		done
		ok "Update completed"
		echo ''
		;;
	*)
		fail "Invalid option selected. Exiting."
		;;
esac