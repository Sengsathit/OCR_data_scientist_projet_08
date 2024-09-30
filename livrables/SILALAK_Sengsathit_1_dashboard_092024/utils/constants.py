import streamlit as st

# Chemins vers les datasets
df_train_path = './datasets/df_train_domain.csv'
df_columns_description_path = './datasets/df_columns_description.csv'

# Url de l'API de scoring
api_url = 'http://13.38.185.52:5000/scoring'

# Header de la page
image_url = "https://raw.githubusercontent.com/Sengsathit/OCR_data_scientist_assets/main/header_pret_a_depenser.png"

# Couleurs
green_color = 'mediumseagreen'
red_color = 'salmon'

# Messages
message_no_data = 'Aucune information client à afficher.html_brVous devez d\'abord vérifier l\'éligibilité d\'un client depuis la page d\'accueil.'
message_no_data_error = 'Aucune donnée à afficher.'