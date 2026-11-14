"""Event handler lower bounds from completed trace spans. Args: checkout result-directory."""
from pathlib import Path
import sys
root,results=map(Path,sys.argv[1:3])
sys.path.insert(0,str(root/"tb/verilator/ctrl_service_budget"))
import grade,load_grade
sinks={"adp_mbx:on_event","acmp_mbx:on_event","maap_mbx:event","aecp_mbx:event","srp_mbx:on_event"}
costs=load_grade.stated(root,"8x8/1if",load_grade.STATED_US)
worst={}
for path in sorted(results.glob("*.log")):
 log=grade.parse(path.read_text(),100_000_000,100_000_000)
 groups=[];current=[];start=None
 for t in log.traced:
  if t[0]=="CALL" and t[-1]=="mbx_event_take":
   if current:
    assert len(current)==5 and {x[-1] for x in current}==sinks
    groups.append((start,current))
   current=[];start=int(t[1])
  elif t[0]=="SPAN" and t[-1] in sinks:
   current.append(t)
 if current:groups.append((start,current))
 assert len(groups)<=len(log.records)
 print(path.name,"consumed event groups",len(groups),"posted",len(log.records))
 for (start,ss),(posted,words) in zip(groups,log.records):
  assert posted<=int(ss[0][1])
  event=grade.EVENT[words[0]&255]
  if event=="TIMER":event={0:"ADP",1:"ACMP",2:"MAAP",3:"AECP"}.get((words[1]>>16)&255,"unknown")
  n=sum(int(t[3]) for t in ss)
  if n>worst.get(event,(0,))[0]:worst[event]=(n,path.name,start)
for event,(cycles,file,start) in sorted(worst.items()):
 key="event."+event;needed=((cycles*21+9999)//10000)*5
 print(key,"handler sum cycles",cycles,"minimum required us",needed,"stated us",costs.get(key,"outside load table"),"at",file,start)
print("Handler sums exclude dispatcher overhead; a below-table sum alone does not certify the full event cost.")
