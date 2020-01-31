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
BENCHMARK_2_PRECALCULATED_FEATURES_FILE = "../PrecalculatedFeaturesForTestDatasets/benchmark_2_features.json"
BENCHMARK_3_PRECALCULATED_FEATURES_FILE = "../PrecalculatedFeaturesForTestDatasets/benchmark_3_features.json"
ASTRAL_SCOP30_PRECALCULATED_FEATURES_FILE = "../PrecalculatedFeaturesForTestDatasets/astral_scop_30_features.json"
NR_DATASET_PRECALCULATED_FEATURES_FILE = "../PrecalculatedFeaturesForTestDatasets/nr_dataset_features.json"
fields = ["pdb", "Domains", "Length", "Interaction_Energy", "Density", "IS-Sum_2", "IS-Sum_3", "IS-Sum_4"]


with open(NR_DATASET_PRECALCULATED_FEATURES_FILE, 'r') as f:
	svm_single_vs_multi_train_data = json.load(f)
f.close()

with open('out.csv', 'w', newline='') as csvfile:
	w = csv.DictWriter(csvfile, fields)
	w.writeheader()
	for key,val in sorted(svm_single_vs_multi_train_data.items()):
	    row = {"pdb": key}
	    row.update(val)
	    w.writerow(row)
