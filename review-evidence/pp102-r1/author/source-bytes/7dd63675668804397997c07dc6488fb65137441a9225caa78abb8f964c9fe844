# SPDX-License-Identifier: CERN-OHL-W-2.0
# Diagram regeneration + documentation lint.
# Targets: diagrams (drawio -> svg), lint (mermaid+wavedrom blocks), stale (export freshness).

DRAWIO      ?= drawio
DRAWIO_SRC  := $(wildcard docs/diagrams/src/*.drawio)
DRAWIO_SVG  := $(patsubst docs/diagrams/src/%.drawio,docs/diagrams/%.svg,$(DRAWIO_SRC))

.PHONY: all check diagrams wavedrom wavedrom-check lint links matrix modmatrix stale
all: diagrams check

# everything CI should enforce (see docs/architecture/09_verification.md section 7)
check: lint wavedrom-check links matrix modmatrix stale

diagrams: $(DRAWIO_SVG) wavedrom

# render every embedded ```wavedrom block to its committed SVG (GitHub cannot
# render WaveDrom natively; bootstraps .venv-wavedrom on first run)
wavedrom:
	@python3 scripts/render-wavedrom.py

wavedrom-check:
	@python3 scripts/render-wavedrom.py --check

docs/diagrams/%.svg: docs/diagrams/src/%.drawio
	@$(DRAWIO) -x -f svg --crop -o $@ $< 2>/dev/null \
	  || xvfb-run -a $(DRAWIO) --no-sandbox -x -f svg --crop -o $@ $<
	@echo "exported $@"

lint:
	@./scripts/lint-diagrams.sh

links:
	@python3 scripts/check-links.py

matrix:
	@python3 scripts/check-matrix.py

# the module<->testbench matrix is GENERATED; drift and an untested module both fail
modmatrix:
	@python3 scripts/gen_matrix.py --check

# Staleness must be meaningful on a fresh checkout too: git does not preserve
# mtimes, so committed files are compared by last-commit time; the mtime test
# only applies when the SOURCE has uncommitted edits (where mtime is truth).
stale:
	@fail=0; \
	for src in $(DRAWIO_SRC); do \
	  svg="docs/diagrams/$$(basename $${src%.drawio}).svg"; \
	  if [ ! -f "$$svg" ]; then echo "STALE: $$svg (missing)"; fail=1; continue; fi; \
	  if git diff --quiet -- "$$src" 2>/dev/null; then \
	    st=$$(git log -1 --format=%ct -- "$$src"); \
	    gt=$$(git log -1 --format=%ct -- "$$svg"); \
	    if [ -n "$$st" ] && [ -n "$$gt" ] && [ "$$st" -gt "$$gt" ]; then \
	      echo "STALE: $$svg (source committed after the export)"; fail=1; \
	    fi; \
	  elif [ "$$src" -nt "$$svg" ]; then \
	    echo "STALE: $$svg (uncommitted source edit newer than the export)"; fail=1; \
	  fi; \
	done; exit $$fail
