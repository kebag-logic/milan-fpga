/* Host demonstration: a GCC alias of a file-scope static is the same object,
 * so a callee handed the alias's address overwrites the static's value.
 * build: cc -O2 -o demo alias_semantics_demo.c && ./demo  -> prints "aem_loaded=1" */
#include <stdio.h>
static int aem_loaded;
extern int aem_view __attribute__((alias("aem_loaded")));
static int __attribute__((noinline)) load_aem_image(void) { return 0; } /* CRC failed */
static void __attribute__((noinline)) nvm_boot(void) { (void)sscanf("1", "%d", &aem_view); }
int main(void)
{
	aem_loaded = load_aem_image();
	nvm_boot();
	printf("aem_loaded=%d\n", aem_loaded);
	return 0;
}
