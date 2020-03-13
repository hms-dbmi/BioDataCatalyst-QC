#!/usr/bin/env python
# coding: utf-8

# # PIC-SURE API use-case: Export All Variables from all of the studies in BioData Catalyst (Freeze 5b)

# ## PIC-SURE python API 
# ### What is PIC-SURE? 
# 
# <!--img src="./img/PIC-SURE_logo.png" width= "360px"> -->
# 
# Databases exposed through PIC-SURE API encompass a wide heterogeneity of architectures and data organizations underneath. PIC-SURE hide this complexity and expose the different databases in the same format, allowing researchers to focus on the analysis and medical insights, thus easing the process of reproducible sciences.
# 
# ### More about PIC-SURE
# PIC-SURE stands for Patient-centered Information Commons: Standardized Unification of Research Elements. The API is available in two different programming languages, python and R, allowing investigators to query databases in the same way using any of those languages.
# 
# PIC-SURE is a large project from which the R/python PIC-SURE API is only a brick. Among other things, PIC-SURE also offers a graphical user interface, allowing research scientist to get quick knowledge about variables and data available for a specific data source.
# 
# The python API is actively developed by the Avillach-Lab at Harvard Medical School.
# 
# GitHub repo:
# * https://github.com/hms-dbmi/pic-sure-python-adapter-hpds
# * https://github.com/hms-dbmi/pic-sure-python-client
# 
# 

# # Getting your own user-specific security token

# **Before running this notebook, please be sure to review the get_your_token.ipynb notebook. It contains explanation about how to get a security token, mandatory to access the databases.**

# # Environment set-up

# ### Pre-requisite
# - python 3.6 or later (although earlier versions of Python 3 must work too)
# - pip: python package manager, already available in most system with a python interpreter installed ([pip installation instructions](https://pip.pypa.io/en/stable/installing/))

# ### IPython magic command
# 
# Those two lines of code below do load the `autoreload` IPython extension. Although not necessary to execute the rest of the Notebook, it does enable to reload every dependency each time python code is executed, thus enabling to take into account changes in external file imported into this Notebook (e.g. user defined function stored in separate file), without having to manually reload libraries. Turns out very handy when developing interactively. More about [IPython Magic commands](https://ipython.readthedocs.io/en/stable/interactive/magics.html).

# In[1]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# ### Installation of required python packages
# 
# Using the pip package manager, we install the packages listed in the `requirements.txt` file.

# In[2]:


get_ipython().system('cat requirements.txt')


# In[3]:


import sys
get_ipython().system('{sys.executable} -m pip install --upgrade pip')
get_ipython().system('{sys.executable} -m pip install -r requirements.txt')


# In[4]:


get_ipython().system('{sys.executable} -m pip install --upgrade --force-reinstall git+https://github.com/hms-dbmi/pic-sure-python-adapter-hpds.git')
get_ipython().system('{sys.executable} -m pip install --upgrade --force-reinstall git+https://github.com/hms-dbmi/pic-sure-python-client.git')


# Import all the external dependencies, as well as user-defined functions stored in the `python_lib` folder

# In[5]:


import json
from pprint import pprint

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from scipy import stats

import PicSureHpdsLib
import PicSureClient

from python_lib.utils import get_multiIndex_variablesDict, joining_variablesDict_onCol


# In[6]:


print("NB: This Jupyter Notebook has been written using PIC-SURE API following versions:\n- PicSureClient: 1.1.0\n- PicSureHpdsLib: 1.1.0\n")
print("The PIC-SURE API libraries versions you've been downloading are: \n- PicSureClient: {0}\n- PicSureHpdsLib: {1}".format(PicSureClient.__version__, PicSureHpdsLib.__version__))


# ##### Set up the options for displaying tables and plots in this Notebook

# In[7]:


# Pandas DataFrame display options
pd.set_option("max.rows", 100)

# Matplotlib display parameters
plt.rcParams["figure.figsize"] = (14,8)
font = {'weight' : 'bold',
        'size'   : 12}
plt.rc('font', **font)


# ### Connecting to a PIC-SURE network

# Several information are needed to get access to data through the PIC-SURE API: a network URL, a resource id, and a user security token which is specific to a given URL + resource.

# In[8]:


PICSURE_network_URL = "<pic-sure_URL>"
resource_id = "<resource_id>"
token_file = "token.txt"


# In[9]:


with open(token_file, "r") as f:
    my_token = f.read()


# In[10]:


client = PicSureClient.Client()
connection = client.connect(PICSURE_network_URL, my_token)
adapter = PicSureHpdsLib.Adapter(connection)
resource = adapter.useResource(resource_id)


# Two objects are created here: a `connection` and a `resource` object, using respectively the `picsure` and `hpds` libraries. 
# 
# As we will only be using one single resource, **the `resource` object is actually the only one we will need to proceed with data analysis hereafter** (the `connection` object is useful to get access to different databases stored in different resources). 
# 
# It is connected to the specific data source ID we specified, and enables to query and retrieve data from this source.

# ### Getting help with the PIC-SURE python API

# Each object exposed by the PicSureHpdsLib library got a `help()` method. Calling it will print out a helper message about it. 

# In[11]:


resource.help()


# For instance, this output tells us that this `resource` object got 2 methods, and it gives insights about their function. 

# ## Using the *variables dictionary*

# Once connection to the desired resource has been established, we first need to get a quick grasp of which variables are available in the database. To this end, we will use the `dictionary` method of the `resource` object.

# A `dictionary` instance offers the possibility to retrieve matching records according to a specific term, or to retrieve information about all available variables, using the `find()` method. For instance, looking for variables containing the term `COPD` is done this way: 

# In[12]:


dict_vars = resource.dictionary().find()


# Subsequently, objects created by the `dictionary.find` exposes the search result using 4 different methods: `.count()`, `.keys()`, `.entries()`, and `.DataFrame()`. 

# In[13]:


pprint({"Count": dict_vars.count(), 
        "Keys": dict_vars.keys()[0:5]})


# In[14]:


dict_df = dict_vars.DataFrame()


# In[15]:


dict_df = dict_df[['categorical', 'patientCount', 'observationCount']]


# In[16]:


dict_df.index = dict_df.index.str.replace(',', '_')


# In[22]:


dict_df.index[0].split('\\')[1]


# In[23]:


dict_df['StudyName'] = [ind.split('\\')[1] for ind in dict_df.index]


# In[38]:


StudyNames = sorted(dict_df['StudyName'].unique())


# In[39]:


VarCountsByStudy = [dict_df.loc[dict_df['StudyName'] == study].shape[0] for study in StudyNames]


# In[42]:


VarCountsByStudyDataFrame = pd.DataFrame({'Study Name' : StudyNames, 'Variable Count' : VarCountsByStudy})


# In[45]:


TotalVarCount = sum(VarCountsByStudy)


# In[46]:


TotalVarCount


# In[29]:


## Export all the variables from the BDCatalyst platform to a CSV file with headers


# In[30]:


dict_df.to_csv(r'BDCatalyst_AllVariables.csv', header=True)


# In[ ]:


VarCountsByStudyDataFrame.to_csv(r'BDCatalyst_VariablesCountsForEachStudy.csv', header=True)

