/* Production composite source, deterministic peripheral contract. */
#include <stdio.h>
#include "fx3_model.h"
#include "usb_audio_desc.h"
static const char *label="BOOT";
static unsigned checks;
#define CHECK(x) do { ++checks; if (!(x)) { printf("FAIL %s line %u\n",label,__LINE__); exit(1); } } while (0)
#undef CyU3PSetEpConfig
#undef CyU3PUsbSendEP0Data
#undef CyU3PUsbAckSetup
#undef CyU3PUsbStall
#undef CyU3PGpifSMStart
#undef CyU3PUsbRegisterSetupCallback
#undef CyU3PMutexGet
#undef CyU3PMutexPut
#define CY_U3P_USB_EP_ISO 1
#define CY_U3P_DMA_TYPE_MANUAL 1
#define CY_U3P_DMA_TYPE_AUTO 2
#define CY_U3P_DMA_CB_CONS_EVENT 2
static CyU3PEpConfig_t eps[256];
static uint8_t ep0[256];
static unsigned sent, acked, stalled, gpif_running, starts, packet_mode, fast_enum;
static unsigned control_locked;
static int CyU3PMutexGet(CyU3PMutex *m, uint32_t wait) { (void)m;(void)wait;CHECK(!control_locked);control_locked=1;return 0; }
static int CyU3PMutexPut(CyU3PMutex *m) { (void)m;CHECK(control_locked);control_locked=0;return 0; }
static int CyU3PSetEpConfig(uint8_t ep, CyU3PEpConfig_t *c) { eps[ep]=*c; return 0; }
static int CyU3PUsbSendEP0Data(uint16_t n,uint8_t *p) { CHECK(!control_locked);CHECK(n<=256); memcpy(ep0,p,n);sent=n;return 0; }
static int CyU3PUsbAckSetup(void) { ++acked;return 0; }
static int CyU3PUsbStall(int ep,int on,int reset) { (void)ep;(void)on;(void)reset;++stalled;return 0; }
static int CyU3PGpifSMStart(int a,int b) { (void)a;(void)b;gpif_running=1;++starts;return 0; }
static void CyU3PGpifDisable(int force) { (void)force;gpif_running=0; }
static int CyU3PUsbSetEpPktMode(int ep,int mode) { CHECK(ep==UA_FROM_HOST_EP);packet_mode=mode;return 0; }
static void CyU3PUsbRegisterSetupCallback(CyBool_t (*f)(uint32_t,uint32_t),int fast) { (void)f;fast_enum=fast; }
#define UA_AUDIO_FUNCTION
#define main firmware_main
#include "fx3_main.c"
#undef main

static void model_advance(unsigned us) { model_us+=us; }
static int CyU3PDmaChannelCreate(CyU3PDmaChannel *ch,int type,CyU3PDmaChannelConfig_t *cfg)
{
    CHECK(!ch->live); memset(ch,0,sizeof *ch);ch->live=1;
    ch->size=cfg->size;ch->count=cfg->count;ch->prod=cfg->prodSckId;ch->cons=cfg->consSckId;ch->type=type;
    return 0;
}
static int CyU3PDmaChannelDestroy(CyU3PDmaChannel *ch) { CHECK(ch->live); memset(ch,0,sizeof *ch);return 0; }
static int CyU3PDmaChannelReset(CyU3PDmaChannel *ch)
{ CHECK(ch->live);ch->queued=ch->fetched=ch->active=0;return 0; }
static int CyU3PDmaChannelGetBuffer(CyU3PDmaChannel *ch,CyU3PDmaBuffer_t *b,unsigned wait)
{
    (void)wait;CHECK(ch->live);if(!ch->queued)return CY_U3P_ERROR_TIMEOUT;
    CHECK(!ch->fetched);ch->fetched=1;b->buffer=ch->bytes[0];b->count=ch->lengths[0];b->size=ch->size;return 0;
}
static int CyU3PDmaChannelDiscardBuffer(CyU3PDmaChannel *ch)
{
    CHECK(ch->fetched && ch->queued);--ch->queued;ch->fetched=0;
    memmove(ch->bytes,ch->bytes+1,(size_t)ch->queued*sizeof ch->bytes[0]);
    memmove(ch->lengths,ch->lengths+1,(size_t)ch->queued*sizeof ch->lengths[0]);return 0;
}
static uint8_t capture_bytes[4096];
static unsigned capture_length;
static int CyU3PDmaChannelCommitBuffer(CyU3PDmaChannel *ch,uint16_t n,unsigned flags)
{
    (void)flags;CHECK(ch==&au_capture); CHECK(n==ch->lengths[0]);
    memcpy(capture_bytes,ch->bytes[0],n);capture_length=n;
    return CyU3PDmaChannelDiscardBuffer(ch);
}
static int CyU3PDmaChannelSetupSendBuffer(CyU3PDmaChannel *ch,CyU3PDmaBuffer_t *b)
{
    CHECK(ch->live && !ch->active && b->count<=b->size);
    ch->sending=b->buffer;ch->length=b->count;ch->active=1;ch->completed=0;return 0;
}
static int CyU3PDmaChannelWaitForCompletion(CyU3PDmaChannel *ch,unsigned wait)
{ (void)wait;CHECK(ch->live);return ch->completed?CY_U3P_SUCCESS:CY_U3P_ERROR_TIMEOUT; }
static void finish(CyU3PDmaChannel *ch) { ch->active=0;ch->completed=1; }
static void queue(CyU3PDmaChannel *ch,const uint8_t *p,unsigned n)
{ CHECK(ch->live && ch->queued<16 && n<=2048);memcpy(ch->bytes[ch->queued],p,n);ch->lengths[ch->queued++]=(uint16_t)n; }
static void status_record(unsigned seq)
{
    uint8_t p[20]={0x41,0x55,0,0,8,0,6,0,0x80,0xbb,0,0,1,0,0,0,0,0,0,0};
    p[2]=(uint8_t)seq;p[3]=(uint8_t)(seq>>8);p[14]=(uint8_t)UA_CONFIG_DIGEST;p[15]=(uint8_t)(UA_CONFIG_DIGEST>>8);
    p[16]=(uint8_t)au_capture_epoch;p[17]=(uint8_t)(au_capture_epoch>>8);p[18]=(uint8_t)(au_capture_epoch>>16);p[19]=(uint8_t)(au_capture_epoch>>24);
    queue(&au_status,p,20);
}
static void request(unsigned bm,unsigned req,unsigned val,unsigned idx,unsigned len)
{ sent=acked=stalled=0;CHECK(setup_cb(bm | req<<8 | val<<16,idx | len<<16)); }
int main(void)
{
    unsigned i;
    channel(&ch_to_fpga,CY_U3P_DMA_TYPE_MANUAL_OUT,0,0,0,UA_NET_FROM_HOST_SOCKET,0,NULL);
    gpif_init(); audio_boot(); usb_init();
    event_cb(CY_U3P_USB_EVENT_SETCONF,1);
    request(0x40,0xb1,0,0,0);
    status_record(0); audio_service();
    CHECK(au_render.active); finish(&au_render); audio_service();
    request(1,11,1,UA_IF_AS_TO_HOST,0);
    CHECK(au_capture_wait);
    audio_service(); CHECK(au_render.active); finish(&au_render);
    status_record(1); audio_service();
    CHECK(au_capture_live && !au_out_live && !au_render.active);
    for(i=0;i<8192;i++) {
        model_advance(125);
        status_record(i+2);
        audio_service();
        CHECK(au_capture_live && !au_out_live);
        CHECK(!au_render.active && !au_state_pending);
    }
    puts("PASS CAPTURE_ONLY_NO_INTERVAL_RECORD: 8192 service intervals, no socket 3 record");
    return 0;
}
