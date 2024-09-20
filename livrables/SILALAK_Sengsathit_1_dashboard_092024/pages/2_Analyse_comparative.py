import streamlit as st
from utils.functions import *
from utils.constants import *

# Affichage de l'en-tête de la page
display_banner(title='Analyse comparative')

state_data = get_state_data()

if state_data:
    
    client_id = state_data['sk_id_curr']

    # Options à afficher et leurs colonnes correspondantes dans le DataFrame
    options = [
        ('Age (DAYS_BIRTH)', 'DAYS_BIRTH'),
        ('Expérience professionnelle (DAYS_EMPLOYED)', 'DAYS_EMPLOYED'),
        ('Revenus (AMT_INCOME_TOTAL)', 'AMT_INCOME_TOTAL'),
        ('Montant du crédit en cours (AMT_CREDIT)', 'AMT_CREDIT')
    ]

    # Création du selectbox avec les noms d'options
    selected_option = st.selectbox(
        f"Comparaison des caractéristiques du client n° {client_id} par rapport à l'ensemble des clients",
        [opt[0] for opt in options],
        placeholder="Selectionnez une caractéristique..."
    )

    if selected_option:
        # Récupération de la colonne correspondante
        selected_feature = next(opt[1] for opt in options if opt[0] == selected_option)

        # Chargement du dataset
        df = get_dataset()

        # Récupération des valeurs
        client_value = df.loc[df['SK_ID_CURR'] == client_id, selected_feature].iloc[0]
        feature_values = df[selected_feature]

        # Inverser les valeurs pour 'DAYS_EMPLOYED' si nécessaire
        if selected_feature == 'DAYS_EMPLOYED':
            client_value *= -1
            feature_values = feature_values * -1

        # Appel de la fonction pour tracer l'histogramme
        plot_hist_feature(feature_name=selected_feature, values=feature_values, client_value=client_value)
        

else:

    show_error_message(message=message_no_data)