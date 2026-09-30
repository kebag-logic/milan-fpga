static int aem_loaded;
#define J(a, b) a##b
void nvm_boot_splice(void) { aem_\
loaded = 1; }
void nvm_boot_paste(void) { J(aem_, loaded) = 1; }
int read_it(void) { return aem_loaded; }
