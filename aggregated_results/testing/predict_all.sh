
#!/bin/bash

python predict_unlabelled.py alcohol.label unlabelled_testing_data.tsv predict_alcohol.tsv
python predict_unlabelled.py sex.label unlabelled_testing_data.tsv predict_sex.tsv
python predict_unlabelled.py drug.label unlabelled_testing_data.tsv predict_drug.tsv
python predict_unlabelled.py violence.label unlabelled_testing_data.tsv predict_violence.tsv