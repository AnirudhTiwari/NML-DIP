import SVM_v2
import common_functions as utils
import multiDomainIdentifier
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

def get_input_dataset_features_file(x):
	return {
		"Benchmark_2" : "Single Vs Multi Precalculated Features/BenchmarkTwo_singleVsMulti_features.csv",
		"Benchmark_3" : "Single Vs Multi Precalculated Features/BenchmarkThree_singleVsMulti_features.csv",
		"ASTRAL SCOP30" : "Single Vs Multi Precalculated Features/Astral_Scop30_singleVsMulti_features.csv",
		"NR_Dataset" : "Single Vs Multi Precalculated Features/NR_dataset_singleVsMulti_features.csv"
	}[x]

#Taking user input for test dataset
while 1:
	testing_dataset_input = raw_input("Input Testing Dataset: Type A for Benchmark_2, B for Benchmark_3, C for ASTRAL SCOP 30, D for NR_Dataset\n")
	try:
		testing_dataset = get_input_dataset_name(testing_dataset_input)
		if testing_dataset_input == 'E':
			testing_dataset = raw_input("Enter your chain for example: 1utgA\n")
		print "You selected " + testing_dataset + " for testing the SVM\n"
		break
	except KeyError:
		print "Invalid input!!"

print
print "#############################--------STEP 1--------#####################################"
print
print "CLASSIFYING SINGLE-DOMAIN vs MULTI-DOMAIN PROTEINS\n"
print 
feature_set = []
while 1:
	featureSet_input = raw_input("Select features to be used for training and testing:\nType L for Length\nType I for Interaction_Energy\nType R for Radius_of_Gyration\nType D for Density\nFor multiple features, give space sepearated input. For eg. L D for Length & Density\n").split()
	print "You selected: ",

	try:
		for features in featureSet_input:
			feature_set.append(get_input_feature_name(features))
			print get_input_feature_name(features),
		print
		break
	except KeyError:
		print "Invalid Input!!"

file_training_dataset_features = "single_vs_multi_training_dataset.csv"

print "----------------------------------------------------------------------------------------"
print 

with open(file_training_dataset_features) as f:
	SVM_train_data = f.readlines()

classifier = "single_vs_multiDomain"
if testing_dataset_input != 'E':
	file_testing_dataset_features = get_input_dataset_features_file(testing_dataset)

	with open(file_testing_dataset_features) as f:
		SVM_test_data = f.readlines()

else:
	SVM_test_data = calculateFeatures.calculateFeatures_v2([testing_dataset], feature_set, 2)[testing_dataset]
	print SVM_test_data

correct_chains_with_features, incorrect_chains_with_features = SVM_v2.classify(SVM_train_data, SVM_test_data, feature_set, classifier)

utils.SVM_Performance_Analyser(correct_chains_with_features, SVM_test_data, classifier)

correct_chains_output_file_name = "output_correct"+"_"+testing_dataset+"_"+classifier+"_"+str(time.time())+".csv"
inccorect_chains_with_features_output_file_name = "output_incorrect"+"_"+testing_dataset+"_"+classifier+"_"+str(time.time())+ ".csv"


f = open(correct_chains_output_file_name,"w+")
f1 = open(inccorect_chains_with_features_output_file_name, "w+")

multi_correct_chains = []
single_correct_chains = []
total_test_chains = []

for x in SVM_test_data:
	x = x.split(",")
	pdb = x[0].strip()
	chain = x[1].strip()
  	total_test_chains.append(pdb+chain)


for chain_with_features in incorrect_chains_with_features:
	f1.write("%s\n" % chain_with_features.strip())

f1.close()
shutil.move(inccorect_chains_with_features_output_file_name, OUTPUT_FOLDER+"/"+inccorect_chains_with_features_output_file_name)

print "----------------------------------------------------------------------------------------"
print
print "Saved incorrectly classified proteins to:", OUTPUT_FOLDER + "/" + inccorect_chains_with_features_output_file_name, "\n"


for chain_with_features in correct_chains_with_features:
  f.write("%s\n" % chain_with_features.strip())
  chain_with_features = chain_with_features.split(",")
  pdb = chain_with_features[0].strip()
  chain = chain_with_features[1].strip()
  domains = int(chain_with_features[2].strip())

  if domains > 1:
  	multi_correct_chains.append(pdb+chain)
  else:
  	single_correct_chains.append(pdb+chain)

f.close()
shutil.move(correct_chains_output_file_name, OUTPUT_FOLDER+"/"+correct_chains_output_file_name)

print "Saved correctly classified proteins to:", OUTPUT_FOLDER + "/" + correct_chains_output_file_name, "\n"


print "----------------------------------------------------------------------------------------"
print
print "#############################--------STEP 2--------#####################################"
print
print "CLASSIFYING MULTI-DOMAIN PROTEINS\n"
print

feature_set = []

while 1:
	featureSet_input = raw_input("Select features to be used for training and testing:\nType L for Length\nType I for Interaction_Energy\nType S for Density Sum\nType IS for IS-Sum\nFor multiple features, give space sepearated input. For ex. L IS for Length & IS-Sum\n").split()
	print "You selected: ",

	try:
		for features in featureSet_input:
			feature = get_input_feature_name(features)
			if feature == "IS_Sum":
				feature_set.append("IS-Sum_2")
				feature_set.append("IS-Sum_3")
				feature_set.append("IS-Sum_4")
			else:
				feature_set.append(get_input_feature_name(features))
			print get_input_feature_name(features),
		print
		break
	except KeyError:
		print "Invalid Input!!"

print "----------------------------------------------------------------------------------------"
print 


with open('self_created_multi_training_dataset_features_v5.json', 'r') as f:
    SVM_multi_train_data = json.load(f)

classifier = "multi-domain"

print "Feature set is ", feature_set

correct_chains_withDomains, incorrect_chains_withAssignedDomains = SVM_v2.classifyMultiDomainProteins_v2(SVM_multi_train_data, multi_correct_chains, feature_set, classifier)


print "Performance of multi-domin identification"

correct_chains = []
for chain in correct_chains_withDomains:
	correct_chains.append(chain[0].keys()[0])


utils.SVM_Multi_Domain_Performance_Analyser(correct_chains, multi_correct_chains)

print
print "#############################--------STEP 3--------#####################################"
print

correct_chains_post_kmeans, incorrect_chains_post_kmeans = K_Means.applyKMeans(correct_chains)

print
print "K-means Performance"
print
utils.SVM_Multi_Domain_Performance_Analyser(correct_chains_post_kmeans, correct_chains)


print
print "#############################--------OVERALL PERFORMANCE--------#####################################"
print

print
print "Overall Performance"
print
total_correct_chains = correct_chains_post_kmeans + single_correct_chains
utils.SVM_Multi_Domain_Performance_Analyser(total_correct_chains, total_test_chains)
