from sklearn import svm
import common_functions as utils
import stepOne

INPUT_PDB_LIST = ["1ddzA"]
SINGLE_VS_MULTI_DOMAIN_IDENTIFICATION_TRAINING_DATASET_FEATURES_FILE = "TrainingData/single_vs_multi_training_dataset.csv"
MULTI_DOMAIN_IDENTIFICATION_TRAINING_DATASET_FEATURES_FILE = "TrainingData/multiDomain_training_dataset_features.json"
SINGLE_VS_MULTI_FEATURE_SET = ["Length", "Interaction_Energy", "Density"]


def getSingleVsMultiDomainClassifier(singleVsMultiFeatureSet):
	with open(SINGLE_VS_MULTI_DOMAIN_IDENTIFICATION_TRAINING_DATASET_FEATURES_FILE) as f:
		SVM_train_data = f.readlines()
	f.close()

	X_train, y_train = utils.extractFeaturesAndLabelsForSVM(SVM_train_data, singleVsMultiFeatureSet, "single_vs_multiDomain")
	return svm.SVC(gamma='auto').fit(X_train, y_train)


singleVsMultiDomainClassifier = getSingleVsMultiDomainClassifier(SINGLE_VS_MULTI_FEATURE_SET)

for pdb in INPUT_PDB_LIST:
	print stepOne.classifySingleVsMultiDomainProtein(pdb, SINGLE_VS_MULTI_FEATURE_SET, singleVsMultiDomainClassifier)

# multiDomainClassifier = getMultiDomainClassifier(multiDomainClassificationFeatureSet)