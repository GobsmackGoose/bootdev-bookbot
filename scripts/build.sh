#!/bin/bash

set -e

run_inline_step() {
    local label="$1"
    shift
    echo -n "[BUILD] $label... "
    output_file=$(mktemp)
    if "$@" >"$output_file" 2>&1; then
        tr '\n' ' ' <"$output_file"
        echo
    else
        echo
        while IFS= read -r line; do
            echo "[ERROR] $line"
        done <"$output_file"
        rm -f "$output_file"
        exit 1
    fi
    rm -f "$output_file"
}

echo "[BUILD] Starting build process..."

for tool in black ruff python3; do
    if ! command -v $tool >/dev/null 2>&1; then
        echo "[ERROR] $tool not installed."
        exit 1
    fi
done

echo -n "[BUILD] Cleaning build artifacts... "
rm -rf bin/__pycache__ 2>/dev/null || true
echo "All done!"

run_inline_step "Applying formatting" black src/
run_inline_step "Applying linting" ruff check src/ --fix

echo -n "[BUILD] Building programs... "
export PYTHONPYCACHEPREFIX=bin/__pycache__
mkdir -p "$PYTHONPYCACHEPREFIX"
if find src/ -name "*.py" -exec python3 -m py_compile {} +; then
    echo "All done!"
else
    echo "[ERROR] Compilation failed!"
    exit 1
fi

echo "[BUILD] Finished build process successfully!"
