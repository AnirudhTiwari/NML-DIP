from sklearn import svm
import common_functions as utils
import stepOne
import stepTwo
import stepThree
import json

INPUT_PDB_LIST = ["1ddzA", "1uc8A", "1tuhA"]
SINGLE_VS_MULTI_DOMAIN_IDENTIFICATION_TRAINING_DATASET_FEATURES_FILE = "TrainingData/single_vs_multi_training_dataset.csv"
MULTI_DOMAIN_IDENTIFICATION_TRAINING_DATASET_FEATURES_FILE = "TrainingData/multiDomain_training_dataset_features.json"
SINGLE_VS_MULTI_FEATURE_SET = ["Length", "Interaction_Energy", "Density"]
MULTI_DOMAIN_FEATURE_SET = ["Length", "IS-Sum_2", "IS-Sum_3", "IS-Sum_4"]
SINGLE_VS_MULTIDOMAIN = "single_vs_multiDomain"
MULTI_DOMAIN = "multi-domain"

def getSingleVsMultiDomainClassifier(singleVsMultiFeatureSet):
	with open(SINGLE_VS_MULTI_DOMAIN_IDENTIFICATION_TRAINING_DATASET_FEATURES_FILE, 'r') as f:
		svm_single_vs_multi_train_data = f.readlines()
	f.close()

	X_train, y_train = utils.extractFeaturesAndLabelsForSVM(svm_single_vs_multi_train_data, singleVsMultiFeatureSet, SINGLE_VS_MULTIDOMAIN)
	return svm.SVC(gamma='auto').fit(X_train, y_train)

def getMultiDomainClassifier(multiDomainFeatureSet):
	with open(MULTI_DOMAIN_IDENTIFICATION_TRAINING_DATASET_FEATURES_FILE, 'r') as f:
		svm_multi_train_data = json.load(f)
	f.close()

	X_train, y_train = utils.extractFeaturesAndLabelsForSVMFromJson(svm_multi_train_data, multiDomainFeatureSet, MULTI_DOMAIN)
	return svm.SVC(gamma='auto').fit(X_train, y_train)


singleVsMultiDomainClassifier = getSingleVsMultiDomainClassifier(SINGLE_VS_MULTI_FEATURE_SET)
multiDomainClassifier = getMultiDomainClassifier(MULTI_DOMAIN_FEATURE_SET)

for pdb in INPUT_PDB_LIST:
	label = stepOne.classifySingleVsMultiDomainProtein(pdb, SINGLE_VS_MULTI_FEATURE_SET, singleVsMultiDomainClassifier)

	if label=="multi":
		domains = stepTwo.classifyMultiDomainProteins(pdb, MULTI_DOMAIN_FEATURE_SET, multiDomainClassifier)
	else:
		domains = 1

	stepThree.applyKMeansWithPostProcessing(pdb, domains)
	
		

