import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title("Aplicativo de Performance de Compressores")

st.sidebar.header("Sistema de Unidades")
unit = st.sidebar.selectbox("Sistema de Unidades", ["SI","Imperial"])
pressure_unit = st.sidebar.selectbox("Pressão", ["psig","kgf/cm²g"])
flow_unit = st.sidebar.selectbox("Vazão Volumétrica", ["E3*m3/d","MMSCFD"])

st.sidebar.header("Motor")
motor_type = st.sidebar.radio("Tipo", ["Gás Natural","Elétrico"])
rpm = st.sidebar.number_input("RPM", value=3600)
derate = st.sidebar.number_input("Derate (%)", value=0.0)
air_cooler_power = st.sidebar.number_input("Potência Air Cooler (4%)", value=0.0)

st.sidebar.header("Pressões")
inlet_press = st.sidebar.number_input("Pressão de Entrada", value=0.0)
discharge_press = st.sidebar.number_input("Pressão de Descarga", value=0.0)

if st.sidebar.button("Calcular Performance"):
    bhp = (discharge_press - inlet_press)*0.5 + 100
    flow_rate = 5000
    st.subheader("Resultados")
    st.write(f"Pressão de Entrada: {inlet_press} {pressure_unit}")
    st.write(f"Pressão de Descarga: {discharge_press} {pressure_unit}")
    st.write(f"Vazão Volumétrica: {flow_rate} {flow_unit}")
    st.write(f"Potência Requerida (BHP): {bhp:.2f}")

st.sidebar.header("Multirun")
min_suction = st.sidebar.number_input("Pressão de Sucção Mín.", value=0.0)
max_suction = st.sidebar.number_input("Pressão de Sucção Máx.", value=10.0)
min_discharge = st.sidebar.number_input("Pressão de Descarga Mín.", value=0.0)
max_discharge = st.sidebar.number_input("Pressão de Descarga Máx.", value=10.0)
min_rpm = st.sidebar.number_input("RPM Mín.", value=1000)
max_rpm = st.sidebar.number_input("RPM Máx.", value=5000)

if st.sidebar.button("Executar Multirun"):
    suction_range = np.linspace(min_suction, max_suction, 10)
    discharge_range = np.linspace(min_discharge, max_discharge, 10)
    rpm_range = np.linspace(min_rpm, max_rpm, 5)
    flow_rates = []
    powers = []
    for s in suction_range:
        for d in discharge_range:
            for r in rpm_range:
                flow = (d - s)/10 + r/100
                power = (d - s)*0.8 + r/50
                flow_rates.append((s, flow))
                powers.append((s, power))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,5))
    ax1.scatter([f[0] for f in flow_rates],[f[1] for f in flow_rates], alpha=0.5)
    ax1.set_xlabel('Pressão de Sucção')
    ax1.set_ylabel('Vazão')
    ax1.set_title('PS x Vazão')
    ax2.scatter([p[0] for p in powers],[p[1] for p in powers], alpha=0.5)
    ax2.set_xlabel('Pressão de Sucção')
    ax2.set_ylabel('Potência (BHP)')
    ax2.set_title('PS x Potência')
    st.pyplot(fig)
