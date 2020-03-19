#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import xml.etree.ElementTree as ET 


# In[2]:


#Global
studyNames = ['Framingham', 'JHS', 'COPDGene', 'MESA', 'Amish', 'CARDIA', 'HCHS', 'WHI', 'ARIC', 'CFS', 'CHS', 
               'Mayo_VTE', 'GOLDN', 'GenSALT', 'CCAF', 'SAS', 'SAGE', 'CRA', 'VAFAR', 'MGH_AF', 'HVH', 'Partners',
               'VU_AF', 'WGHS', 'GALAII', 'GeneSTAR', 'BAGS', 'Sarcoidosis', 'SAFS', 'GENOA', 'HyperGEN', 'THRV', 
               'DHS']

dataPath = '/data/'
dictPath = '/dict/'


# In[7]:


'''A helper function that finds all the positions of a given character in a string'''
def getAllPositionsOfCharacterInString(string, char):
    return [i for i, letter in enumerate(string) if letter == char]

'''It uses a simple pattern search to find the corresponding data files (Multiple consents) for each dict file'''
def getCorrespondingDataFilesForDictFile(dictFile, dataFilePath):
    cutOffPosition = getAllPositionsOfCharacterInString(dictFile, '.')[3]
    dataFileNamePrefix = dictFile[0:cutOffPosition]
    dataFiles = [fn for fn in os.listdir(dataFilePath) if fn.startswith(dataFileNamePrefix)]
    return dataFiles

def getPatientCountForVariable(data_df, colIndex):
    return (data_df.iloc[:, colIndex]).count()

'''The function that does it all. 
STEP 1: Opens dict files in turn. 
STEP 2: Extracts the variables from each dict file.
STEP 3: For each variable, it looks for patients entering values for that variable in the corresponding data file
STEP 4: Also does a check if at least one patient entered a value for the variable or not
RETURNS two different dataframes'''
def getPatientCountsForEveryVariable(studyName):
    dictFilePath = studyName + dictPath
    dataFilePath = studyName + dataPath
    dictFiles = [f for f in os.listdir(dictFilePath) if os.path.isfile(os.path.join(dictFilePath, f))]
    columnList = ['STUDY', 'PHV', 'LABEL', 'PATIENT_COUNT', 'DESCRIPTION']
    variables_df = pd.DataFrame(columns=columnList)
    unused_variables_df = pd.DataFrame(columns=columnList)
    
    for dictFile in dictFiles:
        dataFiles = getCorrespondingDataFilesForDictFile(dictFile, dataFilePath)
        data_df = pd.concat([pd.read_csv(dataFilePath + fn, sep='\t', comment='#') for fn in dataFiles if os.path.exists(dataFilePath + fn)], 
                            ignore_index=True)
        tree = ET.parse(dictFilePath + dictFile)
        root = tree.getroot()
        varbs = root.iter('variable')
    
        for i, varb in enumerate(root.iter('variable')):
            varb_id = varb.attrib.get('id')
            name = varb.find('name').text
            desc = varb.find('description').text
            pc = getPatientCountForVariable(data_df, i+1)
            new_row = pd.DataFrame([[studyName, varb_id, name, pc, desc]], columns=columnList)
            if pc > 0:
                variables_df = variables_df.append(new_row, ignore_index=True)
            else:
                unused_variables_df = unused_variables_df.append(new_row, ignore_index=True)
            
    return (variables_df, unused_variables_df)

'''A ring to bind them all'''
def main():
    for i, studyName in enumerate(studyNames):
        UsedVariablesDF, UnusedVariablesDF = getPatientCountsForEveryVariable(studyName)
        UsedVariableCount = UsedVariablesDF.shape[0]
        UnusedVariableCount = UnusedVariablesDF.shape[0]
        TotalVariableCount = UsedVariableCount + UnusedVariableCount
        print('{}. Study Name: {}'.format(i, studyName))
        print('There are {} variables in total in the dataset'.format(TotalVariableCount))
        print('{} variables have patient values associated with them'.format(UsedVariableCount))
        print('{} variables have NO patient values associated with them'.format(UnusedVariableCount))
        #UsedVariablesDF.to_csv(r'PatientsCountsForVariablesFromFHS.csv', header=True, index=None)


# In[8]:


main()

