# Load only: N endless CPU-bound jobs under make -j, inside the caller's CPU affinity.
N ?= 16
JOBS := $(addprefix spin-,$(shell seq 1 $(N)))
all: $(JOBS)
$(JOBS):
	@exec ./spin
.PHONY: all $(JOBS)
