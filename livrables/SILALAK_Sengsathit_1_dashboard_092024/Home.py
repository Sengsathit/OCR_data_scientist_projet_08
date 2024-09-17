import pandas as pd
import requests
import streamlit as st
from utils.functions import load_dataset, display_banner, display_gauge, show_error_message, show_info_message, show_feature_importances
from utils.constants import *

# Configuration de la page
st.set_page_config(layout='centered')

# Affichage de l'en-tête de la page
display_banner(title='Évaluation du risque de crédit')

# Chargement du dataset
load_dataset()

# Initialiser le state si ce n'est pas déjà fait
if 'data' not in st.session_state:
    st.session_state['data'] = None

# Champ de saisie pour le numéro de client
client_id = st.text_input(
    "Saisir le numéro de client (ex : 100002, 100040)", 
    st.session_state['data'].get('sk_id_curr') if st.session_state.get('data') else ""
)

# Bouton pour soumettre le numéro de client
if st.button("Vérifier le risque"):
    st.session_state['data'] = None
    if client_id:
        # Valeur de l'ID à envoyer à l'API
        payload = {"sk_id_curr": int(client_id)}
        try:
            # Appel vers l'API + récupération de la réponse
            response = requests.post(api_url, json=payload)

            if response.status_code == 200:
                # Récupérer les données JSON
                response_data = response.json()

                # Sauvegarder les données dans session_state
                st.session_state['data'] = response_data

            elif response.status_code == 400:
                response_data = response.json()
                st.error(f"Erreur : {response_data['error']}")
            else:
                st.error(f"Erreur : {response}")

        except Exception as e:
            st.error(f"Erreur lors de l'appel API : {e}")
    else:
        st.warning("Veuillez saisir un numéro de client.")

# Affichage de l'interface en fonction des données récupérées
def display_home_page_content(data):
    if data:
        threshold = round(data['threshold'] * 100, 2)
        probability = round(data['probability'] * 100, 2)

        # Vérifier le dépassement du seuil de probabilité
        is_credit_default = probability > threshold

        # Affichage du score du client
        display_gauge(value=probability, range_limit=threshold)

        if is_credit_default:
            show_error_message(message='Client à risque')
        else:
            show_info_message(message='Client éligible pour un crédit')

        # Explication des features
        show_feature_importances(df=data)

# Appeler la fonction d'affichage si des données sont présentes
if st.session_state['data']:
    display_home_page_content(st.session_state['data'])