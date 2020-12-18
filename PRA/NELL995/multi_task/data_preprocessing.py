entity_dict = {}
with open("entity2id.txt",'r') as entity_file:
    datas = entity_file.readlines()
    for data in datas[1:]:
        entity_name = data.strip().split('\t')[0]
        entity_id = data.strip().split('\t')[1]
        entity_dict[entity_name]=entity_id

relation_dict = {}
with open("relation2id.txt",'r') as relation_file:
    datas = relation_file.readlines()
    for data in datas[1:]:
        relation_name = data.strip().split('\t')[0]
        # relation_name = relation_name.replace("concept:","")
        relation_id = data.strip().split('\t')[1]
        relation_dict[relation_name]=relation_id
        relation_dict[relation_name+'_inv'] = str(-int(relation_id))

# with open("graph_with_inv.txt",'w') as wf:
#     with open("graph.txt", 'r') as f:
#         datas = f.readlines()
#         for data in datas:
#             e1 = data.strip().split()[0]
#             e2 = data.strip().split()[1]
#             r = data.strip().split()[2]
#             wf.write("%s %s %s\n" % (e1,e2,r))
#             wf.write("%s %s %s\n" % (e2, e1, str(-int(r))))

with open("train2id.txt",'w') as wf:
    with open("train_all.pairs",'r') as f:
        datas = f.readlines()
        for data in datas:
            e1 = data.strip().split(',')[0]
            e2 = data.strip().split(',')[1].split(':')[0]
            r = data.strip().split(',')[1].split(':')[1]
            if e1 in entity_dict.keys():
                e1 = entity_dict[e1]
            if e2 in entity_dict.keys():
                e2 = entity_dict[e2]
            if r in relation_dict.keys():
                r = relation_dict[r]
            wf.write("%s %s %s\n" % (e1,e2,r))


# check #
triples = []
with open('graph.txt','r') as f:
    datas = f.readlines()
    for data in datas:
        e1,e2,r = data.strip().split()
        triples.append([e1,e2,r])

with open('graph_test.txt','w') as wf:
    with open('graph_nell995.txt','r') as f:
        datas = f.readlines()
        for data in datas:
            e1,r,e2 = data.strip().split('\t')
            if e1 in entity_dict.keys():
                e1 = entity_dict[e1]
            if e2 in entity_dict.keys():
                e2 = entity_dict[e2]
            if r in relation_dict.keys():
                r = relation_dict[r]
