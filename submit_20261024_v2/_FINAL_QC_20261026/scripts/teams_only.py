import json,sys,re,glob,os
for d in sorted(glob.glob(sys.argv[1]+'/*/')):
    w=json.load(open(d+'environment/light-servers/world_data/LightMicrosoftTeams.json'))
    tid=[t['id'] for t in w.get('teams',[])]
    txt=' '.join(json.dumps(m) for m in w.get('messages',[]))
    toks=set(re.findall(r'\b[A-Z]{1,5}-\d{2,5}[A-Za-z0-9-]*\b|\b\d[\d,]*\.\d\d\b',txt))
    other=''
    for f in glob.glob(d+'environment/light-servers/world_data/*.json'):
        if 'MicrosoftTeams' not in f: other+=open(f,errors='ignore').read()
    for f in glob.glob(d+'environment/light-servers/task_data/**/*',recursive=True):
        if os.path.isfile(f):
            try: other+=open(f,errors='ignore').read()
            except: pass
    graded=open(d+'tests/reward/rubric/judge.toml').read()+open(d+'tests/test_outputs.py').read()
    only=sorted(t for t in toks if t not in other and t in graded)
    idknown=[t for t in tid if t in other]
    names=set(re.findall(r'"(?:from|sender|author)[^"]*":\s*"([^"]+)"',txt))
    print(os.path.basename(d[:-1])[:8],'| team id reachable elsewhere:',bool(idknown),'| Teams-only tokens that are graded:',only[:8])
