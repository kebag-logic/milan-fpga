/* SPDX-License-Identifier: Apache-2.0 */
/* Public operations drive every event. Internal readback checks ownership bytes. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "shish_lan/msrp.h"
#include "fault_alloc.h"
#include "core/mrp_mad.c"
static unsigned checks, cases, current, focus, seen_leave, seen_join, seen_map;
static uint8_t indicated[48], policy_value[48];
static uint32_t (*original_leave)(const struct mrp_app *,uint8_t,uint8_t,const void *);
#define CHECK(x) do { ++checks; if (!(x)) { fprintf(stderr,"FAIL case=%u line=%u: %s\n",current,__LINE__,#x); exit(1); } } while (0)
static void join_capture(struct mrp_app *a,uint8_t p,uint8_t t,const void *v,bool n)
{ (void)a;(void)v;(void)n;if(p==0&&t==focus)++seen_join; }
static void leave_capture(struct mrp_app *a,uint8_t p,uint8_t t,const void *v)
{ if(p==0&&t==focus){++seen_leave;memcpy(indicated,v,attr_store_len(a->ops,t));} }
static uint32_t leave_policy(const struct mrp_app *a,uint8_t p,uint8_t t,const void *v)
{ if(p==0&&t==focus){++seen_map;memcpy(policy_value,v,attr_store_len(a->ops,t));}return original_leave(a,p,t,v); }
static int send_accept(void *x,uint8_t p,const uint8_t *b,size_t n)
{(void)x;(void)p;(void)b;(void)n;return 0;}
static int send_refuse(void *x,uint8_t p,const uint8_t *b,size_t n)
{(void)x;(void)p;(void)b;(void)n;return -77;}
static size_t wire(uint8_t *b,unsigned type,unsigned value,unsigned ev,unsigned la)
{
 unsigned n=type==1?25:type==2?34:8,list=2+n+1+(type==3)+2;
 memset(b,0,80);b[1]=type;b[2]=n;b[4]=list;b[5]=la?32:0;b[6]=1;
 b[7]=0x11;b[14]=1;
 if(type==3)b[16]=value<<6;
 else {b[15]=1;b[20]=9;b[22]=2;b[23]=value>>8;b[24]=value;b[26]=2;b[27]=0x70;b[28]=0x12;b[31]=0x34;if(type==2){memset(b+32,0x5a,8);b[40]=7;}}
 b[7+n]=36*ev;return list+7;
}
static struct mrp_app *setup(unsigned type)
{
 struct msrp_ctx ctx={0};struct mrp_app *base=msrp_app_create(3,&ctx);CHECK(base);
 struct mrp_app_ops ops=*base->ops;original_leave=ops.map_leave;
 ops.join_ind=join_capture;ops.leave_ind=leave_capture;ops.map_leave=leave_policy;ops.ctx=NULL;
 mrp_app_destroy(base);struct mrp_app *a=mrp_app_create(&ops,3);CHECK(a);
 for(unsigned p=0;p<3;p++){CHECK(mrp_port_configure(a,p,20,60,10000,1,true)==0);mrp_set_periodic(a,p,false);}
 focus=type;seen_leave=seen_join=seen_map=0;memset(indicated,0,48);memset(policy_value,0,48);
 if(type==3){uint8_t b[80];size_t n=wire(b,1,100,1,0);CHECK(mrp_rx(a,0,b,n)==0);CHECK(mrp_rx(a,1,b,n)==0);}
 return a;
}
static struct mrp_attr_inst *instance(struct mrp_app *a,unsigned port,unsigned type)
{ for(struct mrp_attr_inst *i=priv_of(a)->ports[port].attrs;i;i=i->next)if(i->attr_type==type)return i;return NULL; }
static void finish(struct mrp_app *a)
{allocation_fail_after(0);mrp_app_destroy(a);CHECK(allocation_live()==0);shlan_timer_tick();cases++;}
static void sweep(void)
{
 for(unsigned type=1;type<=3;type++)for(unsigned lv=0;lv<2;lv++)for(unsigned fault=1;fault<=3;fault++)for(unsigned action=0;action<14;action++){
  current++;struct mrp_app *a=setup(type);uint8_t b[80],target_tx[256],source_tx[256];
  unsigned old=type==3?2:100,other=type==3?1:200;size_t n=wire(b,type,old,1,0);
  CHECK(mrp_rx(a,0,b,n)==0);struct mrp_attr_inst *i=instance(a,0,type);CHECK(i);
  size_t size=attr_store_len(a->ops,type);uint8_t saved[48]={0};memcpy(saved,i->attr_val,size);
  /* Force a real retained destination even for the Listener route. */
  CHECK(mrp_mad_join(a,2,type,saved,false)==0);
  CHECK(mrp_transmit(a,2,target_tx,sizeof(target_tx),send_refuse,NULL)==-77);
  if(lv){n=wire(b,type,old,4,1);CHECK(mrp_rx(a,0,b,n)==0);}
  seen_leave=seen_join=seen_map=0;allocation_fail_after(fault);mrp_port_role_change(a,0,true);
  CHECK(allocation_failures()==1);CHECK(i->reg==MRP_REG_STATE_LV);CHECK(i->flush_pending);CHECK(!memcmp(i->flush_value,saved,size));
  CHECK(i->leave_timer.cs==1);CHECK(seen_leave==0);allocation_fail_after(0);
  if(type==3){n=wire(b,1,100,1,0);CHECK(mrp_rx(a,0,b,n)==0);}
  n=wire(b,type,other,1,0);_Alignas(max_align_t) uint8_t changed[48]={0};
  CHECK(a->ops->decode_attr(type,0,b+7,b[2],changed)==b[2]);if(type==3)changed[8]=other;
  if(action==0||action==1){CHECK(mrp_mad_join(a,0,type,changed,action==1)==0);CHECK(!memcmp(i->attr_val,changed,size));}
  if(action==2){CHECK(mrp_rx(a,1,b,n)==0);CHECK(!memcmp(i->attr_val,changed,size));}
  if(action==3){
   CHECK(mrp_transmit(a,0,source_tx,sizeof(source_tx),send_refuse,NULL)==-77);
   CHECK(mrp_rx(a,1,b,n)==0);CHECK(priv_of(a)->ports[0].map_head);
   CHECK(!memcmp(i->attr_val,saved,size));
   CHECK(mrp_rx(a,0,b,n)==-SHLAN_ERROR_INVALID);
   allocation_fail_after(fault);shlan_timer_tick();CHECK(allocation_failures()==1);allocation_fail_after(0);
   CHECK(mrp_transmit(a,0,source_tx,sizeof(source_tx),send_accept,NULL)==1);CHECK(!memcmp(i->attr_val,changed,size));
  }
  if(action==4){n=wire(b,type,other,4,1);/* rLA with zero values cannot refresh storage. */b[6]=0;n=7+b[2]+2+2;b[4]=b[2]+4;memset(b+7+b[2],0,4);CHECK(mrp_rx(a,0,b,n)==0);}
  if(action==5){CHECK(mrp_transmit(a,0,source_tx,sizeof(source_tx),send_accept,NULL)==1);}
  if(action==6){mrp_port_role_change(a,0,false);}
  if(action==7){CHECK(mrp_mad_join(a,0,type,changed,true)==0);allocation_fail_after(fault);mrp_port_role_change(a,0,true);CHECK(allocation_failures()==1);allocation_fail_after(0);}
  if(action==8){CHECK(mrp_mad_join(a,0,type,changed,false)==0);CHECK(mrp_mad_leave(a,0,type,changed)==0);}
  if(action==9){CHECK(mrp_reclaim(a,0)==0);}
  if(action<=9){CHECK(i->flush_pending);CHECK(!memcmp(i->flush_value,saved,size));CHECK(i->leave_timer.cs==1);CHECK(seen_leave==0);shlan_timer_tick();}
  if(action==10||action==11||action==12){n=wire(b,type,other,action==10?2:action==11?4:5,0);CHECK(mrp_rx(a,0,b,n)==0);}
  if(action==13){mrp_port_role_change(a,0,true);}
  CHECK(i->reg==MRP_REG_STATE_MT);CHECK(!i->flush_pending);CHECK(seen_leave==1);CHECK(seen_map==1);CHECK(!memcmp(indicated,saved,size));CHECK(!memcmp(policy_value,saved,size));
  unsigned leaves=0;
  for(struct mrp_map_work *w=priv_of(a)->ports[2].map_head;w;w=w->next)if(w->attr_type==type&&!w->join){leaves++;CHECK(!memcmp(w->value,saved,size));}
  CHECK(leaves==1);CHECK(mrp_transmit(a,2,target_tx,sizeof(target_tx),send_accept,NULL)==1);
  CHECK(!priv_of(a)->ports[2].map_head);
  /* All completion paths must leave ordinary unchanged registrations quiet. */
  n=wire(b,type,other,1,0);for(unsigned repeat=0;repeat<3;repeat++)CHECK(mrp_rx(a,0,b,n)==0);
  CHECK(seen_leave==1);CHECK(seen_join==1);
  printf("PASS type=%u initial=%s fault=%u action=%u snapshot_bytes=%zu\n",type,lv?"LV":"IN",fault,action,size);finish(a);
 }
}
static void replacements(void)
{
 for(unsigned type=1;type<=2;type++)for(unsigned fault=0;fault<=9;fault++){
  current++;struct mrp_app *a=setup(type);uint8_t b[80],tx[256];size_t n=wire(b,type,100,1,0);CHECK(mrp_rx(a,0,b,n)==0);
  struct mrp_attr_inst *i=instance(a,0,type);uint8_t saved[48];size_t size=attr_store_len(a->ops,type);memcpy(saved,i->attr_val,size);
  allocation_fail_after(1);mrp_port_role_change(a,0,true);CHECK(allocation_failures()==1);allocation_fail_after(0);
  n=wire(b,type,200,1,0);CHECK(mrp_rx(a,1,b,n)==0);CHECK(i->flush_pending);
  seen_leave=seen_join=seen_map=0;n=wire(b,3-type,300,1,0);allocation_fail_after(fault);int rc=mrp_rx(a,0,b,n);
  CHECK(allocation_failures()==(fault?1:0));CHECK(rc==(fault&&fault<=7?-SHLAN_ERROR_NO_MEMORY:0));
  allocation_fail_after(0);CHECK(mrp_rx(a,0,b,n)==0);CHECK(seen_leave==1);CHECK(!memcmp(indicated,saved,size));CHECK(!memcmp(policy_value,saved,size));CHECK(i->reg==MRP_REG_STATE_MT);CHECK(!i->flush_pending);
  for(unsigned p=1;p<3;p++)CHECK(mrp_transmit(a,p,tx,sizeof(tx),send_accept,NULL)>=0);
  printf("PASS pending replacement old=%u fault=%u\n",type,fault);finish(a);
 }
}
static void destroy_pending(void)
{
 for(unsigned type=1;type<=3;type++)for(unsigned fault=1;fault<=3;fault++){
  current++;struct mrp_app *a=setup(type);uint8_t b[80];size_t n=wire(b,type,type==3?2:100,1,0);CHECK(mrp_rx(a,0,b,n)==0);
  allocation_fail_after(fault);mrp_port_role_change(a,0,true);CHECK(allocation_failures()==1);CHECK(instance(a,0,type)->flush_pending);finish(a);
 }
}
int main(void){sweep();replacements();destroy_pending();printf("PASS storage lifecycle: %u cases, %u checks\n",cases,checks);return 0;}
