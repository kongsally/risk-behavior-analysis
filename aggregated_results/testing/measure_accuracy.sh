#!/bin/bash

python measure_accuracy.py labeled_sex.tsv predict_sex.tsv sex
python measure_accuracy.py labeled_alcohol.tsv predict_sex.tsv alcohol
python measure_accuracy.py labeled_drug.tsv predict_sex.tsv drug
python measure_accuracy.py labeled_violence.tsv predict_sex.tsv violence