#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ "$#" -lt 1 ]; then
	echo
	echo "usage: $0 <resume_filename>-src.yaml [--company-details] [--stack]"
	echo
	exit 1
fi

# ── Detect system package manager ────────────────────────────────────────────
PKG_INSTALL=""
if command -v pacman &>/dev/null; then
	PKG_INSTALL="sudo pacman -S --noconfirm"
elif command -v apt &>/dev/null; then
	PKG_INSTALL="sudo apt install -y"
elif command -v brew &>/dev/null; then
	PKG_INSTALL="brew install"
fi

# ── python3 ───────────────────────────────────────────────────────────────────
if ! command -v python3 &>/dev/null; then
	echo "python3 not found. Attempting to install..." >&2
	if [ -n "$PKG_INSTALL" ]; then
		$PKG_INSTALL python3
	else
		echo "Error: please install python3 manually." >&2
		exit 1
	fi
fi

# ── pip ───────────────────────────────────────────────────────────────────────
PIP=""
if command -v pip3 &>/dev/null; then
	PIP="pip3"
elif python3 -m pip --version &>/dev/null 2>&1; then
	PIP="python3 -m pip"
else
	echo "pip not found. Attempting to install..." >&2
	if command -v pacman &>/dev/null; then
		sudo pacman -S --noconfirm python-pip
		PIP="pip3"
	elif command -v apt &>/dev/null; then
		$PKG_INSTALL python3-pip
		PIP="pip3"
	elif command -v brew &>/dev/null; then
		$PKG_INSTALL python3 # Homebrew python3 includes pip3
		PIP="pip3"
	elif python3 -m ensurepip --upgrade &>/dev/null 2>&1; then
		PIP="python3 -m pip"
	elif python3 -m ensurepip --upgrade --break-system-packages &>/dev/null 2>&1; then
		PIP="python3 -m pip"
	else
		echo "Error: could not install pip. Please install it manually." >&2
		exit 1
	fi
fi

# ── PyYAML ────────────────────────────────────────────────────────────────────
if ! python3 -c "import yaml" &>/dev/null 2>&1; then
	echo "PyYAML not found. Installing..."
	installed=false
	if command -v pacman &>/dev/null; then
		$PKG_INSTALL python-yaml && installed=true
	fi
	if ! $installed; then
		$PIP install --quiet pyyaml 2>/dev/null && installed=true ||
			$PIP install --quiet --break-system-packages pyyaml 2>/dev/null && installed=true
	fi
	if ! $installed; then
		echo "Error: could not install PyYAML. Please install it manually." >&2
		exit 1
	fi
fi

# ── Liberation Serif font (for consistent PDF rendering) ─────────────────────
if ! fc-list | grep -i "liberation serif" &>/dev/null; then
	echo "Liberation Serif font not found. Attempting to install..." >&2
	if [ -n "$PKG_INSTALL" ]; then
		if command -v pacman &>/dev/null; then
			$PKG_INSTALL ttf-liberation
		else
			$PKG_INSTALL fonts-liberation
		fi
		fc-cache -f
	else
		echo "Warning: Liberation Serif not found — PDF fonts may differ. Install 'fonts-liberation' manually." >&2
	fi
fi

if ! command -v brave &>/dev/null; then
	echo "Warning: 'brave' not found — PDF will not be generated." >&2
fi

python3 "$SCRIPT_DIR/generate-resume.py" "$@"
