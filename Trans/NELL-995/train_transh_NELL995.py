import config
import models
import tensorflow as tf
import numpy as np
import os
from sys import argv
import time

os.environ['CUDA_VISIBLE_DEVICES']='0'
#Input training files from benchmarks/FB15K/ folder.
con = config.Config()
#True: Input test files from the same folder.
#con.set_in_path("./benchmarks/WN18RR/")
start1 = time.time()
con.set_in_path("/Users/qiyuchen/Desktop/OpenKE-master/benchmarks/NELL-995/")
#con.set_test_link_prediction(True)
con.set_test_relation_prediction(True)
# con.set_test_triple_classification(True)
con.set_work_threads(8)
con.set_train_times(40)
con.set_nbatches(100)
con.set_alpha(1.0)
con.set_margin(6.0)
con.set_bern(1)
con.set_dimension(50)
con.set_ent_neg_rate(1)
con.set_rel_neg_rate(0)
con.set_opt_method("SGD")

#Models will be exported via tf.Saver() automatically.
con.set_export_files("./res/model.vec.tf", 0)
#Model parameters will be exported to json files automatically.
con.set_out_files("./res/embedding.vec.json")
# con.set_import_files("./res/model.vec.tf")
#Initialize experimental settings.
con.init()
#Set the knowledge embedding model
con.set_model(models.TransH)
#Train the model.
con.run()
end1 = time.time()
#To test models after training needs "set_test_flag(True)".
start2 = time.time()
con.test()
end2 = time.time()
print('The training time：', end1-start1)
print('The testing time: ', end2-start2)
