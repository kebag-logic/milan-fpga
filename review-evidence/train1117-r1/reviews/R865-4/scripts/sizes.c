/* Reviewer probe: lwSRP's allocation sizes, printed by the compiler's diagnostics (compile only), to place them in
   the SRP pool's classes (64, 256, 512 bytes). Build with -m32 for the ILP32 target's sizes. */
#include "core/mrp_mad.c"
char (*size_attr_inst)[sizeof(struct mrp_attr_inst)] = 1;
char (*size_map_work)[sizeof(struct mrp_map_work)] = 1;
char (*size_priv)[sizeof(struct mrp_priv)] = 1;
char (*size_port_state)[sizeof(struct mrp_port_state)] = 1;
char (*size_app)[sizeof(struct mrp_app)] = 1;
char (*size_app_ops)[sizeof(struct mrp_app_ops)] = 1;
