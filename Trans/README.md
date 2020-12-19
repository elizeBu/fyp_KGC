# Trans Series Model

Thanks [OpenKE](https://github.com/thunlp/OpenKE) provided by THUNLP for our reference.

The repository is modified from [OpenKE-master](https://github.com/thunlp/OpenKE/tree/master) and tested on Python 3.5+.

## Dataset

In this experiment, we used FB15k-237, WN18RR and NELL-995 as the experimental data set.
A dataset in the following format is required, which contains five files:
* train2id.txt: training file, the format is each line (**e1, e2, rel**), the first line is the number of triples.
* valid2id.txt: validation file, the format is the same as train2id.txt.
* test2id.txt: test file, the format is the same as train2id.txt.
* entity2id.txt: All entities and corresponding IDs, one per line.
* relation2id.txt: All relations and corresponding IDs, one per line.

All datasets can be downloaded from [OpenKE](https://github.com/thunlp/OpenKE/tree/OpenKE-PyTorch/benchmarks).

## Implementation details
The new ***base*** folder added details for the realization of relation prediction.
Replace the ***base*** folder in OpenKE with the ***base*** folder provided under this directory.



