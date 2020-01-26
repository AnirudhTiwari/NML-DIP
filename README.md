# ProteinDomainIdentificationAlgorithm
Algorithm developed by Anirudh Tiwari and Dr. Nita Parekh for finding Structural Domains in Proteins. This is done by Anirudh Tiwari as part of MS by Research main project at CCNSB, IIIT Hyderabad under the guidance of Dr. Nita Parekh.

## Prequisites To Run The Algorithm
1. Python 2.7 or Python 3.x; Download & Install from [here](https://www.python.org/downloads/).
2. Scikit-learn module; the Scikit-learn module can be installed using Pip, install Pip from [here](https://pip.pypa.io/en/stable/installing/).
3. Git; Download and install Git from [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

There are two versions of the algorithm hosted on two separate branches of this repository. The code hosted on the *master* branch is to be used to execute the algorithm on the 4 test datasets (details below). The code hosted on the *pdbTestBranch* can be used to test the algorithm on any PDB(s). 

The details of how to execute the code on the *pdbTestBranch* can be found below. For details on how to run the code on the *master*, read the README present on the corresponding branch.

## Branch: pdbTestBranch ##
The code hosted on this branch is to be used to test our algorithm on any PDBs. Follow the steps below on shell/Powershell/Terminal to execute the code:

1. `cd` to the directory of your choice and download the repository using git clone:

   ```$git clone https://github.com/AnirudhTiwari/ProteinDomainIdentificationAlgorithm.git```

2. Scoot to the repository: `$cd ProteinDomainIdentificationAlgorithm`

3. Switch to the remote *pdbTestBranch*: 
```
$git fetch origin
$git checkout --track origin/pdbTestBranch
```

4. Now you are on the *pdbTestBranch*, the code expects the user to provide a file containing PDB entries with chains for which the algorithm should be executed. We have provided a sample test file (sampleTestDataset.txt) and it looks like this.
```
1ddzA
1uc8A
1tuhA
1s0fA
```
The first four characters denotes the name of the PDB entry and the last character (in uppercase) represents the chain. 

### Important Note
Please note that **the input file compulsarily needs to be in this format** otherwise the program will not work. Also, please **download the corresponding PDB file(s) from [RCSB](https://www.rcsb.org/) and move them to the `All PDBs` folder** as the program calculates the feature vectors by parsing the PDB files and it expects the PDB files to be present in the `All PDBs` folder.

5. Once you have downloaded all the relevant PDB files to the `All PDBs` folder and created a file containing the name and the chain of the PDB entries for which you want to execute the algorithm, then on your terminal type this
```
$python identifyDomains.py sampleTestDataset.txt 
```
Here replace the `sampleTestDataset.txt` with the name of the file that you have created or just execute this line to see how the algorithm works on our provided sample dataset.

6. The output of the algorithm can be something like this
```
#########################################################################
PDB: 1ddz, Chain: A
Number of domains: 2
Domain 1 :  142 - 392

Domain 2 :  84 - 141    393 - 564
#########################################################################
PDB: 1uc8, Chain: A
Number of domains: 1
Domain 1 :  1 - 280
#########################################################################
PDB: 1tuh, Chain: A
Number of domains: 1
Domain 1 :  19 - 149
#########################################################################
PDB: 1s0f, Chain: A
Number of domains: 4
Domain 1 :  1 - 199    221 - 401    483 - 523

Domain 2 :  458 - 482    655 - 704    779 - 845

Domain 3 :  200 - 220    402 - 457    524 - 654    705 - 778

Domain 4 :  846 - 1290
```
Here, the algorithm provides domain annotation for each entry in the test dataset separated by horizontal line of "#". The output denotes the number of domains identified by the algorithm in given protein and displays the domain boundaries for each domain. The non-contiguous domains are separated by a tab character (4 spaces). 
