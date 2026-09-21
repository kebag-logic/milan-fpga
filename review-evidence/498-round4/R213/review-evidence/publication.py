import ast,copy,json,re,sys
from runner import load,ROOT,TMP
m=load(); path=m.MILAN_SOC_PY; source=path.read_text(); rows=[]
loops=[n for n in ast.walk(ast.parse(source)) if isinstance(n,ast.For) and isinstance(n.iter,ast.Call) and isinstance(n.iter.func,ast.Attribute) and isinstance(n.iter.func.value,ast.Call) and isinstance(n.iter.func.value.func,ast.Name) and n.iter.func.value.func.id in ('fabric_constants','firmware_constants')]
assert len(loops)==2
lines=source.splitlines(keepends=True)
def replace_loop(node,new):
    indent=' '*node.col_offset
    text='\n'.join(indent+s if s else '' for s in new.splitlines())+'\n'
    return ''.join(lines[:node.lineno-1])+text+''.join(lines[node.end_lineno:])
def check(label,text,want):
    ast.parse(text)
    try:m._assert_publication_loop_is_pinned(text); got='ACCEPT'; msg=''
    except AssertionError as e:got='REFUSE'; msg=str(e)
    rows.append(dict(label=label,result=got,message=msg)); print(label,got,flush=True)
    assert got==want,(label,msg)
check('pristine',source,'ACCEPT')
for n in loops:
    name=n.iter.func.value.func.id; canonical=ast.unparse(n)
    value='3 if _name.endswith("CTRL_BOOT") else _value' if name=='fabric_constants' else '300 if _name.endswith("HEARTBEAT_MS") else _value'
    variants={
      'later_override':canonical+'\n    soc.add_constant(_name, '+value+', check_duplicate=False)',
      'conditional_later_override':canonical+'\n    if _name.endswith("CTRL_BOOT"):\n        soc.add_constant(_name, 3, check_duplicate=False)',
      'else_override':canonical+'\nelse:\n    soc.add_constant(_name, 17, check_duplicate=False)',
      'duplicate_loop':canonical+'\n'+canonical,
      'early_continue':canonical.replace('    soc.add_constant','    continue\n    soc.add_constant'),
      'changed_target':canonical.replace('_name, _value','_key, _value',1),
      'substituted_value':canonical.replace('soc.add_constant(_name, _value)','soc.add_constant(_name, '+value+')'),
    }
    for label,text in variants.items(): check(name+' '+label,replace_loop(n,text),'REFUSE')
    formatted=canonical.replace('    soc.add_constant(_name, _value)','    # public constant\n    soc.add_constant(\n        _name,\n        _value,\n    )')
    check(name+' comments and multiline arguments',replace_loop(n,formatted),'ACCEPT')
    # Execute the complete gate with the exact original later-write shape on disk.
    planted=replace_loop(n,variants['later_override']); before=path.read_bytes()
    try:
        path.write_text(planted)
        try:m.test_boot_policy_follows_the_declaration()
        except AssertionError as e:
            assert 'not the pinned complete loop' in str(e),str(e)
            print(name,'complete gate35 REFUSE later_override',flush=True)
        else:raise AssertionError('gate35 accepted later override')
    finally:path.write_bytes(before)
    assert path.read_bytes()==before
for key in m.nvm_shape.WRITER_TIMING_MS:
    values=dict(m.nvm_shape.WRITER_TIMING_MS); values[key]+=1
    try:m._assert_writer_waits_generated(m.FIRMWARE_C.read_text(),values)
    except AssertionError as e:assert 'the pinned set is' in str(e)
    else:raise AssertionError(key+' moved without refusal')
    print('wait',key,'+1 REFUSE',flush=True)
(TMP/'publication.json').write_text(json.dumps(rows,indent=2))
