# ProteinDomainIdentificationAlgorithm
Algorithm developed by Anirudh Tiwari and Dr. Nita Parekh for finding Structural Domains in Proteins. This is done by Anirudh Tiwari as part of MS by Research main project at CCNSB, IIIT Hyderabad under the guidance of Dr. Nita Parekh.

## Prequisites To Run The Algorithm
1. Python 2.7 or Python 3.x; Download & Install from [here](https://www.python.org/downloads/).
2. Scikit-learn module; the Scikit-learn module can be installed using Pip, install Pip from [here](https://pip.pypa.io/en/stable/installing/).
3. Git; Download and install Git from [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

There are two versions of the algorithm hosted on two separate branches of this repository. The code hosted on the *master* branch is to be used to reproduce the results on the 4 test datasets (details below). The code hosted on the *pdbTestBranch* can be used to test the algorithm on any PDB(s). 

The details of how to execute the code on the master branch can be found below. For details on how to run the code on the *pdbTestBranch*, read the README present on the corresponding branch.

## Branch: Master; Code to run on 4 test datasets ##
The code hosted on this branch this branch is to reproduce the results that we have presented in the paper on the four datasets, namely, **benchmark_2**, **benchmark_3**, **ASTRAL SCOP 30** & **NR_Dataset**. Follow the steps below on shell/Powershell/Terminal to execute the code:
1. `cd` to the directory of your choice and download the repository using git clone:

   ```$git clone https://github.com/AnirudhTiwari/ProteinDomainIdentificationAlgorithm.git```

2. Scoot to the repository: `$cd ProteinDomainIdentificationAlgorithm`

3. Start the execution by running: `$python Domain_Identification.py`

4. The program will take a few seconds to compile and will show a prompt which will ask you select a dataset out of the 4 datasets on which you want to run the code. Select the dataset by pressing the relevant key. The code has 3 steps out of which 2 will execute in a few seconds and the last step will take around a minute or two (max) for larger datasets like ASTRAL SCOP/NR_Dataset. The output of each step is explained below.

### Step 1: Classification Between Single- & Multi-domain Proteins.
The output of this step can look like this:

```
#############################--------STEP 1--------#####################################

CLASSIFYING SINGLE-DOMAIN vs MULTI-DOMAIN PROTEINS

Feature set is:  ['Length', 'Interaction_Energy', 'Density']

----------------------------------------------------------------------------------------
Performance of single vs multi-domain identification


Contiguous
Multi {'Correct': 51, 'Total': 66, 'Accuracy': '77.27%'}
Single {'Correct': 45, 'Total': 54, 'Accuracy': '83.33%'}
Total {'Correct': 96, 'Total': 120, 'Accuracy': '80.00%'}

Non-Contiguous
Multi {'Correct': 31, 'Total': 32, 'Accuracy': '96.88%'}
Single {'Correct': 0, 'Total': 0}
Total {'Correct': 31, 'Total': 32, 'Accuracy': '96.88%'}

Total
Multi {'Correct': 82, 'Total': 98, 'Accuracy': '83.67%'}
Single {'Correct': 45, 'Total': 54, 'Accuracy': '83.33%'}
Total {'Correct': 127, 'Total': 152, 'Accuracy': '83.55%'}


----------------------------------------------------------------------------------------
```

The algorithm first tells the user the features that are being used to train and test the SVM. Then, the performance of the SVM is presented. Here, the first blob under **Contiguous** shows the performance of our algorithm in identifying contiguous domains on single and multi-domain proteins. The second blob under **Non-Contiguous** shows the results on the non-contiguous domains. The final blob under **Total** shows the overall result on contiguous and non-contiguous domains combined. The accuracy is determined by comparing our results with CATH annotation.

### Step 2: Identification of Number of Domains in Multi-domain Proteins
The output of this step can look like this:

```
#############################--------STEP 2--------#####################################

CLASSIFYING MULTI-DOMAIN PROTEINS


Feature set is  ['Length', 'IS-Sum_2', 'IS-Sum_3', 'IS-Sum_4']

----------------------------------------------------------------------------------------
Performance of multi-domin identification

2-domain
Contiguous (34/35) 97.14%
Non-Contiguous (17/19) 89.47%
Total (51/54) 94.44%

3-domain
Contiguous (5/13) 38.46%
Non-Contiguous (6/11) 54.55%
Total (11/24) 45.83%

4-domain
Contiguous (1/3) 33.33%
Non-Contiguous (1/1) 100.00%
Total (2/4) 50.00%


Overall Results
Contiguous (40/51) 78.43%
Non-Contiguous (24/31) 77.42%
Total (64/82) 78.05%
----------------------------------------------------------------------------------------
```
Similarly to Step 1, the features used to train and test the SVM are displayed to the user. The performance of the algorithm is presented for each of 2-, 3- & 4-domain proteins with a breakdown of performance on contiguous and non-contiguous domains. The **Overall Results** shows the overall performance of the SVM in identification of the number of domains in multi-domain proteins.

### Step 3: Identification of Domain Boundaries
The output of this step can look like this
```
#############################--------STEP 3--------#####################################

----------------------------------------------------------------------------------------

K-means Performance

2-domain
Contiguous (33/34) 97.06%
Non-Contiguous (16/17) 94.12%
Total (49/51) 96.08%

3-domain
Contiguous (3/5) 60.00%
Non-Contiguous (4/6) 66.67%
Total (7/11) 63.64%

4-domain
Contiguous (0/1) 0.00%
Non-Contiguous (1/1) 100.00%
Total (1/2) 50.00%


Overall Results
Contiguous (36/40) 90.00%
Non-Contiguous (21/24) 87.50%
Total (57/64) 89.06%
```
The performance of the k-means algorithm is presented here on multi-domain proteins. The output is in the same format as the previous step. 

### Overall Performance
The overall performance of the algorithm is presented after all the 3 steps are complete. The performance of the algorithm in identifying all the n-domain proteins is presented. The output of which can look like this and is in the same format as the output of the previous two steps.
```
1-domain
Contiguous (45/54) 83.33%
Total (45/54) 83.33%

2-domain
Contiguous (33/49) 67.35%
Non-Contiguous (16/20) 80.00%
Total (49/69) 71.01%

3-domain
Contiguous (3/14) 21.43%
Non-Contiguous (4/11) 36.36%
Total (7/25) 28.00%

4-domain
Contiguous (0/3) 0.00%
Non-Contiguous (1/1) 100.00%
Total (1/4) 25.00%


Overall Results
Contiguous (81/120) 67.50%
Non-Contiguous (21/32) 65.62%
Total (102/152) 67.11%
```



