'''
This file contains scripts to parse a pdb file and outputs relevant data.
'''

#Constants
PDB_FOLDER = "All PDBs/"

'''
This expects that the a 4 character pdbId is provided. For example: 1b5e.
This will return a list of all the chains by parsing the corresponding pdb file.
For 1b5e, it will return ['A', 'B']. The chains can be found by reading the TER
entry in the PDB file and its corresponding 21st character.
'''
def findChainsInTheGivenPDB(pdb):
	pdb_file_path = PDB_FOLDER + pdb + ".pdb"
	with open(pdb_file_path, 'r') as f:
		pdb_data = f.readlines()
	f.close()

	chains = []
	for line in pdb_data:
		if line[0]=='T' and line[1]=='E' and line[2]=='R':
			chains.append(line[21])
	return chains


