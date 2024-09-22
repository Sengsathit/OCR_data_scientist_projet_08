import sys
import os
import pandas as pd
import pytest
import pandas as pd
from unittest import mock
import streamlit as st

# Ajouter le chemin vers le dossier utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from functions import * # type: ignore

# Simuler les paths de constantes pour les tests
df_train_path = 'mock_train.csv'
df_columns_description_path = 'mock_columns.csv'

# Mock pour `st.session_state`
@pytest.fixture
def mock_session_state(mocker):
    mocker.patch('streamlit.session_state', {})

# Test de la fonction get_state_data
def test_get_state_data(mock_session_state):
    assert get_state_data() is None  # type: ignore
    st.session_state['client_data'] = 'some_data'
    assert get_state_data() == 'some_data'  # type: ignore

# Test de la fonction get_column_description
@mock.patch('pandas.read_csv')
def test_get_column_description(mock_read_csv):    
    # Simuler un DataFrame
    mock_df = pd.DataFrame({'Row': ['feature1'], 'Description': ['Description of feature1']})
    mock_read_csv.return_value = mock_df
    description = get_column_description('feature1')  # type: ignore
    assert description == 'Description of feature1'

# Test de la fonction show_info_message
def test_show_info_message(mocker):
    # Mock st.markdown
    mocker.patch('streamlit.markdown')
    # Simuler un message d'info
    message = "This is a test info message."
    show_info_message(message) # type: ignore
    st.markdown.assert_called_once_with(
        f"""
        <div style="background-color:#d4edda;padding:10px;border-radius:5px;">
        <strong style="color:#155724;">{message}</strong>
        </div>
        """, unsafe_allow_html=True
    )

# Test de la fonction show_error_message
def test_show_error_message(mocker):
    # Mock st.markdown
    mocker.patch('streamlit.markdown')
    # Simuler un message d'erreur
    message = "This is a test error message."
    show_error_message(message)  # type: ignore
    st.markdown.assert_called_once_with(
        f"""
        <div style="background-color:#ffcccb;padding:10px;border-radius:5px;">
        <strong style="color:#b30000;">{message.replace('html_br', '<br>')}</strong>
        </div>
        """, unsafe_allow_html=True
    )