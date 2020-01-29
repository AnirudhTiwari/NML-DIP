'''
This is a script to parse the any dataset features and write into a .csv file for analysis.
This file write the output to out.csv. Import that out.csv to a relevant excel sheet and proceed.
I have added out.csv and *.xslx to the .gitignore to avoid polutting the code.
'''
import json
import csv
import itertools
import sys

SINGLE_VS_MULTI_DOMAIN_IDENTIFICATION_TRAINING_DATASET_FEATURES_FILE = "../TrainingData/singleVsMultiTrainingDatasetFeatures.json"

fields = ["pdb", "Domains", "Length", "Interaction_Energy", "Density", "Radius_Of_Gyration"]


with open(SINGLE_VS_MULTI_DOMAIN_IDENTIFICATION_TRAINING_DATASET_FEATURES_FILE, 'r') as f:
	svm_single_vs_multi_train_data = json.load(f)
f.close()

with open('out.csv', 'w', newline='') as csvfile:
	w = csv.DictWriter(csvfile, fields)
	w.writeheader()
	for key,val in sorted(svm_single_vs_multi_train_data.items()):
	    row = {"pdb": key}
	    row.update(val)
	    w.writerow(row)