# The split store's flash path at f3e902f2: its own LiteSPI port, never the processor or KL_nvm_backend

The only two matches below are comments naming the all-fabric placement's writers; no code in the store names the processor or the backend.

$ git grep -n "KL_nvm_backend\|protocol_processor\|pp_shadow\|ppmem\|nvm_dev_\|dev_region" -- sw/firmware/ctrl_nvm ":!*.md"
sw/firmware/ctrl_nvm/nvm_layout3.h:25: * (KL_nvm_backend.sv, milan_baremetal.c); nothing there reads this file.
sw/firmware/ctrl_nvm/nvm_shape.h:10: * today's journal (milan_baremetal.c, KL_nvm_backend.sv). This store never
(rc=0 : 1 is no match)

$ grep -n "f->read\|f->program\|f->erase\|f->busy\|flash->" sw/firmware/ctrl_nvm/nvm_store.c
112:	return nvm.flash->now_us(nvm.flash->ctx);
182:	if (nvm.flash->read(nvm.flash->ctx, addr, dst, len))
305:	if (f->read(f->ctx, nvm_slot_addr(slot), nvm_stage, NVM_IMG_LEN))
415:		if (f->read(f->ctx, NVM_LEGACY_A + i * slot, nvm_chunk, NVM_KLJ_HDR) == 0 &&
689:	    f->erase(f->ctx, nvm_slot_addr(nvm.target) + nvm.block * NVM_ERASE_BLOCK)) {
702:	int busy = f->busy(f->ctx);
717:	if (f->read(f->ctx, nvm_slot_addr(nvm.target) + nvm.pos, nvm_chunk, n))
743:	if (f->program(f->ctx, nvm_slot_addr(nvm.target) + nvm.pos, nvm_stage + nvm.pos, n)) {

$ grep -n "spiflash_master_\|SPIFLASH_BASE\|ls_in_journal" sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c
110:		if (spiflash_master_status_read() & bit)
124:	while (spiflash_master_status_read() & LS_RX_READY) {
127:		spiflash_master_rxtx_read();
129:	spiflash_master_phyconfig_write(
133:	spiflash_master_cs_write(1);
142:	spiflash_master_rxtx_write(out);
145:	return (int)(spiflash_master_rxtx_read() & 0xffu);
150:	spiflash_master_cs_write(0);
179:static int ls_in_journal(uint32_t addr, uint32_t len)
188:	const volatile uint8_t *src = (const volatile uint8_t *)(SPIFLASH_BASE + addr);
207:	    !ls_in_journal(addr, len))
222:	if (!ls_in_journal(base, LS_BLOCK))
