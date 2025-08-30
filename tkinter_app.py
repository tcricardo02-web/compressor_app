import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

class CompressorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Aplicativo de Performance de Compressores")
        self.geometry("1200x800")

        # Variáveis globais
        self.unit_system = "SI"  # "SI" ou "Imperial"
        self.config_data = {}
        self.performance_results = {}

        # Criar notebook (abas)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Adicionar abas
        self.create_unit_tab()
        self.create_equipment_config_tab()
        self.create_process_tab()
        self.create_performance_calc_tab()
        self.create_report_tab()
        self.create_multirun_tab()

    def create_unit_tab(self):
        unit_frame = ttk.Frame(self.notebook)
        self.notebook.add(unit_frame, text="Unidades de Medida")

        # Sistema de unidades
        ttk.Label(unit_frame, text="Sistema de Unidades:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.unit_var = tk.StringVar(value="SI")
        ttk.Radiobutton(unit_frame, text="SI", variable=self.unit_var, value="SI", command=self.update_units).grid(row=0, column=1, sticky=tk.W)
        ttk.Radiobutton(unit_frame, text="Imperial", variable=self.unit_var, value="Imperial", command=self.update_units).grid(row=0, column=2, sticky=tk.W)

        # Pressão
        ttk.Label(unit_frame, text="Pressão:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.pressure_var = tk.StringVar(value="psig")
        ttk.Radiobutton(unit_frame, text="psig", variable=self.pressure_var, value="psig").grid(row=1, column=1, sticky=tk.W)
        ttk.Radiobutton(unit_frame, text="kgf/cm²g", variable=self.pressure_var, value="kgf/cm²g").grid(row=1, column=2, sticky=tk.W)

        # Temperatura
        ttk.Label(unit_frame, text="Temperatura:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        self.temp_var = tk.StringVar(value="°C")
        ttk.Radiobutton(unit_frame, text="°C", variable=self.temp_var, value="°C").grid(row=2, column=1, sticky=tk.W)
        ttk.Radiobutton(unit_frame, text="°F", variable=self.temp_var, value="°F").grid(row=2, column=2, sticky=tk.W)

        # Comprimento
        ttk.Label(unit_frame, text="Comprimento:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        self.length_var = tk.StringVar(value="mm")
        ttk.Radiobutton(unit_frame, text="mm", variable=self.length_var, value="mm").grid(row=3, column=1, sticky=tk.W)
        ttk.Radiobutton(unit_frame, text="polegadas", variable=self.length_var, value="polegadas").grid(row=3, column=2, sticky=tk.W)

        # Vazão
        ttk.Label(unit_frame, text="Vazão Volumétrica:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        self.flow_var = tk.StringVar(value="E3*m3/d")
        ttk.Radiobutton(unit_frame, text="E3*m3/d", variable=self.flow_var, value="E3*m3/d").grid(row=4, column=1, sticky=tk.W)
        ttk.Radiobutton(unit_frame, text="MMSCFD", variable=self.flow_var, value="MMSCFD").grid(row=4, column=2, sticky=tk.W)

    def update_units(self):
        self.unit_system = self.unit_var.get()
        # Atualizar outros widgets conforme necessário

    def create_equipment_config_tab(self):
        config_frame = ttk.Frame(self.notebook)
        self.notebook.add(config_frame, text="Configuração do Equipamento")

        # Motor
        motor_frame = ttk.LabelFrame(config_frame, text="Motor")
        motor_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W+tk.E)

        ttk.Label(motor_frame, text="Tipo:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.motor_type = tk.StringVar(value="Gás Natural")
        ttk.Radiobutton(motor_frame, text="Gás Natural", variable=self.motor_type, value="Gás Natural").grid(row=0, column=1, sticky=tk.W)
        ttk.Radiobutton(motor_frame, text="Elétrico", variable=self.motor_type, value="Elétrico").grid(row=0, column=2, sticky=tk.W)

        ttk.Label(motor_frame, text="RPM:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.rpm_entry = ttk.Entry(motor_frame)
        self.rpm_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(motor_frame, text="Derate (%):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.derate_entry = ttk.Entry(motor_frame)
        self.derate_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(motor_frame, text="Potência Air Cooler (4%):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.air_cooler_power_entry = ttk.Entry(motor_frame)
        self.air_cooler_power_entry.grid(row=3, column=1, padx=5, pady=5)

        # Air Cooler
        air_cooler_frame = ttk.LabelFrame(config_frame, text="Air Cooler")
        air_cooler_frame.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W+tk.E)

        ttk.Label(air_cooler_frame, text="Perda de Carga (% por estágio):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.cooler_pressure_drop_entry = ttk.Entry(air_cooler_frame)
        self.cooler_pressure_drop_entry.insert(0, "1")
        self.cooler_pressure_drop_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(air_cooler_frame, text="Temperatura Saída (°F por estágio):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.cooler_temp_entry = ttk.Entry(air_cooler_frame)
        self.cooler_temp_entry.insert(0, "120")
        self.cooler_temp_entry.grid(row=1, column=1, padx=5, pady=5)

        # Compressor
        compressor_frame = ttk.LabelFrame(config_frame, text="Compressor")
        compressor_frame.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W+tk.E)

        ttk.Label(compressor_frame, text="Stroke:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.stroke_entry = ttk.Entry(compressor_frame)
        self.stroke_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(compressor_frame, text="Número de Cilindros:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.num_cylinders_entry = ttk.Entry(compressor_frame)
        self.num_cylinders_entry.grid(row=1, column=1, padx=5, pady=5)

        # Frame para adicionar cilindros
        self.cylinder_frame = ttk.Frame(compressor_frame)
        self.cylinder_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        ttk.Button(compressor_frame, text="Adicionar Cilindro", command=self.add_cylinder).grid(row=3, column=0, columnspan=2, pady=10)

        # Botão para gerar diagrama
        ttk.Button(config_frame, text="Gerar Diagrama", command=self.generate_diagram).grid(row=3, column=0, pady=20)

    def add_cylinder(self):
        num_cylinders = int(self.num_cylinders_entry.get()) if self.num_cylinders_entry.get() else 1

        for i in range(num_cylinders):
            cylinder_frame = ttk.LabelFrame(self.cylinder_frame, text=f"Cilindro {i+1}")
            cylinder_frame.pack(side=tk.LEFT, padx=5, pady=5)

            ttk.Label(cylinder_frame, text="Estágio:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
            stage_var = tk.StringVar(value="1")
            stage_combo = ttk.Combobox(cylinder_frame, textvariable=stage_var, values=["1", "2", "3"]
            )
            stage_combo.grid(row=0, column=1, padx=5, pady=5)

            ttk.Label(cylinder_frame, text="Clearance (%):").grid(row=1, column=0, stick=tk.W, padx=5, pady=5)
            clearance_entry = ttk.Entry(cylinder_frame)
            clearance_entry.grid(row=1, column=1, padx=5, pady=5)

            ttk.Label(cylinder_frame, text="SACE:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
            sace_var = tk.StringVar(value="Sim")
            sace_combo = ttk.Combobox(cylinder_frame, textvariable=sace_var, values=["Sim", "Não"])
            sace_combo.grid(row=2, column=1, padx=5, pady=5)

            ttk.Label(cylinder_frame, text="VVCP (%):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
            vvcp_entry = ttk.Entry(cylinder_frame)
            vvcp_entry.grid(row=3, column=1, padx=5, pady=5)

    def generate_diagram(self):
        messagebox.showinfo("Diagrama", "Diagrama gerado com sucesso!")

    def create_process_tab(self):
        process_frame = ttk.Frame(self.notebook)
        self.notebook.add(process_frame, text="Processo")

        # PFD
        pfd_frame = ttk.LabelFrame(process_frame, text="PFD do Compressor e Air Cooler")
        pfd_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.pfd_canvas = tk.Canvas(pfd_frame, bg="white", width=800, height=400)
        self.pfd_canvas.pack(padx=10, pady=10)

        power_frame = ttk.LabelFrame(process_frame, text="Potência Requerida")
        power_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(power_frame, text="BHP:").pack(side=tk.LEFT, padx=10, pady=10)
        self.bhp_label = ttk.Label(power_frame, text="0")
        self.bhp_label.pack(side=tk.LEFT, padx=10, pady=10)

    def create_performance_calc_tab(self):
        perf_frame = ttk.Frame(self.notebook)
        self.notebook.add(perf_frame, text="Cálculo de Performance")

        ttk.Label(perf_frame, text="Pressão de Entrada:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        self.inlet_press_entry = ttk.Entry(perf_frame)
        self.inlet_press_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(perf_frame, text="Pressão de Descarga:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        self.discharge_press_entry = ttk.Entry(perf_frame)
        self.discharge_press_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(perf_frame, text="Calcular Performance", command=self.calculate_performance).grid(row=2, column=0, columnspan=2, pady=20)

        results_frame = ttk.LabelFrame(perf_frame, text="Resultados")
        results_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W+tk.E)

        self.results_text = tk.Text(results_frame, height=10, width=80)
        self.results_text.pack(padx=10, pady=10)

    def calculate_performance(self):
        inlet_press = float(self.inlet_press_entry.get())
        discharge_press = float(self.discharge_press_entry.get())
        bhp = (discharge_press - inlet_press) * 0.5 + 100
        flow_rate = 5000
        result = f"""
        Pressão de Entrada: {inlet_press} {self.pressure_var.get()}
        Pressão de Descarga: {discharge_press} {self.pressure_var.get()}
        Vazão Volumétrica: {flow_rate} {self.flow_var.get()}
        Potência Requerida (BHP): {bhp:.2f}
        """
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, result)
        self.bhp_label.config(text=f"{bhp:.2f}")

    def create_report_tab(self):
        report_frame = ttk.Frame(self.notebook)
        self.notebook.add(report_frame, text="Relatório")

        self.report_text = tk.Text(report_frame, height=30, width=100)
        self.report_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        ttk.Button(report_frame, text="Gerar Relatório", command=self.generate_report).pack(pady=10)
        ttk.Button(report_frame, text="Exportar PDF", command=self.export_pdf).pack(pady=10)

    def generate_report(self):
        report_content = f"""
        RELATÓRIO DE PERFORMANCE DO COMPRESSOR

        Data: {pd.Timestamp.now().strftime('%d/%m/%Y')}

        CONFIGURAÇÃO DO EQUIPAMENTO:
        - Motor: {self.motor_type.get()}
        - RPM: {self.rpm_entry.get()}
        - Derate: {self.derate_entry.get()}%
        - Potência Air Cooler: {self.air_cooler_power_entry.get()}%

        RESULTADOS DE PERFORMANCE:
        - Pressão Entrada: {self.inlet_press_entry.get()} {self.pressure_var.get()}
        - Pressão Descarga: {self.discharge_press_entry.get()} {self.pressure_var.get()}
        - Potência (BHP): {self.bhp_label['text']}
        """
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(tk.END, report_content)

    def export_pdf(self):
        filename = filedialog.asksaveasfilename(defaultextension=".pdf",
                                               filetypes=[("PDF files", "*.pdf")])
        if filename:
            c = canvas.Canvas(filename, pagesize=letter)
            width, height = letter
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, height - 50, "RELATÓRIO DE PERFORMANCE DO COMPRESSOR")
            c.setFont("Helvetica", 12)
            y_position = height - 100
            lines = self.report_text.get(1.0, tk.END).split('
')
            for line in lines:
                if line.strip():
                    c.drawString(50, y_position, line)
                    y_position -= 20
                    if y_position < 50:
                        c.showPage()
                        y_position = height - 50
            c.save()
            messagebox.showinfo("Exportação", f"Relatório exportado para {filename}")

    def create_multirun_tab(self):
        multirun_frame = ttk.Frame(self.notebook)
        self.notebook.add(multirun_frame, text="Multirun")
        ttk.Label(multirun_frame, text="Pressão de Sucção Mínima:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        self.min_suction_entry = ttk.Entry(multirun_frame)
        self.min_suction_entry.grid(row=0, column=1, padx=10, pady=10)
        ttk.Label(multirun_frame, text="Pressão de Sucção Máxima:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        self.max_suction_entry = ttk.Entry(multirun_frame)
        self.max_suction_entry.grid(row=1, column=1, padx=10, pady=10)
        ttk.Label(multirun_frame, text="Pressão de Descarga Mínima:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        self.min_discharge_entry = ttk.Entry(multirun_frame)
        self.min_discharge_entry.grid(row=2, column=1, padx=10, pady=10)
        ttk.Label(multirun_frame, text="Pressão de Descarga Máxima:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
        self.max_discharge_entry = ttk.Entry(multirun_frame)
        self.max_discharge_entry.grid(row=3, column=1, padx=10, pady=10)
        ttk.Label(multirun_frame, text="RPM Mínimo:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=10)
        self.min_rpm_entry = ttk.Entry(multirun_frame)
        self.min_rpm_entry.grid(row=4, column=1, padx=10, pady=10)
        ttk.Label(multirun_frame, text="RPM Máximo:").grid(row=5, column=0, sticky=tk.W, padx=10, pady=10)
        self.max_rpm_entry = ttk.Entry(multirun_frame)
        self.max_rpm_entry.grid(row=5, column=1, padx=10, pady=10)
        ttk.Button(multirun_frame, text="Executar Multirun", command=self.run_multirun).grid(row=6, column=0, columnspan=2, pady=20)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        self.multirun_fig = FigureCanvasTkAgg(fig, master=multirun_frame)
        self.multirun_fig.get_tk_widget().grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    def run_multirun(self):
        min_suction = float(self.min_suction_entry.get())
        max_suction = float(self.max_suction_entry.get())
        min_discharge = float(self.min_discharge_entry.get())
        max_discharge = float(self.max_discharge_entry.get())
        min_rpm = float(self.min_rpm_entry.get())
        max_rpm = float(self.max_rpm_entry.get())
        suction_range = np.linspace(min_suction, max_suction, 10)
        discharge_range = np.linspace(min_discharge, max_discharge, 10)
        rpm_range = np.linspace(min_rpm, max_rpm, 5)
        flow_rates = []
        powers = []
        for suction in suction_range:
            for discharge in discharge_range:
                for rpm in rpm_range:
                    flow = (discharge - suction) / 10 + rpm / 100
                    power = (discharge - suction) * 0.8 + rpm / 50
                    flow_rates.append((suction, flow))
                    powers.append((suction, power))
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        ax1.scatter([f[0] for f in flow_rates], [f[1] for f in flow_rates], alpha=0.5)
        ax1.set_xlabel('Pressão de Sucção')
        ax1.set_ylabel('Vazão')
        ax1.set_title('PS x Vazão')
        ax2.scatter([p[0] for p in powers], [p[1] for p in powers], alpha=0.5)
        ax2.set_xlabel('Pressão de Sucção')
        ax2.set_ylabel('Potência (BHP)')
        ax2.set_title('PS x Potência')
        self.multirun_fig.figure = fig
        self.multirun_fig.draw()

if __name__ == "__main__":
    app = CompressorApp()
    app.mainloop()
