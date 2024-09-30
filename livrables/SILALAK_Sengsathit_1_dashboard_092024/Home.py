import pandas as pd
import requests
import streamlit as st
from utils.functions import *
from utils.constants import *

# Fonction pour l'affichage de l'interface en fonction des données récupérées
def display_home_page_content(data):
    if data:
        client_id = data['sk_id_curr']
        threshold = round(data['threshold'] * 100, 2)
        probability = round(data['probability'] * 100, 2)

        # Vérifier le dépassement du seuil de probabilité
        is_credit_default = probability > threshold

        # Affichage du score du client
        display_gauge(client_id=client_id, value=probability, range_limit=threshold)

        if is_credit_default:
            show_error_message(message='Client à risque')
        else:
            show_info_message(message='Client éligible pour un crédit')

        # Explication des features
        show_feature_importances(df=data)


# Configuration de la page
st.set_page_config(layout='centered')

# Affichage de l'en-tête de la page
display_banner(title='Évaluation du risque de crédit')

# Chargement des données du client
state_data = get_state_data()

# Champ de saisie pour le numéro de client
client_id = st.text_input(
    "Saisir le numéro de client (ex : 100002, 100040)", 
    state_data['sk_id_curr'] if state_data else ""
)

# Bouton pour soumettre le numéro de client
if st.button("Vérifier le risque"):
    st.session_state['client_data'] = None
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
                st.session_state['client_data'] = response_data
                state_data = st.session_state['client_data']

            elif response.status_code == 400:
                response_data = response.json()
                st.error(f"Erreur : {response_data['error']}")
            else:
                st.error(f"Erreur : {response}")

        except Exception as e:
            st.error(f"Erreur lors de l'appel API : {e}")
    else:
        st.warning("Veuillez saisir un numéro de client.")

# Appeler la fonction d'affichage si des données de client existent
if state_data:
    display_home_page_content(data=state_data)