#define R 0x600u
_Pragma("push_macro(\"R\")")
#undef R
#define R 0x604u
int x = R;
_Pragma("pop_macro(\"R\")")
int y = R;
