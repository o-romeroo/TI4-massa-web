import pandas as pd
from rdkit.Chem.Crippen import MolLogP as CalcMolLogP
from rdkit.Chem import (
	AllChem, rdMolDescriptors, rdFingerprintGenerator
)

def physicochemical_descriptors(file):
	NumHAcceptors = {}
	NumHDonors = {}
	ExactMolWt = {}
	NumRotatableBonds = {}
	FractionCSP3 = {}
	TPSA = {}
	LogP_WildmanCrippen = {}

	for i in file['molecules']:
		NumHAcceptors[i.GetProp('_Name')] = rdMolDescriptors.CalcNumHBA(i) # CALC: number of hydrogen acceptors
		NumHDonors[i.GetProp('_Name')] = rdMolDescriptors.CalcNumHBD(i) # CALC: number of hydrogen donors
		ExactMolWt[i.GetProp('_Name')] = rdMolDescriptors.CalcExactMolWt(i) # CALC: molecular weight
		NumRotatableBonds[i.GetProp('_Name')] = rdMolDescriptors.CalcNumRotatableBonds(i) # CALC: number of rotatable bounds
		FractionCSP3[i.GetProp('_Name')] = rdMolDescriptors.CalcFractionCSP3(i) # CALC: sp3 carbon fraction
		TPSA[i.GetProp('_Name')] = rdMolDescriptors.CalcTPSA(i) # CALC: TPSA
		LogP_WildmanCrippen[i.GetProp('_Name')] = CalcMolLogP(i) # CALC: WildmanCrippen Log P

	file['NumHAcceptors'] = pd.Series(NumHAcceptors)
	file['NumHDonors'] = pd.Series(NumHDonors)
	file['ExactMolWt'] = pd.Series(ExactMolWt)
	file['NumRotatableBonds'] = pd.Series(NumRotatableBonds)
	file['FractionCSP3'] = pd.Series(FractionCSP3)
	file['TPSA'] = pd.Series(TPSA)
	file['LogP_WildmanCrippen'] = pd.Series(LogP_WildmanCrippen)
	return file

def atompairs_fingerprint(file):
	FP_dict = {}
	for i in file['molecules']:
		# Updated AtomPair Fingerprint (without count).
		# To use AtomPairCount use the function (fpgen.GetCountFingerprintAsNumPy).
		# 1) Determine the fingerprint generator using AtomPairs Fingerprint.
		# 2) Generate the numpy array fingerprint using the generator.
		# 3) Transform the np.array in list.
		fpgen = rdFingerprintGenerator.GetAtomPairGenerator(fpSize=1024)  # 1
		FPasBinary = fpgen.GetFingerprintAsNumPy(i)  # 2
		BinaryAsList = list(FPasBinary)  # 3

		# DEPRECATED (by RDKit):
		# 1) Determine the fingerprint of the molecule using AtomPairs Fingerprint.
		# 2) Convert fingerprint to text.
		# 3) Each bit of fingerprint will be a string item of a list.
		# FPasBitVect = rdMolDescriptors.GetHashedAtomPairFingerprintAsBitVect(
		# i, nBits=1024
		# ) # 1
		# FPasBinary = cDataStructs.BitVectToText(FPasBitVect) # 2
		# BinaryAsList = list(FPasBinary) # 3

		BinaryAsNewList = []
		for a in BinaryAsList:
			b = int(a) # Each bit of fingerprint will be a int item of a list.
			BinaryAsNewList.append(b)
		FP_dict[i.GetProp('_Name')] = BinaryAsNewList # Create a "molecule name":fingerprint dictionary.

	file['AtomPairs'] = pd.Series(FP_dict) # Add the fingerprint to the dataframe.
	return file
