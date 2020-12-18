from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_fscore_support
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score,recall_score
import pickle
from sklearn.metrics import classification_report
from collections import Counter
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.metrics import average_precision_score
import datetime

class Model:

    def __init__(self,feature_file="train_data_pcrw-exact.txt"):

        self.feature_file = feature_file
        self.features = []
        self.labels = []
        self.coef = []
        self.test_result=[]
        self.path_num = 0
        self.data_preprocess()
        self.path_ids = [n for n in range(3848)]



    def data_preprocess(self):

        with open(self.feature_file,"r") as f:
            datas = f.readlines()
            for data in datas:
                data = eval(data.strip().split("\t")[1]) # 有些是int，有些是float
                for n,d in enumerate(data):
                    data[n] = float(d)
                if len(data) == 3848:
                    self.labels.append(data[0])
                    self.features.append(data[1:])
    def train(self,
              stop_loss=0.01,
                max_iter=10000):

        self.model = LogisticRegression(penalty="l1",
                                        C=0.5,
                                        class_weight="balanced",
                                        random_state=0,
                                        solver="saga",
                                        multi_class="multinomial",
                                        tol=stop_loss,
                                        max_iter=max_iter,
                                        verbose=1
                                        )

        X_train, X_test, y_train, y_test = train_test_split(self.features, self.labels, test_size=0.3, random_state=0)
        self.model.fit(X_train, y_train)
        self.test_result = precision_recall_fscore_support(y_test, self.model.predict(X_test), average="micro")
        print(self.model.classes_)
        relation_change_dict = {}
        for id, target in enumerate(self.model.classes_):
            relation_change_dict[id] = target

        total_rank_list = []
        for i in range(len(X_test)):
            temp_rank_list = []
            rank_list = []
            for id, pr in enumerate(self.model.predict_proba([X_test[i]])[0]):
                temp_rank_list.append([relation_change_dict[id], pr])
                temp_rank_list = sorted(temp_rank_list, key=lambda s: s[1], reverse=True)
            for r in temp_rank_list:
                rank_list.append(r[0])
            total_rank_list.append(rank_list)

        y_pred = []
        for t in total_rank_list:
            y_pred.append(t[0])
        print(y_pred)
        print(self.model.predict(X_test))

        ranks = []
        hits3 = []
        for i in range(len(total_rank_list)):
            r = total_rank_list[i]
            if y_test[i] in r:
                for n, rid in enumerate(r):
                    if float(y_test[i]) == float(rid):
                        rank = n + 1
                        ranks.append(rank)
                        if rank <= 3:
                            hits3.append(1.0)
                        else:
                            hits3.append(0.0)
        print("Mean Rank", np.mean(ranks))
        print("Hits3", np.mean(hits3))
        print("Precision", precision_score(y_test, self.model.predict(X_test), average='micro'))
        return

    def save(self, model_file, result_file="result.txt"):
        with open(model_file,"wb") as f:
            pickle.dump(self.model,f)

        with open(result_file,"w") as f:
            for result in self.test_result:
                f.write(str(result)+"\n")
            f.write("\n\n\n")
            for n,c in enumerate(self.coef):
                f.write(str(self.path_ids[n])+"\t"+str(c)+"\n")
        return self.model

    def path_selection(self,threshold=0.001):

        tem = []
        for n, c in enumerate(self.coef):
            if abs(c) > threshold:
                tem.append(self.path_ids[n])
            else:
                continue
        self.path_ids = tem
        del tem
        return

    def retrain(self,stop_loss=0.0001, max_iter=100000):
        for m,feature in enumerate(self.features):
            tem = []
            for n,v in enumerate(feature):
                if n in self.path_ids:
                    tem.append(v)
            self.features[m] = tem
            del tem
        self.train(stop_loss=stop_loss, max_iter=max_iter)

if __name__ == "__main__":
    starttime = datetime.datetime.now()
    model = Model(feature_file="train_data_pcrw-exact.txt")
    model.train(stop_loss=0.01, max_iter=10000)
    m = model.save("model_LR.pkl","result_LR.txt")
    #load model
    # with open("model_LR.pkl","rb") as fo:
    #     m = pickle.load(fo)

    endtime = datetime.datetime.now()
    print("Time:", endtime - starttime)



