/* Reviewer probe: lwSRP private allocation sizes the static pool must serve.
 * Each array's size (nm -S) equals the measured struct size. */
#include "core/mrp_mad.c"
char sz_attr_inst[sizeof(struct mrp_attr_inst)];
char sz_priv_one_port[sizeof(struct mrp_priv) + sizeof(struct mrp_port_state)];
#ifdef HAVE_MAP_WORK
char sz_map_work[sizeof(struct mrp_map_work)];
#endif
char sz_app[sizeof(struct mrp_app)];
char sz_app_ops[sizeof(struct mrp_app_ops)];
char sz_priv_header[sizeof(struct mrp_priv)];
