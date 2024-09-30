import streamlit as st
import pandas as pd
from utils.functions import *
from utils.constants import *

# Fonction pour afficher une ligne d'information à propos du client
def display_info_line(feature, value, additional_string=""):
    st.markdown(f"""
        <p style='font-size:24px; display:inline;'>{feature} : </p>
        <p style='font-size:16px; display:inline;'>{value} {additional_string}</p>
    """, unsafe_allow_html=True)

# Fonction pour afficher l'ensemble du contenu de la page informations client
def display_client_info_content(data):
    df = get_dataset_train()

    client = df.query(f"SK_ID_CURR == {data['sk_id_curr']}")

    client_id = client['SK_ID_CURR'].values[0]
    display_info_line(feature='Numéro client', value=client_id)

    age = abs(round(client['DAYS_BIRTH'].values[0] / 365))
    display_info_line(feature='Age', value=age, additional_string='ans')

    isWoman = client['CODE_GENDER_F'].values[0]
    display_info_line(feature='Sexe', value="Femme" if isWoman else "Homme")

    days_employed = client['DAYS_EMPLOYED'].values[0]
    work_experience = abs(round(days_employed / 365)) if pd.notna(days_employed) else 'NC'
    additional_string = 'année(s)' if pd.notna(days_employed) else ""
    display_info_line(feature='Expérience professionnelle', value=work_experience, additional_string=additional_string)

    amt_income_total = client['AMT_INCOME_TOTAL'].values[0]
    if pd.notna(amt_income_total):
        income = f"{amt_income_total:,.0f}".replace(',', ' ')
    else:
        income = 'NC'
    additional_string = '$' if pd.notna(amt_income_total) else None
    display_info_line(feature='Revenu annuel', value=income, additional_string=additional_string)

    amt_credit = client['AMT_CREDIT'].values[0]
    if pd.notna(amt_credit):
        credit = f"{amt_credit:,.0f}".replace(',', ' ')
    else:
        credit = 'NC'
    additional_string = '$' if pd.notna(amt_credit) else None
    display_info_line(feature='Crédit en cours', value=credit, additional_string=additional_string)



# Affichage de l'en-tête de la page
display_banner(title='Informations client')

# Chargement des données du client
state_data = get_state_data()

# Afficher les informations du client si elles existent
if state_data:
    display_client_info_content(data=state_data)
else:
    show_error_message(message=message_no_data)

