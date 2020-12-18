from collections import defaultdict
import numpy as np
import datetime

class Feature():

    def __init__(self):
        self.data_file = "graph.txt"
        self.path_file = "paths_threshold.txt"
        self.train_file = "valid2id_new.txt"
        self.nodes = {} # 记录节点的关系信息
        self.train_data = defaultdict(list)
        self.set_range()

    def set_range(self): # 设置关系的值域和节点的关系信息
        with open(self.data_file,"r") as f:
            datas = f.readlines()
            for data in datas:
                node_1, node_2,relation = data.strip().split()
                if node_1 not in self.nodes.keys():
                    tem_node = Node(node_1)
                    self.nodes[node_1] = tem_node
                self.nodes[node_1].add(relation, node_2)

    def _prob(self, begin, end, relation_path): # 采取后向截断的动态规划
        prob = 0
        length = len(relation_path)
        # print(relation_path,length)
        if length == 1:
            if end in self.nodes[begin].info[relation_path[0]]:
                prob = 1/len(self.nodes[begin].info[relation_path[0]])
            else:
                prob = 0
            return prob
        else:
            if self.nodes[begin].info[relation_path[0]] == []:
                return 0
            else:
                for entity in self.nodes[begin].info[relation_path[0]]:
                    if(entity not in self.nodes.keys()):
                        prob = 0
                    else:
                        prob += (1/len(self.nodes[begin].info[relation_path[0]])) * self._prob(entity, end, relation_path[1:])
                return prob

    def _walkers_prob(self,walker_num,begin,end,relation_path): # Finger Print 方法是基于蒙特卡洛方法来估计路径概率
        walkers = []
        for n in range(walker_num):
            walkers.append(Walker("%d"%n,begin))
        for relation in relation_path:
            for walker in walkers:
                if walker.state=="walking":
                    start = walker.walk_history[-1]
                    subnodes = self.nodes[start].info[relation]
                    walker.onestep_walk(subnodes)
                else:
                    continue
        count = 0
        for walker in walkers:
            if walker.walk_history[-1]==end and walker.state=="walking":
                count += 1
        return count/walker_num

    def _particle_filtering_prob(self,walker_num,begin,end,relation_path,threshold_num=5):

        walkers = []
        for n in range(walker_num):
            walkers.append(Walker("%d"%n,begin))

        old_node_workers = {begin:walkers}

        for relation in relation_path:
            current_node_workers = defaultdict(list)
            for node in old_node_workers.keys():
                subnodes = self.nodes[node].info[relation]
                if subnodes == []:
                    continue
                else:
                    mean = len(old_node_workers[node])/len(subnodes)
                    if mean >= threshold_num: # 说明够分
                        num_distribute = int(mean)
                        k = 0
                        for subnode in subnodes:
                            if len(old_node_workers[node])-k >= mean:
                                for l in range(num_distribute):
                                    current_node_workers[subnode].append(old_node_workers[node][k+l])
                                k += num_distribute
                            else:
                                for l in range(k,len(old_node_workers[node])):
                                    current_node_workers[subnode].append(old_node_workers[node][k+l])
                    else: # 不够分，就按最小的分，但是是随机分
                        k = 0
                        for l in range(int(len(old_node_workers[node])/threshold_num)):
                            ran = np.random.randint(len(subnodes),size=1)[0]
                            if len(old_node_workers[node])-k >= threshold_num:
                                for n in range(threshold_num):
                                    current_node_workers[subnodes[ran]].append(old_node_workers[node][k+l])
                                k += threshold_num
                            else:
                                for l in range(k,len(old_node_workers[node])):
                                    current_node_workers[subnodes[ran]].append(old_node_workers[node][k + l])
            old_node_workers = current_node_workers

        if end in old_node_workers.keys():
            return len(old_node_workers[end])/walker_num
        else:
            return 0

    def _low_sample_varaince(self):
        print("to be continued")


    def get_probs(self,prob_flag="pcrw-exact",walker_num=50): # 完全按照随机游走的公式来计算路径概率

        relation_paths = []
        with open(self.path_file,"r") as f:
            paths = f.readlines()
            for path in paths:
                if(path.strip().split("\t")[1:]):
                    relation_paths.append(path.strip().split("\t")[1:])
        # print(relation_paths)

        with open(self.train_file,"r") as f:
            datas = f.readlines()
            for s,data in enumerate(datas):
                # print("开始！")
                node_1 = data.strip().split()[0]
                node_2 = data.strip().split()[1]
                if node_1 not in self.nodes.keys():
                    print("发现未注册实体:%s"%node_1)
                    continue
                else:
                    flag = data.strip().split()[-1]
                    if flag:
                        self.train_data[(node_1,node_2)].append(int(flag))

                    for path in relation_paths:
                        if prob_flag == "pcrw-exact":
                            tem = self._prob(node_1,node_2,path)

                        elif prob_flag == "finger-print":
                            tem = self._walkers_prob(walker_num=walker_num,
                                                     begin=node_1,
                                                     end=node_2,
                                                     relation_path=path)
                        elif prob_flag == "particle-filter":
                            tem = self._particle_filtering_prob(walker_num=walker_num,
                                                                begin=node_1,
                                                                end=node_2,
                                                                relation_path=path,
                                                                threshold_num=5)
                        else:
                            print("Boss, Flag is not write!")
                            return
                        self.train_data[(node_1, node_2)].append(tem)
                print("第%d个结束！\n"%s)

        with open("train_data_%s.txt"%prob_flag,"w") as f:
            for key in self.train_data:
                f.write(str(key)+"\t"+str(self.train_data[key])+"\n")
        return




class Node:

    def __init__(self,NodeName):
        self.name = NodeName
        self.info = defaultdict(list) # 记录从实体NodeName出发，经关系relation,能到达的实体
    def add(self,relation, subnode):
        self.info[relation].append(subnode)

class Walker:
    def __init__(self,name,begin):
        self.name = name
        self.walk_history = [begin]
        self.state = "walking"

    def onestep_walk(self,subnodes):
        if subnodes==[]:
            self.state = "stop"
            # print("walker %s stopped!"%self.name)
            return
        else:
            n = len(subnodes)
            m = np.random.randint(n,size=1)[0]
            self.walk_history.append(subnodes[m])
        return

if __name__ == "__main__":
    starttime = datetime.datetime.now()
    feature = Feature()
    feature.get_probs()
    endtime = datetime.datetime.now()
    print("Time:", endtime - starttime)
