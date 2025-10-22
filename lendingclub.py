import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# 页面美化
st.set_page_config(
  page_tilte = "지능형신용평가모형",
   page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)
