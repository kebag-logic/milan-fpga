#!/usr/bin/env bash
# Run Python against exports of the LiteX stack revisions pinned in
# sw/litex/litex_pins.txt, ahead of whatever the base interpreter has installed.
# Usage: PINS=<dir with migen/ litex/ liteeth/ litedram/ litespi/ litex-boards/> \
#        BASEPY=<python with the remaining LiteX deps> pinned_py.sh <args...>
set -euo pipefail
: "${PINS:?set PINS}"; : "${BASEPY:?set BASEPY}"
export PYTHONPATH="$PINS/migen:$PINS/litex:$PINS/liteeth:$PINS/litedram:$PINS/litespi:$PINS/litex-boards${PYTHONPATH:+:$PYTHONPATH}"
export PYTHONDONTWRITEBYTECODE=1
exec "$BASEPY" -B "$@"
