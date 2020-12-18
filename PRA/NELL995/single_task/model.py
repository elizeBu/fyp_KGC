from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_fscore_support
from sklearn.svm import SVC
from sklearn.metrics import precision_score,recall_score,accuracy_score
import pickle
import datetime
import numpy as np
from collections import defaultdict
from sklearn.metrics import average_precision_score

class Model:

    def __init__(self,feature_file="./result/agentbelongstoorganization/train_data_pcrw-exact_agentbelongstoorganization.txt"):

        relation = 'concept_agentbelongstoorganization'
        self.dataPath_ = './NELL-995/tasks/' + relation
        self.feature_file = feature_file
        self.features = []
        self.labels = []
        self.coef = []
        self.test_result = []
        self.test_features = []
        self.test_labels = []
        self.path_num = 0
        self.data_preprocess()
        self.path_file = "./result/agentbelongstoorganization/paths_threshold_agentbelongstoorganization.txt"
        self.data_file = self.dataPath_ + "/graph.txt"
        self.nodes = {}  # 记录节点的关系信息
        self.path_ids = [n for n in range(2254)]
        self.set_range()

    def set_range(self):  # 设置关系的值域和节点的关系信息
        with open(self.data_file, "r") as f:
            datas = f.readlines()
            for data in datas:
                node_1, relation, node_2 = data.strip().split("\t")
                if node_1 not in self.nodes.keys():
                    tem_node = Node(node_1)
                    self.nodes[node_1] = tem_node
                self.nodes[node_1].add(relation, node_2)

    def _prob(self, begin, end, relation_path):  # 采取后向截断的动态规划
        prob = 0
        length = len(relation_path)
        if length == 1:
            if end in self.nodes[begin].info[relation_path[0]]:
                prob = 1 / len(self.nodes[begin].info[relation_path[0]])
            else:
                prob = 0
            return prob
        else:
            if self.nodes[begin].info[relation_path[0]] == []:
                return 0
            else:
                for entity in self.nodes[begin].info[relation_path[0]]:
                    prob += (1 / len(self.nodes[begin].info[relation_path[0]])) * self._prob(entity, end,
                                                                                             relation_path[1:])
                return prob

    def data_preprocess(self):
        with open(self.feature_file,"r") as f:
            datas = f.readlines()
            for data in datas:
                data = eval(data.strip().split("\t")[1]) # 有些是int，有些是float
                # print(len(data))
                for n,d in enumerate(data):
                    data[n] = float(d)
                if len(data) == 2256:
                    self.labels.append(data[0])
                    self.features.append(data[1:])

    def train(self, stop_loss=0.01, max_iter=10000):

        self.model = LogisticRegression(
                            C=0.5,
                            random_state=0,
                            penalty="l1",
                            class_weight="balanced",
                            solver="saga",
                            tol=stop_loss,
                            max_iter=max_iter,
                            verbose=1
                            )


        X_train, X_test, y_train, y_test = train_test_split(self.features, self.labels, test_size=0.3, random_state=0)
        self.model.fit(X_train, y_train)
        # self.model1.fit(X_train,y_train)
        # self.model.predict_proba([X_test[0]])
        self.test_result = precision_recall_fscore_support(y_test, self.model.predict(X_test), average='micro')
        # self.test_result1 = precision_recall_fscore_support(y_test, self.model1.predict(X_test), average='micro')
        return

    def save(self, model_file, result_file="result.txt"):
        ids = []
        with open(model_file,"wb") as f:
            pickle.dump(self.model,f)

        with open(result_file,"w") as f:

            f.write(str(self.test_result)+"\n")

            f.write("\n\n\n")
            for n,c in enumerate(self.coef):
                f.write(str(self.path_ids[n])+"\t"+str(c)+"\n")
                ids.append(self.path_ids[n])
        return ids


class Node:

    def __init__(self, NodeName):
        self.name = NodeName
        self.info = defaultdict(list)  # 记录从实体NodeName出发，经关系relation,能到达的实体

    def add(self, relation, subnode):
        self.info[relation].append(subnode)


if __name__ == "__main__":
    starttime = datetime.datetime.now()
    relation = "agentbelongstoorganization"
    path = "./result/agentbelongstoorganization/"
    model = Model(feature_file=path + "train_data_pcrw-exact_agentbelongstoorganization.txt")
    model.train(stop_loss=0.0001, max_iter=10000)
    ids = model.save(path+"model_LR.pkl",path+"result_LR.txt")
    test_labels = []
    test_features =[]
    test_pairs = []

    with open(path+"test_data_pcrw-exact_agentbelongstoorganization.txt") as tf:
        datas = tf.readlines()
        for data in datas:
            data = eval(data.strip().split("\t")[1])  # 有些是int，有些是float
            # print(len(data))
            for n, d in enumerate(data):
                data[n] = float(d)
            if len(data) == 2256:
                test_labels.append(data[0])
                test_features.append(data[1:])
    # load model
    with open(path+"model_LR.pkl","rb") as fo:
        m = pickle.load(fo)

    y_score = []
    for p in m.predict_proba(test_features):
        y_score.append(p[0])
    print("Linear Regression prediction probability: ",y_score)


    y_true = test_labels
    AP = average_precision_score(y_true,y_score)

    print(relation + " Linear Regression Average precision: ",AP )

    result = precision_recall_fscore_support(test_labels, m.predict(test_features), average='micro')

    print("LR precision_recall_fscore_support: ", result)


    endtime = datetime.datetime.now()
    print("Time:",endtime-starttime)



