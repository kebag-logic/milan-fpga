# make -C <this dir> SUITE=<capture_coherence dir> WORK=<dir>: the hosted shape, a recipe run under make -C
repro:
	python3 $VALIDATION_STORAGE/617-a434-work/mf_repro.py $(SUITE) $(WORK) inherit
