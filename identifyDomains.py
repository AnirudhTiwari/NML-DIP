from builtins import str
from sklearn import svm
import common_functions as utils
import stepOne
import stepTwo
import stepThree
import json
import sys
import pdbParser

#Constants
SINGLE_VS_MULTI_DOMAIN_IDENTIFICATION_TRAINING_DATASET_FEATURES_FILE = "TrainingData/singleVsMultiTrainingDatasetFeatures.json"
MULTI_DOMAIN_IDENTIFICATION_TRAINING_DATASET_FEATURES_FILE = "TrainingData/multiDomainTrainingDatasetFeatures.json"
SINGLE_VS_MULTI_FEATURE_SET = ["Length", "Interaction_Energy", "Density"]
MULTI_DOMAIN_FEATURE_SET = ["Length", "IS-Sum_2", "IS-Sum_3", "IS-Sum_4"]
SINGLE_VS_MULTIDOMAIN = "single_vs_multiDomain"
MULTI_DOMAIN = "multi-domain"

def getSingleVsMultiDomainClassifier(singleVsMultiFeatureSet):
	with open(SINGLE_VS_MULTI_DOMAIN_IDENTIFICATION_TRAINING_DATASET_FEATURES_FILE, 'r') as f:
		svm_single_vs_multi_train_data = json.load(f)
	f.close()

	X_train, y_train = utils.extractFeaturesAndLabelsForSVMFromJson(svm_single_vs_multi_train_data, singleVsMultiFeatureSet, SINGLE_VS_MULTIDOMAIN)
	return svm.SVC(gamma='auto').fit(X_train, y_train)

def getMultiDomainClassifier(multiDomainFeatureSet):
	with open(MULTI_DOMAIN_IDENTIFICATION_TRAINING_DATASET_FEATURES_FILE, 'r') as f:
		svm_multi_train_data = json.load(f)
	f.close()

	X_train, y_train = utils.extractFeaturesAndLabelsForSVMFromJson(svm_multi_train_data, multiDomainFeatureSet, MULTI_DOMAIN)
	return svm.SVC(gamma='auto').fit(X_train, y_train)

def getTestDataset():
	with open(str(sys.argv[1]), 'r') as f:
		testDataset = f.readlines()
	return testDataset

def executeAlgorithmWhenTheNumberOfDomainsIsProvided(pdb, domains):
	print("##############################################################################")
	stepThree.applyKMeansWithPostProcessing(pdb, domains)

#This excepts the input as pdbId+Chain. For example: 1b5eB. 
def executeAlgorithmWhenPdbAndChainAreProvided(pdb):
	print("##############################################################################")
	label = stepOne.classifySingleVsMultiDomainProtein(pdb, SINGLE_VS_MULTI_FEATURE_SET, singleVsMultiDomainClassifier)
	if label=="multi":
		domains = stepTwo.classifyMultiDomainProteins(pdb, MULTI_DOMAIN_FEATURE_SET, multiDomainClassifier)
	else:
		domains = 1
	stepThree.applyKMeansWithPostProcessing(pdb, domains)

def executeAlgorithmWhenTheNumberOfDomainsIsNotProvided(pdb):
	if len(pdb)==5: #Implies that the user has provided the chain as an input
		print("##############################################################################")
		print("User provided the PDB: {} and Chain: {}".format(pdb[:4], pdb[4]))
		executeAlgorithmWhenPdbAndChainAreProvided(pdb)

	#Implies that the user has not provided the chain as an input 
	#and the algorithm is to be executed for all chains in the PDB
	elif len(pdb)==4:
		print("##############################################################################")
		print("User only provided the PDB, finding domains for every chain in the PDB:", pdb)
		chains = pdbParser.findChainsInTheGivenPDB(pdb)
		for chain in chains:
			executeAlgorithmWhenPdbAndChainAreProvided(pdb+chain)


#Main execution of the program begins here
testDataset = getTestDataset()
singleVsMultiDomainClassifier = getSingleVsMultiDomainClassifier(SINGLE_VS_MULTI_FEATURE_SET)
multiDomainClassifier = getMultiDomainClassifier(MULTI_DOMAIN_FEATURE_SET)

for entry in testDataset:
	if entry.isspace()!=True:
		entry = entry.strip()
		entry = entry.split()
		pdb = entry[0].strip()
		try:
			if len(entry)==2: #Implies that the user has provided the number of domains and only the last step is to be applied.
				domains = int(entry[1].strip())
				print("##############################################################################")
				print("User provided no. of domains: {} for PDB: {}, Chain: {}".format(domains, pdb[:4], pdb[4]))
				executeAlgorithmWhenTheNumberOfDomainsIsProvided(pdb, domains)
			
			else: #Implies that the user has not provided the number of domains and all the 3 steps of the algorithm is to be applied.
				executeAlgorithmWhenTheNumberOfDomainsIsNotProvided(pdb)
		except:
			print("Error finding domains for PDB: {}, please contact the developer for help.".format(pdb))
		print()
