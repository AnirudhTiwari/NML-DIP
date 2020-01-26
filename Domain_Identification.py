from __future__ import print_function
from builtins import input
import SVM_v2
import common_functions as utils
import calculateFeatures
import csv
import json
import K_Means
import time
import shutil

OUTPUT_FOLDER = "OutputFiles"

def get_input_dataset_name(x):
	return {
		'A' : "Benchmark_2",
		'B' : "Benchmark_3",
		'C' : "ASTRAL SCOP30",
		'D' : "NR_Dataset"
	}[x]

def get_input_feature_name(x):
	return {
		'L' : "Length",
		'I' : "Interaction_Energy",
		'R' : "Radius_Of_Gyration",
		'D' : "Density",
		'S' : "Density_Sum",
		'IS': "IS_Sum"
	}[x]

def get_test_dataset(x):
	return {
		"Benchmark_2" : "TestDatasets/benchmark_2_chains.txt",
		"Benchmark_3" : "TestDatasets/benchmark_3_chains.txt",
		"ASTRAL SCOP30" : "TestDatasets/astral_scop_30_chains.txt",
		"NR_Dataset" : "TestDatasets/nr_dataset_chains.txt"
	}[x]
def get_test_dataset_features(x):
	return {
	"Benchmark_2" : "PrecalculatedFeaturesForTestDatasets/benchmark_2_features.json",
	"Benchmark_3" : "PrecalculatedFeaturesForTestDatasets/benchmark_3_features.json",
	"ASTRAL SCOP30" : "PrecalculatedFeaturesForTestDatasets/astral_scop_30_features.json",
	"NR_Dataset" : "PrecalculatedFeaturesForTestDatasets/nr_dataset_features.json"
	}[x]

#Taking user input for test dataset
while 1:
	testing_dataset_input = input("Input Testing Dataset: Type A for Benchmark_2, B for Benchmark_3, C for ASTRAL SCOP 30, D for NR_Dataset\n")
	try:
		testing_dataset = get_input_dataset_name(testing_dataset_input)
		print("You selected " + testing_dataset + " for testing the algorithm\n")
		break
	except KeyError:
		print("Invalid input!!")

print()
print("#############################--------STEP 1--------#####################################")
print()
print("CLASSIFYING SINGLE-DOMAIN vs MULTI-DOMAIN PROTEINS\n")

feature_set = ["Length", "Interaction_Energy", "Density"]

file_training_dataset_features = "TrainingData/singleVsMultiTrainingDatasetFeatures.json"
print("Feature set is: ", feature_set)
print() 
with open(file_training_dataset_features) as f:
	SVM_train_data = json.load(f)
f.close()


classifier = "single_vs_multiDomain"
file_testing_dataset_features = get_test_dataset(testing_dataset)

with open(file_testing_dataset_features) as f:
	SVM_test_data = f.readlines()
f.close()

test_dataset_feature_file = get_test_dataset_features(testing_dataset)

with open(test_dataset_feature_file) as f:
	SVM_test_data_features = json.load(f)
f.close()

correct_chains_with_features, incorrect_chains_with_features = SVM_v2.classify(SVM_train_data, SVM_test_data, SVM_test_data_features, feature_set, classifier)

print("----------------------------------------------------------------------------------------")
print("Performance of single vs multi-domain identification")
print() 
utils.SVM_Performance_Analyser(correct_chains_with_features, SVM_test_data, classifier)

multi_correct_chains = []
single_correct_chains = []


with open("HelperData/pdb_to_domains_map.json") as f:
	pdb_to_domain_map = json.load(f)
f.close()

for chain in correct_chains_with_features:
	domains = pdb_to_domain_map[chain]
	if int(domains) > 1:
		multi_correct_chains.append(chain)
	else:
		single_correct_chains.append(chain)


print("----------------------------------------------------------------------------------------")
print()
print("#############################--------STEP 2--------#####################################")
print()
print("CLASSIFYING MULTI-DOMAIN PROTEINS\n")
print()

feature_set = ["Length", "IS-Sum_2", "IS-Sum_3", "IS-Sum_4"]

with open('TrainingData/multiDomainTrainingDatasetFeatures.json', 'r') as f:
    SVM_multi_train_data = json.load(f)

classifier = "multi-domain"

print("Feature set is ", feature_set)
print()
step2_correct_chains, step2_incorrect_chains = SVM_v2.classifyMultiDomainProteins_v2(SVM_multi_train_data, multi_correct_chains, SVM_test_data_features, feature_set, classifier)

print("----------------------------------------------------------------------------------------")
print("Performance of multi-domin identification")
print()

utils.SVM_Multi_Domain_Performance_Analyser(step2_correct_chains, multi_correct_chains)

print("----------------------------------------------------------------------------------------")
print()
print("#############################--------STEP 3--------#####################################")
print()

correct_chains_post_kmeans, incorrect_chains_post_kmeans = K_Means.applyKMeans(step2_correct_chains)

print("----------------------------------------------------------------------------------------")
print()
print("K-means Performance")
print()
utils.SVM_Multi_Domain_Performance_Analyser(correct_chains_post_kmeans, step2_correct_chains)

print()
print("#############################--------OVERALL PERFORMANCE--------#####################################")
print()
print()
total_correct_chains = correct_chains_post_kmeans + single_correct_chains
utils.SVM_Multi_Domain_Performance_Analyser(total_correct_chains, SVM_test_data)
