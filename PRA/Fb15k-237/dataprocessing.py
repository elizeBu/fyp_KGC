with open('train2id_new.txt','w') as wf:
    with open('train2id.txt','r') as rf:
        datas = rf.readlines()
        for data in datas:
            e1,e2,r = data.strip().split()
            if r == '0':
                r = 237
                wf.write("%s %s %s\n"%(e1,e2,r))
            else:
                wf.write("%s %s %s\n" % (e1, e2, r))

with open('graph.txt','w') as wf:
    with open('train2id_new.txt','r') as rf:
        datas = rf.readlines()
        for data in datas:
            e1,e2,r = data.strip().split()
            wf.write("%s %s %s\n"%(e1,e2,r))
            wf.write("%s %s %s\n" % (e2, e1, str(-int(r))))

with open('test2id_new.txt','w') as wf:
    with open('test2id.txt','r') as rf:
        datas = rf.readlines()
        for data in datas:
            e1,e2,r = data.strip().split()
            if r == '0':
                r = 237
                wf.write("%s %s %s\n"%(e1,e2,r))
            else:
                wf.write("%s %s %s\n" % (e1, e2, r))