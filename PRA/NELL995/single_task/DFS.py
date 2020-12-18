# -*- coding: utf-8 -*-

from collections import defaultdict
from collections import Counter
import sys
import datetime
sys.setrecursionlimit(20000)

class graph:

    def __init__(self):

        self.nodes =  {} # 节点名字到(r,子节点)组构成的词典
        self.paths = [] # 记录所有搜索到的路径
        self.begin = ""
        self.path = defaultdict(list) # 记录单条路径
        # self.times = 0  # 已经搜索到多少路径了？
        self.max_length = 5
        self.end = ""
        self.steps = 0
        self.relation_paths = [] # 记录所有关系路径，不包含实体

    def add(self, node, relation, next_node):
        if node in self.nodes:
            if next_node not in self.nodes:  # 需要先建立Node结构
                self.nodes[next_node] = Node(next_node)
            self.nodes[node].conjunctions.append((relation, self.nodes[next_node]))
        else:
            self.nodes[node] = Node(node) # 创建头节点，然后依然调用此函数
            self.add(node, relation,next_node)


    def set_init(self, begin, end, max_length): # 路径搜索时，初始化一些参数

        self.begin = begin
        self.end = end
        self.max_length = max_length
        self.path = [("root",self.begin)]
        self.paths = []
        self.relation_paths = []
    # self.max_times = max_search_times


    def dfs(self, begin): # 深度优先搜索

        if begin == self.end:
            tem = []
            for n in self.path:
                tem.append(n)

            self.paths.append(tem)
            # print("paths",self.paths)
            return
        try: # 偶尔出现没有在数据库中出现的实体，所以加一个try catch
            if self.nodes[begin].conjunctions is None:
                return
            if len(self.path) == self.max_length+1: # 设置一下最大路径长度
                return
            for (_relation, subnode) in self.nodes[begin].conjunctions:

                if (_relation, subnode.NodeName) not in self.path:
                    # print((_relation, subnode.NodeName))
                    self.path.append((_relation, subnode.NodeName))
                    self.dfs(subnode.NodeName)
                    self.path.remove((_relation, subnode.NodeName))
                # print(self.path)
        except:
            print("存在没有注册的实体%s\n"%begin)
        return

    def extract_route(self): # 将路径中的关系单拿出来
        for path in self.paths:
            tem = ""
            for e in path:
                tem = tem + e[0] +"\t"
            self.relation_paths.append(tem)
        return

"""
对于知识图谱来说，这里的每个节点不仅包含节点的名称，而且包含从它出去的每个关系以及关系的另一端的另一个节点
"""
class Node:

    def __init__(self,NodeName):
        self.NodeName = NodeName
        self.conjunctions = []

if __name__ == "__main__":
    starttime = datetime.datetime.now()
    relation = 'concept_teamplayssport'
    dataPath_ = './NELL-995/tasks/' + relation
    save_path = "./result/teamplayssport/path_dfs_teamplayssport.txt"
    alpha = 0.01
    paths = []
    kg = graph()
    data_path = dataPath_ + "/graph.txt"
    train_path = dataPath_ + "/train.pairs"
    test_path = dataPath_ + "/test.pairs"
    max_length = 4

    with open(data_path,"r") as f:
        datas = f.readlines()
        for data in datas:
            [node, relation, next_node] = data.strip().split("\t")
            # print(node)
            kg.add(node, relation, next_node)

    print("*************train_path*************")
    with open(train_path,"r") as f:
        datas = f.readlines()
        for n, data in enumerate(datas):
            [node_1, node_2] = data.strip()[0:-3].split(",")
            [node_1, node_2] = data.strip()[0:-3].split(",")
            node_1 = node_1.replace("thing$", "")
            node_2 = node_2.replace("thing$", "")
            flag = data.strip()[-1]
            if flag == "+":
                begin = node_1
                end = node_2
                kg.set_init(begin, end, max_length)
                print("开始第%d个样本对：\n"%n)
                kg.dfs(begin)
                kg.extract_route()
                paths.extend(kg.relation_paths)
            else:
                continue

    print("*************test_path*************")
    with open(test_path,"r") as f:
        datas = f.readlines()
        for n, data in enumerate(datas):
            [node_1, node_2] = data.strip()[0:-3].split(",")
            node_1 = node_1.replace("thing$", "")
            node_2 = node_2.replace("thing$", "")
            flag = data.strip()[-1]
            if flag == "+":
                begin = node_1
                end = node_2
                kg.set_init(begin, end, max_length)
                print("开始第%d个样本对：\n"%n)
                kg.dfs(begin)
                kg.extract_route()
                paths.extend(kg.relation_paths)
            else:
                continue
    path_count = Counter(paths)
    with open(save_path,"w") as f:
        for path in path_count.keys():
            f.write(path + "%d"%path_count[path] + "\n")

    with open(save_path, "r") as f:
        dict = {}
        datas = f.readlines()
        for data in datas:
            path = data.strip().split("\t")[1:-2]
            num = int(data.strip().split("\t")[-1])
            path_str = ""
            for relation in path:
                path_str += (relation+"\t")
            dict[path_str] = num
        threshold = int(700 * alpha)
        dict_2 = {}
        for key in dict.keys():
            if dict[key]>=threshold:
                dict_2[key] = dict[key]
    with open("./result/teamplayssport/paths_threshold_teamplayssport.txt","w") as f:
        for n,key in enumerate(dict_2.keys()):
            f.write("%d\t"%n+key+"\n")
    endtime = datetime.datetime.now()
    print("Time:",endtime-starttime)














