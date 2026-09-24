void sink(unsigned int);
void f(void) {
#ifdef MILAN_NEVER_DEFINED
#if·x
#endif
	*(volatile unsigned int *)0x90000600u = 1u;
#ifdef MILAN_NEVER_DEFINED
#endif·y
#endif
}
