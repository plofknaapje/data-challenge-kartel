# -*- coding: utf-8 -*-
"""
Created on Wed May 30 16:23:48 2018

@author: 20166843
"""

import conversations as cnv
import access
from textblob import TextBlob
import re
import pickle
from datetime import datetime, timedelta
import seaborn as sns; sns.set()
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import numpy as np

df = pd.read_csv('sentiment_airlines.csv')