include ../include/generated/variables.mak
include $(SOC_DIRECTORY)/software/common.mak

CFLAGS += -I$(BIOS_DIRECTORY)

OBJECTS = milan_baremetal.o

all: libmilan_baremetal.a

libmilan_baremetal.a: $(OBJECTS)
	$(AR) crs $@ $(OBJECTS)

-include $(OBJECTS:.o=.d)

%.o: $(LIBMILAN_BAREMETAL_DIRECTORY)/%.c
	$(compile)

.PHONY: all clean

clean:
	$(RM) $(OBJECTS) libmilan_baremetal.a .*~ *~
