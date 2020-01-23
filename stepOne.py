import calculateFeatures
import numpy as np

def classifySingleVsMultiDomainProtein(pdbID, featureSet, stepOneClassifier):
	X_test = calculateFeatures.calculateFeatures_v2([pdbID], featureSet, 2)[pdbID]
	assigned_domains = stepOneClassifier.predict(np.array(X_test).reshape(1,-1))[0]
	return assigned_domains
	