/* SPDX-License-Identifier: (GPL-2.0 OR MIT) */
/* Stub for the BIOS command registry: each handler becomes a named pointer
 * the harness can call, so the firmware's static functions stay static. */
#ifndef COMMAND_H
#define COMMAND_H
#define SYSTEM_CMDS 0
typedef void (*cmd_handler)(int nb_params, char **params);
#define define_command(cmd_name, handler, help_txt, group_id) \
	cmd_handler const nvm_host_cmd_##cmd_name = handler
#endif
