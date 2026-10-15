/* Exec a named file through the 32-bit (int 0x80) or x32 system-call entry, from a 64-bit process. */
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>
int main(int argc, char **argv) {
    char *m = mmap(0, 4096, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS | MAP_32BIT, -1, 0);
    strcpy(m, argv[2]);
    unsigned int *vector = (unsigned int *)(m + 1024), *env = vector + 8;
    vector[0] = (unsigned int)(unsigned long)m; vector[1] = 0; env[0] = 0;
    long ret;
    if (argv[1][0] == 'i') {
        __asm__ volatile("int $0x80" : "=a"(ret) : "a"(11), "b"((unsigned int)(unsigned long)m),
                         "c"((unsigned int)(unsigned long)vector), "d"((unsigned int)(unsigned long)env) : "memory");
    } else {
        ret = syscall(0x40000000L | 520, m, vector, env);
    }
    return 99;
}
