#!/usr/bin/env bash
set -euo pipefail

cd -- "$(dirname -- "${BASH_SOURCE[0]}")"

INSTALL_DEV=false
INSTALL_PI=false
RUN_WIZARD=true

usage() {
    cat <<'EOF'
Usage: ./install.sh [OPTIONS]

Options:
  --pi          Also install Raspberry Pi GPIO dependencies (requirements-pi.txt)
  --dev         Also install development tools from pyproject.toml ([dependency-groups] dev)
  --no-wizard   Skip running tools/setup_wizard.py after installation
  -h, --help    Show this help message
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dev)
            INSTALL_DEV=true
            shift
            ;;
        --pi)
            INSTALL_PI=true
            shift
            ;;
        --no-wizard)
            RUN_WIZARD=false
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            usage >&2
            exit 1
            ;;
    esac
done

is_supported_python() {
    "$1" -c 'import sys; raise SystemExit(0 if (3, 11) <= sys.version_info[:2] < (3, 14) else 1)' >/dev/null 2>&1
}

PY_CMD=""
for candidate in python3.13 python3.12 python3.11 python3; do
    if command -v "$candidate" >/dev/null 2>&1 && is_supported_python "$candidate"; then
        PY_CMD="$candidate"
        break
    fi
done

if [[ -z "$PY_CMD" ]]; then
    echo "Python 3.11, 3.12, or 3.13 was not found." >&2
    if command -v python3 >/dev/null 2>&1; then
        echo "Detected $(python3 --version 2>&1), which is outside the supported range (>=3.11,<3.14)." >&2
    fi
    echo "Please install a supported Python version and try again." >&2
    exit 1
fi

echo "Using Python interpreter: $PY_CMD ($("$PY_CMD" --version 2>&1))"

if [[ ! -x ".venv/bin/python" ]]; then
    if ! "$PY_CMD" -c 'import venv, ensurepip' >/dev/null 2>&1; then
        echo "Error: Python venv/ensurepip support is missing for $PY_CMD." >&2
        echo "On Debian/Ubuntu, install the matching venv package (e.g. sudo apt install python3-venv) and retry." >&2
        exit 1
    fi
    echo ""
    echo "[1/3] Creating virtual environment (.venv)..."
    "$PY_CMD" -m venv .venv
else
    echo ""
    echo "[1/3] Existing virtual environment found (.venv)."
fi

VENV_PY=".venv/bin/python"

echo ""
echo "[2/3] Installing/updating Python dependencies..."
"$VENV_PY" -m pip install --upgrade pip
"$VENV_PY" -m pip install -r requirements.txt

if [[ "$INSTALL_PI" == true ]]; then
    echo "Installing Raspberry Pi dependencies (requirements-pi.txt)..."
    "$VENV_PY" -m pip install -r requirements-pi.txt
fi

if [[ "$INSTALL_DEV" == true ]]; then
    echo "Installing development tools (pyproject.toml [dependency-groups] dev)..."
    "$VENV_PY" -m pip install --group dev
fi

if [[ "$RUN_WIZARD" == true ]]; then
    echo ""
    echo "[3/3] Starting setup wizard..."
    "$VENV_PY" tools/setup_wizard.py
else
    echo ""
    echo "[3/3] Setup complete (--no-wizard)."
fi
