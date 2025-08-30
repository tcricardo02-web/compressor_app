import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

# Configuração inicial da página
st.set_page_config(page_title="Aplicativo de Performance de Compressores", layout="wide")

# Funções auxiliares permanecem as mesmas...

def main():
    st.title("Aplicativo de Performance de Compressores")
    
    # Inicializar estado da sessão com valores padrão corretos
    if 'equipment_data' not in st.session_state:
        st.session_state.equipment_data = {
            'motor_type': 'Gás Natural',
            'rpm': 1500,
            'derate': 5.0,  # Garantir que seja float
            'air_cooler_power': 4.0,  # Garantir que seja float
            'cooler_pressure_drop': 1.0,
            'cooler_temp': 120.0,
            'stroke': 200.0,
            'num_cylinders': 4,
            'cylinders': [],
            'inlet_press': 100.0,
            'discharge_press': 500.0,
            'performance': None
        }
    
    # Restante do código permanece igual...
    
    with tabs[1]:  # Configuração do Equipamento
        st.header("Configuração do Equipamento")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Motor")
            motor_type = st.selectbox(
                "Tipo de Motor:",
                ["Gás Natural", "Elétrico"],
                key="motor_type"
            )
            
            # Converter para float se necessário
            try:
                rpm = float(st.session_state.equipment_data['rpm'])
            except (TypeError, ValueError):
                rpm = 1500.0
            rpm = st.number_input(
                "RPM:",
                min_value=500,
                max_value=3000,
                value=rpm,
                step=100,
                key="rpm"
            )
            
            # Converter para float se necessário
            try:
                derate = float(st.session_state.equipment_data['derate'])
            except (TypeError, ValueError):
                derate = 5.0
            derate = st.slider(
                "Derate (%):",
                min_value=0,
                max_value=20,
                value=derate,
                key="derate"
            )
            
            # Converter para float se necessário
            try:
                air_cooler_power = float(st.session_state.equipment_data['air_cooler_power'])
            except (TypeError, ValueError):
                air_cooler_power = 4.0
            air_cooler_power = st.number_input(
                "Potência Air Cooler (%):",
                min_value=1,
                max_value=10,
                value=air_cooler_power,
                step=0.5,
                key="air_cooler_power"
            )
        
        # Restante do código permanece igual...
