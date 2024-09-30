import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from utils.constants import *



# Fonction pour récupérer le state data
def get_state_data():
    # Initialiser le state s'il n'est pas encoré initialé
    if 'client_data' not in st.session_state:
        st.session_state['client_data'] = None
    return st.session_state['client_data']



# Fonction pour récupérer le dataset d'entraînement
@st.cache_data
def get_dataset_train():
    df = pd.read_csv(df_train_path)

    # Liste des caractéristiques à convertir en valeurs positives
    features_to_convert = ['DAYS_EMPLOYED', 'DAYS_REGISTRATION', 'DAYS_LAST_PHONE_CHANGE', 'DAYS_EMPLOYED_PERCENT']
    
    # Appliquer la conversion aux colonnes sélectionnées
    for feature in features_to_convert:
        if feature in df.columns:
            df[feature] = df[feature].abs()

    return df



# Fonction pour récupérer le dataset des noms de colonnes
@st.cache_data
def get_dataset_columns_description():
    df = pd.read_csv(df_columns_description_path)
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
        <strong style="color:#b30000;">{message.replace('html_br', '<br>')}</strong>
        </div>
        """, unsafe_allow_html=True
    )



# Fonction pour afficher les feature importances
def show_feature_importances(df):
    # Trier les valeurs du plus grand au plus petit
    sorted_global = sorted(df['feature_importances_global'], key=lambda x: x['shap_value'], reverse=True)[:10]

    # Trier les valeurs négatives du plus petit au plus grand
    sorted_negatives = sorted(df['feature_importances_negative'], key=lambda x: x['shap_value'])[:10]

    # Trier les valeurs positives du plus grand au plus petit
    sorted_positives = sorted(df['feature_importances_positive'], key=lambda x: x['shap_value'], reverse=True)[:10]

    # Affichage de la contribution globale des features
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader('Contribution globale des features')
    st.text('')
    df_sorted_global= pd.DataFrame(sorted_global).sort_values(by='shap_value', ascending=True)
    fig_global = plot_feature_importance(df_sorted_global, '', 'blue')
    st.plotly_chart(fig_global)

    # Affichage de la contribution locale des features
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader('Contribution locale des features')
    st.text('')
    df_sorted_negatives = pd.DataFrame(sorted_negatives).sort_values(by='shap_value', ascending=False)
    df_sorted_positives = pd.DataFrame(sorted_positives).sort_values(by='shap_value', ascending=True)
    fig_neg = plot_feature_importance(df_sorted_negatives, 'Contributions négatives', 'gray')
    fig_pos = plot_feature_importance(df_sorted_positives, 'Contributions positives', 'orange')
    st.plotly_chart(fig_neg)
    st.plotly_chart(fig_pos)



# Fonction pour afficher une distribution en fonction d'une feature sélectionnée
def plot_hist_feature(client_id, feature_name):
    # Chargement du dataset
    df = get_dataset_train()

    # Récupération des valeurs
    client_value = df.loc[df['SK_ID_CURR'] == client_id, feature_name].iloc[0]
    feature_values = df[feature_name]

    fig, ax = plt.subplots()
    sns.histplot(feature_values, bins=30, kde=False, ax=ax, edgecolor='white')
    ax.axvline(x=client_value, color='red', linestyle='--', linewidth=1, label=f"valeur du client : {client_value}")
    ax.legend()
    plt.title(f"Distribution pour la caractéristique {feature_name}")
    plt.ylabel('Effectif')
    st.pyplot(fig)



# Fonction pour afficher la dispersion des caractéristiques sélectionnées
def plot_scatter_features(feature_name_1, feature_name_2):
    # Chargement du dataset
    df = get_dataset_train()

    fig, ax = plt.subplots()
    sns.scatterplot(df, x=feature_name_1, y=feature_name_2)
    plt.title(f"Relation entre {feature_name_1} et {feature_name_2}")
    st.pyplot(fig)



# Fonction pour récupérer les noms des features numériques
def get_numerical_features():
    df = get_dataset_train()
    columns = df.select_dtypes(include=['float']).columns
    return columns



# Fonction pour récupérer la description d'une feature
def get_column_description(feature_name):
    df = get_dataset_columns_description()
    description = df.query(f"Row == '{feature_name}'")['Description'].values[0]
    return description