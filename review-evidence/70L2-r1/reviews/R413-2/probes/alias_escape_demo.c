/* R413-2: a GNU alias of the verdict static, its address handed to sscanf()
 * inside nvm_boot(). No C-level `&aem_loaded`, no store to it in this unit;
 * the write is made by the library. Mirrors plants.py alias_sscanf. */
#include <stdio.h>
static int aem_loaded;
extern int milan_r413_alias __attribute__((alias("aem_loaded")));
__attribute__((noinline)) static int load_aem_image(void) { return 0; } /* CRC failed */
__attribute__((noinline)) static void nvm_boot(void)
{
	(void)sscanf("1", "%d", &milan_r413_alias);
}
__attribute__((noinline)) static void entity_advertise(int verified)
{
	printf("entity_advertise(verified=%d): %s\n", verified,
	       verified ? "ENABLE WRITTEN" : "entity stays disabled");
}
void milan_init(void)
{
	aem_loaded = load_aem_image();
	nvm_boot();
	entity_advertise(aem_loaded);
}
#ifdef HOST_MAIN
int main(void) { milan_init(); return 0; }
#endif
