import streamlit as st
from utils.functions import *
from utils.constants import *

# FUNCTIONS -----------------------------------------------------------------------------------------------------------------------------

# END_FUNCTIONS -------------------------------------------------------------------------------------------------------------------------

# Affichage de l'en-tête de la page
display_banner(title='Analyse bi-variée')

numerical_features = get_numerical_features()

# Diviser l'interface en deux colonnes
col1, col2 = st.columns(2)

# Ajouter un selectbox dans la première colonne
with col1:
    feature_1 = st.selectbox(
        'Choisir la première caractéristique :',
        numerical_features
    )

# Ajouter un selectbox dans la deuxième colonne
with col2:
    feature_2 = st.selectbox(
        'Choisir la seconde caractéristique :',
        numerical_features
    )

plot_scatter_features(feature_name_1=feature_1, feature_name_2=feature_2)

feature_1_description = get_column_description(feature_1)
feature_2_description = get_column_description(feature_2)

st.header('Description des caractéristiques')

st.write(f"{feature_1} = {feature_1_description}")
st.write(f"{feature_2} = {feature_2_description}")