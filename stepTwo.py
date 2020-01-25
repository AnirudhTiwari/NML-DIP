import calculateFeatures
import numpy as np

def classifyMultiDomainProteins(pdbID, featureSet, stepTwoClassifier):
	X_test = calculateFeatures.calculateFeatures_v2([pdbID], featureSet, 2)[pdbID]
	return stepTwoClassifier.predict(np.array(X_test).reshape(1,-1))[0]
	
