
#!/bin/bash

python bootstrap_trainingdata.py drug.label unlabeled_training_data 5
python bootstrap_trainingdata.py sex.label unlabeled_training_data 5
python bootstrap_trainingdata.py alcohol.label unlabeled_training_data 5
python bootstrap_trainingdata.py violence.label unlabeled_training_data 5