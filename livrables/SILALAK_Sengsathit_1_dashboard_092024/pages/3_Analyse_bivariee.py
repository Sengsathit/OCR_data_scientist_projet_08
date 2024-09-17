import streamlit as st
from utils.functions import display_banner, show_info_message, show_error_message
from utils.constants import *

# Affichage de l'en-tête de la page
display_banner(title='Analyse bi-variée')

try:
    data = st.session_state['data']
    show_info_message(message='OK')
except:
    show_error_message(message='Aucune information client à afficher. Vous devez d\'abord vérifier l\'éligibilité d\'un client.')
