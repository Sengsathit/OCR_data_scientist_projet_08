import streamlit as st
from utils.functions import *
from utils.constants import *

# Affichage de l'en-tête de la page
display_banner(title='Analyse comparative')

# Chargement des données du client
state_data = get_state_data()

# Afficher les données comparatives du client si elles existent
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

        # Tracer l'histogramme
        plot_hist_feature(client_id=client_id, feature_name=selected_feature)

        # Récupérer puis afficher les descriptions des caractéristiques sélectionnées
        st.header('Description des caractéristiques')
        try:
            feature_description = get_column_description(selected_feature)
            st.write(f"{selected_feature} = {feature_description}")
        except:
            show_error_message(message=message_no_data_error)


else:

    show_error_message(message=message_no_data)