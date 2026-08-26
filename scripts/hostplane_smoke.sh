#!/bin/sh
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Run the product UART smoke from a bench workstation after programming.

if [ -z "${MILAN_UART:-}" ]; then
    echo "HOSTPLANE SMOKE: FAIL (MILAN_UART is required)" >&2
    exit 2
fi

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
exec python3 "$SCRIPT_DIR/baremetal_uart_smoke.py" --port "$MILAN_UART" \
    --baud "${MILAN_UART_BAUD:-115200}" \
    --timeout "${MILAN_UART_TIMEOUT:-5}"
