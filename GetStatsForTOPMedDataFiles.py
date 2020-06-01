#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os

#Global
DirectoryParamStr = 'DirectoryName'
DataFileParamStr = 'DataFileName'
DictFileParamStr = 'DictFileName'
ConsentParamStr = 'ConsentParam'
SubjectIdParamStr = 'SubjectIdParam'
DataDirStr = '/data/'
#DictDirStr = '/dict/'

StudyListings = {
    "Framingham Heart Study" : {
        DirectoryParamStr : 'Framingham',
        DataFileParamStr : 'phs000007.v30.pht000182.v13.p11.Framingham_Subject.MULTI.txt',
        ConsentParamStr : 'consent_1217'
    },
    "COPDGene" : {
        DirectoryParamStr : 'COPDGene',
        DataFileParamStr : 'phs000179.v6.pht002237.v3.p2.COPDGene_Subject.MULTI.txt',
        DictFileParamStr : 'phs000179.v6.pht002239.v4.COPDGene_Subject_Phenotypes.data_dict.xml'
    },
    "Women's Health Initiative (WHI)" : {
        DirectoryParamStr : 'WHI',
        DataFileParamStr : 'phs000200.v11.pht000982.v8.p3.WHI_Subject.MULTI.txt'
    },
    "Mult-Ethnic Study of Atherosclerosis (MESA)" : {
        DirectoryParamStr : 'MESA-New',
        DataFileParamStr : 'phs000209.v13.pht001108.v4.p3.MESA_Subject.MULTI.txt'
    },
    "Atherosclerosis Risk in Communities (ARIC)" : {
        DirectoryParamStr : 'ARIC',
        DataFileParamStr : 'phs000280.v5.pht001440.v5.p1.ARIC_Subject.MULTI.txt'
    },
    "Cleveland Family Study (CFS)" : {
        DirectoryParamStr : 'CFS',
        DataFileParamStr : 'phs000284.v2.pht001899.v2.p1.CFS_CARe_Subject.MULTI.txt',
        DictFileParamStr : 'phs000284.v2.pht001902.v1.CFS_CARe_Subject_Phenotypes.data_dict.xml'
    },
    "Jackson Heart Study" : {
        DirectoryParamStr : 'JHS',
        DataFileParamStr : 'phs000286.v6.pht001920.v5.p2.JHS_Subject.MULTI.txt'
    }, 
    "Cardiovascular Health Study (CHS)" : {
        DirectoryParamStr : 'CHS',
        DataFileParamStr : 'phs000287.v6.pht001447.v4.p1.CHS_Subject.MULTI.txt',
        ConsentParamStr : 'gencons'
    },
    "GENEVA GWAS of Venous Thrombosis (VTE)" : {
        DirectoryParamStr : 'GENEVA_GWAS_VTE',
        DataFileParamStr : 'phs000289.v2.pht001883.v1.p1.Venous_Thrombosis_Subject.MULTI.txt',
        DictFileParamStr : 'phs000289.v2.pht001886.v2.Venous_Thrombosis_Subject_Phenotypes.data_dict.xml',
        SubjectIdParamStr : 'SUBJID'
    },
    "Genetics of Lipid Lowering Drugs and Diet Network (GOLDN)" : {
        DirectoryParamStr : 'GOLDN',
        DataFileParamStr : 'phs000741.v2.pht003915.v2.p1.GOLDN_Lipid_Lowering_Subject.MULTI.txt',
        DictFileParamStr : 'phs000741.v2.pht003918.v2.GOLDN_Lipid_Lowering_Subject_Phenotypes.data_dict.xml',
        ConsentParamStr : 'consent'
    },
    "Genetic Epidemiology Network of Salt Study (GenSALT)" : {
        DirectoryParamStr : 'GenSALT',
        DataFileParamStr : 'phs000784.v2.pht004283.v1.p1.GenSalt_Subject.MULTI.txt',
        DictFileParamStr : 'phs000784.v2.pht004286.v1.GenSalt_Subject_Phenotypes.data_dict.xml',
        ConsentParamStr : 'Consent'
    },
    "Cleveland Clinic Foundation's Lone Atrial Fibrillation GWAS (CCAF)" : {
        DirectoryParamStr : 'CCF_AFIB_GWAS',
        DataFileParamStr : 'phs000820.v1.pht004330.v1.p1.Lone_Atrial_Fibrillation_Subject.MULTI.txt',
        DictFileParamStr : 'phs000820.v1.pht004332.v1.Lone_Atrial_Fibrillation_Subject_Phenotypes.data_dict.xml',
        ConsentParamStr : 'consent'
    },
    "Study of Adiposity in Samoans (SAS)" : {
        DirectoryParamStr : 'SAS',
        DataFileParamStr : 'phs000914.v1.pht005251.v1.p1.Samoans_Adiposity_Subject.MULTI.txt',
        DictFileParamStr : 'phs000914.v1.pht005253.v1.Samoans_Adiposity_Subject_Phenotypes.data_dict.xml'
    },
    "Genes-environments and Admixture in Latino Asthmatics (GALA II) - Genomic" : {
        DirectoryParamStr : 'GALAII_WGS',
        DataFileParamStr : 'phs000920.v3.pht004897.v3.p2.TOPMed_WGS_GALAII_Subject.MULTI.txt',
        DictFileParamStr : 'phs000920.v3.pht004900.v3.TOPMed_WGS_GALAII_Sample_Attributes.data_dict.xml'
    },
    "Study of African-Americans, Asthma, Genes, and Environments (SAGE)" : {
        DirectoryParamStr : 'SAGE',
        DataFileParamStr : 'phs000921.v3.pht004881.v3.p1.TOPMed_WGS_SAGE_Subject.MULTI.txt',
        DictFileParamStr : 'phs000921.v3.pht004883.v3.TOPMed_WGS_SAGE_Subject_Phenotypes.data_dict.xml'
    }, 
    "Boston Early-Onset COPD Study (EOCOPD)" : {
        DirectoryParamStr : 'Boston_COPD',
        DataFileParamStr : 'phs000946.v3.pht004972.v2.p1.TOPMed_WGS_Boston_EO_COPD_Subject.MULTI.txt',
        DictFileParamStr : 'phs000946.v3.pht005719.v1.TOPMed_WGS_Boston_EO_COPD_Subject_Phenotypes.data_dict.xml'
    },
    "COPDGene-Genomic" : {
        DirectoryParamStr : 'COPDGene_WGS',
        DataFileParamStr : 'phs000951.v3.pht005050.v3.p3.TOPMed_WGS_COPDGene_Subject.MULTI.txt'
    }, 
    "Cleveland Family Study - Genomic (CFS)" : {
        DirectoryParamStr : 'CFS_WGS',
        DataFileParamStr : 'phs000954.v2.pht006297.v1.p1.TOPMed_WGS_CFS_Subject.MULTI.txt'
    },
    "Genetic of Cardiometabolic Health in Amish (Amish)" : {
        DirectoryParamStr : 'Amish',
        DataFileParamStr : 'phs000956.v3.pht005000.v1.p1.TOPMed_WGS_Amish_Subject.MULTI.txt',
        DictFileParamStr : 'phs000956.v3.pht005002.v1.TOPMed_WGS_Amish_Subject_Phenotypes.data_dict.xml'
    }, 
    "Jackson Heart Study - Genomic (JHS)" : {
        DirectoryParamStr : 'JHS_WGS',
        DataFileParamStr : 'phs000964.v3.pht004838.v1.p1.TOPMed_WGS_JHS_Subject.MULTI.txt'
    },
    "Study of Adiposity in Samoans - Genomic (SAS)" : {
        DirectoryParamStr : 'SAS_WGS',
        DataFileParamStr : 'phs000972.v4.pht005679.v1.p1.TOPMed_WGS_Samoans_Adiposity_Subject.MULTI.txt'
    },
    "Framingham Heart Study - Genomic" : {
        DirectoryParamStr : 'Framingham_WGS',
        DataFileParamStr : 'phs000974.v3.pht004909.v2.p2.TOPMed_WGS_FHS_Subject.MULTI.txt'
    },
    "Genetic Epidemiology of Asthma in Costa Rica (CRA)" : {
        DirectoryParamStr : 'CRA',
        DataFileParamStr : 'phs000988.v3.pht005245.v3.p1.TOPMed_WGS_Asthma_Costa_Rica_Subject.MULTI.txt'
    },
    "Heart and Vascular Heart - Genomic (HVH)" : {
        DirectoryParamStr : 'HVH_WGS',
        DataFileParamStr : 'phs000993.v3.pht005013.v2.p2.TOPMed_WGS_HVH_Subject.MULTI.txt'
    },
    "Vanderbilt Atrial Fibrillation Ablation Registry (VAFAR)" : {
        DirectoryParamStr : 'VU_AF_WGS',
        DataFileParamStr : 'phs000997.v3.pht005087.v3.p2.TOPMed_WGS_VAFAR_Subject.MULTI.txt',
        DictFileParamStr : 'phs000997.v3.pht005688.v3.TOPMed_WGS_VAFAR_Subject_Phenotypes.data_dict.xml'
    },
    "MGH Atrial Fibrillation Study (MGH_AF)" : {
        DirectoryParamStr : 'MGH_AF',
        DataFileParamStr : 'phs001001.v1.pht005653.v1.p1.MGH_AF_Subject.MULTI.txt',
        DictFileParamStr : 'phs001001.v1.pht005655.v1.MGH_AF_Subject_Phenotypes.data_dict.xml'
    },
    "Heart and Vascular Health Study (HVH)" : {
        DirectoryParamStr : 'HVH',
        DataFileParamStr : 'phs001013.v3.pht005309.v3.p2.HVH_Subject.MULTI.txt',
        DictFileParamStr : 'phs001013.v3.pht005311.v2.HVH_Subject_Phenotypes.data_dict.xml',
        ConsentParamStr : 'SUBJECT_ID' #Because of a shift in the columns in this file
    },
    "Partners Health Care Biobank (Partners)" : {
        DirectoryParamStr : 'Partners',
        DataFileParamStr : 'phs001024.v3.pht005116.v2.p1.TOPMed_WGS_Partners_AFGen_Subject.MULTI.txt',
        DictFileParamStr : 'phs001024.v3.pht005693.v1.TOPMed_WGS_Partners_AFGen_Subject_Phenotypes.data_dict.xml'
    }, 
    "Vanderbilt Atrial Fibrillation Registry (VU_AF)" : {
        DirectoryParamStr : 'VU_AF',
        DataFileParamStr : 'phs001032.v4.pht005098.v2.p2.TOPMed_WGS_VUH_AF_Subject.MULTI.txt',
        DictFileParamStr : 'phs001032.v4.pht005675.v3.TOPMed_WGS_VUH_AF_Subject_Phenotypes.data_dict.xml'
    },
    "Novel Risk Factors for Development of Atrial Fibrillation in Women (WGHS)" : {
        DirectoryParamStr : 'WGHS',
        DataFileParamStr : 'phs001040.v3.pht005203.v2.p1.TOPMed_WGS_WGHS_Subject.MULTI.txt',
        DictFileParamStr : 'phs001040.v3.pht005682.v3.TOPMed_WGS_WGHS_Subject_Phenotypes.data_dict.xml'
    },
    "MGH Atrial Fibrillation Study - Genomic (MGH_AF)" : {
        DirectoryParamStr : 'MGH_AF_WGS',
        DataFileParamStr : 'phs001062.v3.pht005261.v2.p2.TOPMed_WGS_MGH_AF_Subject.MULTI.txt'
    },
    "Genetic Study of Atherosclerosis Risk (GeneSTAR)" : {
        DirectoryParamStr : 'GeneSTAR',
        DataFileParamStr : 'phs001074.v1.pht005339.v1.p1.GeneSTAR_Platelet_Aggregation_iPS_MKs_Subject.MULTI.txt',
        DictFileParamStr : 'phs001074.v1.pht005342.v1.GeneSTAR_Platelet_Aggregation_iPS_MKs_Subject_Phenotypes.data_dict.xml'
    },
    "Genetics and Epidemiology of Asthma in Barbados (BAGS)" : {
        DirectoryParamStr : 'BAGS',
        DataFileParamStr : 'phs001143.v2.pht005902.v1.p1.TOPMed_WGS_BAGS_Subject.MULTI.txt',
        DictFileParamStr : 'phs001143.v2.pht005905.v2.TOPMed_WGS_BAGS_Subject_Phenotypes.data_dict.xml'
    }, 
    "Genes-Environments and Admixture in Latino Asthmatics (GALA II)" : {
        DirectoryParamStr : 'GALAII',
        DataFileParamStr : 'phs001180.v1.pht006988.v1.p1.GALAII_Subject.MULTI.txt',
        DictFileParamStr : 'phs001180.v1.pht006991.v1.GALAII_Subject_Phenotypes.data_dict.xml'
    }, 
    "Cleveland Clinic Atrial Fibrillation Study - Genomic (CCAF)" : {
        DirectoryParamStr : 'CCAF',
        DataFileParamStr : 'phs001189.v2.pht005977.v2.p1.TOPMed_WGS_CCAF_Subject.MULTI.txt',
        DictFileParamStr : 'phs001189.v2.pht005979.v2.TOPMed_WGS_CCAF_Subject_Phenotypes.data_dict.xml'
    }, 
    "African American Sarcoidosis Genetic Resource (Sarcoidosis)" : {
        DirectoryParamStr : 'Sarcoidosis',
        DataFileParamStr : 'phs001207.v1.pht005790.v1.p1.TOPMed_WGS_AA_Sarcoidosis_Subject.MULTI.txt',
        DictFileParamStr : 'phs001207.v1.pht005793.v1.TOPMed_WGS_AA_Sarcoidosis_Subject_Phenotypes.data_dict.xml'
    }, 
    "Atherosclerosis Risk in Communities - Genomic (ARIC)" : {
        DirectoryParamStr : 'ARIC_WGS',
        DataFileParamStr : 'phs001211.v2.pht005754.v2.p2.TOPMed_WGS_ARIC_Subject.MULTI.txt'
    }, 
    "San Antonio Family Heart Study (SAFHS)" : {
        DirectoryParamStr : 'SAFS',
        DataFileParamStr : 'phs001215.v2.pht008628.v2.p2.TOPMed_WGS_SAFHS_Subject.MULTI.txt',
        DictFileParamStr : 'phs001215.v2.pht008631.v2.TOPMed_WGS_SAFHS_Subject_Phenotypes.data_dict.xml'
    },
    "Genetic Epidemiology of Salt Sensitivity - Genomic (GenSALT)" : {
        DirectoryParamStr : 'GenSALT_WGS',
        DataFileParamStr : 'phs001217.v1.pht007761.v1.p1.TOPMed_WGS_GenSalt_Subject.MULTI.txt',
        DictFileParamStr : 'phs001217.v1.pht007764.v1.TOPMed_WGS_GenSalt_Subject_Phenotypes.data_dict.xml'
    },
    "Genetic Study of Atherosclerosis Risk - Genomic (GeneSTAR)" : {
        DirectoryParamStr : 'GeneSTAR_WGS',
        DataFileParamStr : 'phs001218.v1.pht005957.v1.p1.TOPMed_WGS_GeneSTAR_Subject.MULTI.txt',
        DictFileParamStr : 'phs001218.v1.pht007766.v1.TOPMed_WGS_GeneSTAR_Subject_Phenotypes.data_dict.xml'
    }, 
    "Women's Health Initiative - Genomic (WHI)" : {
        DirectoryParamStr : 'WHI_WGS',
        DataFileParamStr : 'phs001237.v1.pht005987.v1.p1.TOPMed_WGS_WHI_Subject.MULTI.txt'
    },
    "Genetic Epidemiology Network of Arteriopathy (GENOA)" : {
        DirectoryParamStr : 'GENOA',
        DataFileParamStr : 'phs001238.v2.pht006028.v2.p1.GENOA_Subject.MULTI.txt'
    },
    "Genetics of Left Ventricular Hypertrophy (HyperGEN)" : {
        DirectoryParamStr : 'HyperGEN',
        DataFileParamStr : 'phs001293.v1.pht008893.v1.p1.TOPMed_WGS_HyperGEN_Subject.MULTI.txt',
        DictFileParamStr : 'phs001293.v1.pht008896.v1.TOPMed_WGS_HyperGEN_Subject_Phenotypes.data_dict.xml'
    }, 
    "Genetic Epidemiology Network of Arteriopathy - Genomic (GENOA)" : {
        DirectoryParamStr : 'GENOA_WGS',
        DataFileParamStr : 'phs001345.v1.pht008602.v1.p1.TOPMed_WGS_GENOA_Subject.MULTI.txt'
    },
    "Genetics of Lipid Lowering Drugs and Diet Network - Genomic (GOLDN)" : {
        DirectoryParamStr : 'GOLDN_WGS',
        DataFileParamStr : 'phs001359.v1.pht008688.v1.p1.TOPMed_WGS_GOLDN_Subject.MULTI.txt'
    },
    "Cardiovascular Health Study - Genomic (CHS)" : {
        DirectoryParamStr : 'CHS_WGS',
        DataFileParamStr : 'phs001368.v1.pht007957.v1.p1.TOPMed_WGS_CHS_VTE_Subject.MULTI.txt'
    }, 
    "Rare Variants for Hypertension in Taiwan Chinese (THRV)" : {
        DirectoryParamStr : 'THRV',
        DataFileParamStr : 'phs001387.v1.pht008967.v1.p1.TOPMed_WGS_THRV_Subject.MULTI.txt',
        DictFileParamStr : 'phs001387.v1.pht008970.v1.TOPMed_WGS_THRV_Subject_Phenotypes.data_dict.xml'
    },
    "GWAS of Venous Thrombosis - Genomic (VTE)" : {
        DirectoryParamStr : 'Mayo_VTE_WGS',
        DataFileParamStr : 'phs001402.v2.pht008237.v2.p1.TOPMed_WGS_Mayo_VTE_Subject.MULTI.txt',
        DictFileParamStr : 'phs001402.v2.pht008239.v1.TOPMed_WGS_Mayo_VTE_Subject_Phenotypes.data_dict.xml'
    },
    "Diabetes Heart Study (DHS) African American Coronary Artery Calcification (AA CAC)" : {
        DirectoryParamStr : 'DiabetesHeartStudy',
        DataFileParamStr : 'phs001412.v1.pht006743.v1.p1.TOPMed_WGS_DHS_Subject.MULTI.txt',
        DictFileParamStr : 'phs001412.v1.pht006746.v1.TOPMed_WGS_DHS_Subject_Phenotypes.data_dict.xml'
    },
    "MESA and MESA Family AA-CAC" : {
        DirectoryParamStr : 'AA_CAC',
        DataFileParamStr : 'phs001416.v2.pht009013.v1.p1.TOPMed_WGS_MESA_Subject.MULTI.txt'
    }
}

def GetPatientAndConsentCountsForStudy(CallCount, StudyName, Directry, FileName, ConsentParam, SubjIdParam):
    print str(CallCount) + ". Processing " + StudyName
    print "Subject File: " + FileName
    FileAndPath = Directry + DataDirStr + FileName
    SubjectDF = pd.read_csv(FileAndPath, sep="\t", comment="#")
    
    PatientCt = len(pd.unique(SubjectDF[SubjIdParam]))
    print "Found " + str(PatientCt) + " patients in study"

    ConsentLevels = pd.unique(SubjectDF[ConsentParam])
    print "Consent Levels: " + str(ConsentLevels) 
    
    Consent0DF = SubjectDF.loc[SubjectDF[ConsentParam] == 0]
    Consent0PatientCt = len(pd.unique(Consent0DF[SubjIdParam]))
    print str(Consent0PatientCt) + " patients had Consent Level 0"
    
    Consent1DF = SubjectDF.loc[SubjectDF[ConsentParam] == 1]
    Consent1PatientCt = len(pd.unique(Consent1DF[SubjIdParam]))
    print str(Consent1PatientCt) + " patients had Consent Level 1"
    
    Consent2DF = SubjectDF.loc[SubjectDF[ConsentParam] == 2]
    Consent2PatientCt = len(pd.unique(Consent2DF[SubjIdParam]))
    print str(Consent2PatientCt) + " patients had Consent Level 2"
    
    Consent3DF = SubjectDF.loc[SubjectDF[ConsentParam] == 3]
    Consent3PatientCt = len(pd.unique(Consent3DF[SubjIdParam]))
    print str(Consent3PatientCt) + " patients had Consent Level 3"
    print
    return str(PatientCt), str(ConsentLevels), str(Consent0PatientCt), str(Consent1PatientCt), str(Consent2PatientCt), str(Consent3PatientCt)


def CompileDataFrameWithResults():
    ResultDF = pd.DataFrame(columns=['StudyName', 'AccessionNumber', 'PatientCount', 'ConsentLevels', 'Consent0PatientCount', 'Consent1PatientCount', 'Consent2PatientCount', 'Consent3PatientCount'])
    SerNum = 1
    
    for StudyName in StudyListings.keys():
        ConsentParam = 'CONSENT'
        SubjectIdParam = 'dbGaP_Subject_ID'
        ParamsForStudy = StudyListings.get(StudyName)
        Directory = ParamsForStudy.get(DirectoryParamStr)
        FileName = ParamsForStudy.get(DataFileParamStr)
        AccessionNumber = FileName.split('.')[0]
        
        if ParamsForStudy.has_key(ConsentParamStr):
            ConsentParam = ParamsForStudy.get(ConsentParamStr)
        if ParamsForStudy.has_key(SubjectIdParamStr):
            SubjectIdParam = ParamsForStudy.get(SubjectIdParamStr)
        
        PatientCount, ConsentLevels, Consent0PatientCount, Consent1PatientCount, Consent2PatientCount, Consent3PatientCount = GetPatientAndConsentCountsForStudy(SerNum, StudyName, Directory, FileName, ConsentParam, SubjectIdParam)
        ResultDF = ResultDF.append({'StudyName' : StudyName, 'AccessionNumber' : AccessionNumber, 'PatientCount' : PatientCount, 'ConsentLevels' : ConsentLevels, 'Consent0PatientCount' : Consent0PatientCount, 'Consent1PatientCount' : Consent1PatientCount, 'Consent2PatientCount' : Consent2PatientCount,  'Consent3PatientCount' : Consent3PatientCount}, ignore_index=True)
        
        SerNum += 1   
    return ResultDF


def main():
    ResultDF = CompileDataFrameWithResults()
    ResultDF.to_csv(r'PatientsCountsByConsentsForFreeze5bStudies.csv', header=True, index=None)



main()