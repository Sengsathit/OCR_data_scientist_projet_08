import streamlit as st
from utils.functions import *
from utils.constants import *

# FUNCTIONS -----------------------------------------------------------------------------------------------------------------------------

# END_FUNCTIONS -------------------------------------------------------------------------------------------------------------------------

# Affichage de l'en-tête de la page
display_banner(title='Analyse bi-variée')

data_state = get_state_data()

if data_state:
    show_info_message(message='OK')
else:
    show_error_message(message=message_no_data)
