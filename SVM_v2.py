import common_functions as utils
from sklearn import svm
import calculateFeatures
import numpy as np

def classify(training_data, testing_data, testing_data_features, feature_set, classification_type):
	X_train, y_train = utils.extractFeaturesAndLabelsForSVMFromJson(training_data, feature_set, classification_type)
	clf = svm.SVC(gamma='auto').fit(X_train, y_train)

	correct_chains = []
	incorrect_chains = []

	for chain in testing_data:
		chain = chain.strip()
		cath_domains = testing_data_features[chain]["Domains"]

		if cath_domains > 1:
			correct_label = "multi"
		else:
			correct_label = "single" 

		features = []
		for feature in feature_set:
			features.append(testing_data_features[chain][feature])

		assigned_domains = clf.predict(np.array(features).reshape(1,-1))[0]

		if assigned_domains == correct_label:
			correct_chains.append(chain)
		else:
			incorrect_chains.append(chain)

	return correct_chains, incorrect_chains

'''
This method is to be used when we are using the updated algorithm whereby we are using IS-Sum1, IS-Sum2, IS-Sum3 and Length as feature vectors. 
Thus, in this don't calculate the prediction confidence for each split, we use the SVM to classify in a single go by evaluating this 4-D feature vector.
Consult self_created_multi_training_dataset_features_v5.json to get an idea of the feature vector set that we will be calculating. NOTE: IF THE FEATURE SET
CONTAINS "Interaction_Energy" AS A FEATURE THAN IT WOULD BE TRANSLATED TO CORRESPONDING IS-SUM_2/3/4 BASED ON THE NUMBER OF DOMAINS IT IS SUPPOSED TO HAVE.
This function returns a list of list for correct and incorrect chains both. The fundamental list has 2 items [feature_map, AssignedDomains]
feature map looks like this -> "1a0hA": {
        "Domains": 2, 
        "IS-Sum_2": "1.03", 
        "IS-Sum_3": "4.61", 
        "IS-Sum_4": "28.7", 
        "Length": 159
    }
'''

def classifyMultiDomainProteins_v2(training_data, testing_data, testing_data_features, feature_set, classification_type):
	X_train, y_train = utils.extractFeaturesAndLabelsForSVMFromJson(training_data, feature_set, classification_type)
	correct_chains = []
	incorrect_chains = []

	clf = svm.SVC(probability=True, gamma='auto').fit(X_train, y_train)
	for chain in testing_data:
		domains = testing_data_features[chain]["Domains"]
		features = []

		for feature in feature_set:
			features.append(testing_data_features[chain][feature])

		assigned_domains = clf.predict(np.array(features).reshape(1,-1))[0]

		if assigned_domains == domains:
			correct_chains.append(chain)
		else:
			incorrect_chains.append(chain)

	return correct_chains, incorrect_chains


