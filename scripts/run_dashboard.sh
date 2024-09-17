#!/bin/bash

# Arrêt de l'instance du Dashboard
lsof -i tcp:8502 | awk '/8502/{print $2}' | xargs kill

# Lancer le dashboard en arrière-plan avec nohup
cd /home/ubuntu/OCR_data_scientist_projet_08
source .venv/bin/activate
cd livrables
nohup streamlit run SILALAK_Sengsathit_1_dashboard_092024.py --server.port 8502 > dashboard.out 2> dashboard.err < /dev/null &