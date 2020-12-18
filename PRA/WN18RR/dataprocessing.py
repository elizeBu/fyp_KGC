with open("graph.txt",'w') as wf:
    with open('train2id.txt','r') as rf:
        datas = rf.readlines()
        for data in datas:
            e1,e2,r = data.strip().split()
            if (r != '0'):
                wf.write("%s %s %s\n"%(e1,e2,r))
                wf.write("%s %s %s\n"%(e2,e1,str(-int(r))))
            else:
                r = 11
                wf.write("%s %s %s\n" % (e1, e2, r))
                wf.write("%s %s %s\n" % (e2, e1, str(-int(r))))


with open('valid2id_new.txt','w') as wf:
    with open('valid2id.txt','r') as rf:
        datas = rf.readlines()
        for data in datas:
            e1,e2,r = data.strip().split()
            if (r != '0'):
                wf.write("%s %s %s\n"%(e1,e2,r))
            else:
                r = 11
                wf.write("%s %s %s\n" % (e1, e2, r))

from collections import  Counter
import random
relation1 = {}
with open('relation2id.txt','r') as rf:
    datas = rf.readlines()
    for d in datas:
        rel_id = d.strip().split('\t')[1]
        relation1[rel_id] = []


with open('train2id_new.txt','r') as f:
    datas = f.readlines()
    for n,data in enumerate(datas):
        e1,e2,r = data.strip().split()
        if r in relation1.keys():
            relation1[r].append(n)

sample_id = {}
sample_use = []
for k in relation1.keys():
    sample_rel_id = random.sample(relation1[k],80)
    sample_id[k] = sample_rel_id
    for s in sample_rel_id:
        sample_use.append(s)
print(sample_id)
print(sample_use)


with open('train2id_use.txt','w') as wf:
    with open('train2id_new.txt','r') as rf:
        datas = rf.readlines()
        for n,data in enumerate(datas):
            e1,e2,r = data.strip().split()
            if n in sample_use:
                print(n)
                wf.write('%s %s %s\n'%(e1,e2,r))


relation = []
with open('valid2id_new.txt','r') as f:
    datas = f.readlines()
    for data in datas:
        e1,e2,r = data.strip().split()
        relation.append(r)
print(Counter(relation))
