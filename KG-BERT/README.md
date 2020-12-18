# KGC, Language-based Model, Knowledge Graph BERT (KG-BERT)

Thanks [KG-BERT](https://github.com/yao8839836/kg-bert) provided by Liang, Yao for our reference.

The repository is modified from [pytorch-pretrained-BERT](https://github.com/huggingface/pytorch-pretrained-BERT) and tested on Python 3.5+.


## Installing requirement packages

```bash
pip install -r requirements.txt
```

## Data

(1) The benchmark knowledge graph datasets are in ./KG-BERT/data (./FB15k-237 or ./WN18RR or ./NELL-995).

(2) NELL995_data_processing folder contains process of NELL-995 dataset preprocessing, the output can be found in ./KG-BERT/data/NELL-995 respectively.

## Experimental results

### Relation Prediction

#### FB15k-237

```shell
python3 run_bert_relation_prediction.py 
--task_name kg  
--do_train  
--do_eval 
--do_predict 
--data_dir ./data/FB15k-237
--bert_model bert-base-cased
--max_seq_length 25
--train_batch_size 32 
--learning_rate 5e-5 
--num_train_epochs 5.0 
--output_dir ./output_FB15k-237/  
--gradient_accumulation_steps 1 
--eval_batch_size 512
```

#### WN18RR

```shell
python3 run_bert_relation_prediction.py 
--task_name kg  
--do_train  
--do_eval 
--do_predict 
--data_dir ./data/WN18RR
--bert_model bert-base-cased
--max_seq_length 25
--train_batch_size 32 
--learning_rate 5e-5 
--num_train_epochs 5.0 
--output_dir ./output_WN18RR/  
--gradient_accumulation_steps 1 
--eval_batch_size 512
```

#### NELL-995

```shell
python3 run_bert_relation_prediction.py 
--task_name kg  
--do_train  
--do_eval 
--do_predict 
--data_dir ./data/NELL-995
--bert_model bert-base-cased
--max_seq_length 25
--train_batch_size 32 
--learning_rate 5e-5 
--num_train_epochs 5.0 
--output_dir ./output_NELL-995/  
--gradient_accumulation_steps 1 
--eval_batch_size 512
```
