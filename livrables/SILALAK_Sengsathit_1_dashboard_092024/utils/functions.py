import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
from .constants import *
import pandas as pd
import numpy as np
import seaborn as sns

# Fonction pour récupérer le state data
def get_state_data():
    # Initialiser le state s'il n'est pas encoré initialé
    if 'client_data' not in st.session_state:
        st.session_state['client_data'] = None
    return st.session_state['client_data']

# Fonction pour récupérer le dataset
@st.cache_data
def get_dataset():
    df = pd.read_csv(df_path)
    return df

# Fonction pour afficher la bannière
def display_banner(title):
    st.image(image_url, use_column_width=True)
    st.markdown(
        f"<h1 style='text-align: center; font-size: 48px; margin-bottom: 40px;'>{title}</h1>", 
        unsafe_allow_html=True
    )

# Fonction pour créer une jauge selon le score du client et le seuil de décision du modèle
def display_gauge(client_id, value, range_limit):
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={ 'valueformat': '.2f' },
        title={'text': f"Score du client n° {client_id} pour un seuil à {range_limit}", 'font': {'size': 24}},
        gauge={
            'axis': {'range': [0, 100]},
            'steps': [
                {'range': [0, range_limit], 'color': green_color},
                {'range': [range_limit, 100], 'color': red_color}
            ],
            'bar': {'color': 'white', 'thickness': 0.2}
        }
    ))

    st.plotly_chart(fig)

# Fonction pour créer un graphique de barres horizontales avec Plotly
def plot_feature_importance(df, title, color):
    fig = px.bar(df, 
                y='feature_name', 
                x='shap_value', 
                orientation='h', 
                title=title, 
                labels={'shap_value': 'SHAP Value', 'feature_name': ''},
                color_discrete_sequence=[color])
    return fig

# Fonction pour afficher un message d'information
def show_info_message(message):
    st.markdown(
        f"""
        <div style="background-color:#d4edda;padding:10px;border-radius:5px;">
        <strong style="color:#155724;">{message}</strong>
        </div>
        """, unsafe_allow_html=True
    )

# Fonction pour afficher un message d'erreur
def show_error_message(message):
    st.markdown(
        f"""
        <div style="background-color:#ffcccb;padding:10px;border-radius:5px;">
        <strong style="color:#b30000;">{message.replace('\n', '<br>')}</strong>
        </div>
        """, unsafe_allow_html=True
    )

# Fonction pour afficher les feature importances
def show_feature_importances(df):
    # Trier les valeurs négatives du plus petit au plus grand
    sorted_negatives = sorted(df['feature_importances_negative'], key=lambda x: x['shap_value'])[:10]

    # Trier les valeurs positives du plus grand au plus petit
    sorted_positives = sorted(df['feature_importances_positive'], key=lambda x: x['shap_value'], reverse=True)[:10]

    # Affichage de la contribution des features
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader('Contribution des features')

    st.text('')

    # Convertir les données en DataFrames
    df_sorted_negatives = pd.DataFrame(sorted_negatives).sort_values(by='shap_value', ascending=False)
    df_sorted_positives = pd.DataFrame(sorted_positives).sort_values(by='shap_value', ascending=True)

    # Créer les graphiques pour les importances positives et négatives
    fig_neg = plot_feature_importance(df_sorted_negatives, 'Contributions négatives', 'gray')
    fig_pos = plot_feature_importance(df_sorted_positives, 'Contributions positives', 'orange')

    # Afficher les graphiques avec Streamlit
    st.plotly_chart(fig_neg)
    st.plotly_chart(fig_pos)

# Fonction pour afficher une distribution en fonction d'une feature sélectionnée
def plot_hist_feature(feature_name, values, client_value):
    fig, ax = plt.subplots()
    sns.histplot(values, bins=30, kde=False, ax=ax, edgecolor='white')
    ax.axvline(x=client_value, color='red', linestyle='--', linewidth=1, label=f"valeur du client : {client_value}")
    ax.legend()
    plt.title(f"Distribution pour la caractéristique {feature_name}")
    plt.ylabel('Effectif')
    st.pyplot(fig)