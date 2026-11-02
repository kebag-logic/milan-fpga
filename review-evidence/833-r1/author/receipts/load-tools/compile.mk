# Load only: N endless real compile loops under make -j, with their own disk output, inside the caller's CPU affinity.
N ?= 16
OBJ ?= $VALIDATION_STORAGE/833-a726/tmp/compile-load
JOBS := $(addprefix cc-,$(shell seq 1 $(N)))
all: $(JOBS)
$(JOBS):
	@mkdir -p $(OBJ); while :; do g++ -std=c++20 -O2 -c tu.cpp -o $(OBJ)/$@.o; done
.PHONY: all $(JOBS)
