import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import struct
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SubaruECULogAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Subaru WRX STI ECU Log Analyzer")
        
        self.frame = tk.Frame(root)
        self.frame.pack(padx=20, pady=20)
        
        self.upload_csv_btn = tk.Button(self.frame, text="Upload ECU Log (CSV)", command=self.load_csv)
        self.upload_csv_btn.grid(row=0, column=0, padx=10, pady=5)
        
        self.upload_rom_btn = tk.Button(self.frame, text="Upload ROM File (BIN)", command=self.load_rom)
        self.upload_rom_btn.grid(row=1, column=0, padx=10, pady=5)
        
        self.upload_def_btn = tk.Button(self.frame, text="Upload ROM Definition (XML)", command=self.load_xml)
        self.upload_def_btn.grid(row=2, column=0, padx=10, pady=5)
        
        self.analyze_btn = tk.Button(self.frame, text="Analyze Data", command=self.analyze, state=tk.DISABLED)
        self.analyze_btn.grid(row=3, column=0, padx=10, pady=10)
        
        self.log_text = tk.Text(root, height=10, width=80)
        self.log_text.pack(pady=10)
        
        self.plot_frame = tk.Frame(root)
        self.plot_frame.pack()
        
        self.csv_file = None
        self.rom_file = None
        self.xml_file = None
        self.rom_data = {}
        self.xml_data = {}

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.csv_file = pd.read_csv(file_path)
            self.log(f"Loaded CSV file: {file_path}")
            self.log(f"CSV Columns: {', '.join(self.csv_file.columns)}")
            messagebox.showinfo("Success", "ECU Log file loaded successfully!")
            self.check_ready()

    def load_rom(self):
        file_path = filedialog.askopenfilename(filetypes=[("Binary Files", "*.bin")])
        if file_path:
            with open(file_path, 'rb') as f:
                self.rom_file = f.read()
            self.log(f"Loaded ROM file: {file_path}")
            messagebox.showinfo("Success", "ROM file loaded successfully!")
            self.check_ready()

    def load_xml(self):
        file_path = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml")])
        if file_path:
            tree = ET.parse(file_path)
            root = tree.getroot()
            for table in root.findall(".//table"):
                name = table.get("name")
                address = table.get("address")
                if name and address:
                    self.xml_data[name] = int(address, 16)
            self.log(f"Loaded XML definition file: {file_path}")
            self.log(f"Extracted Parameters: {', '.join(self.xml_data.keys())}")
            messagebox.showinfo("Success", "ROM Definition file loaded successfully!")
            self.check_ready()

    def check_ready(self):
        if self.csv_file is not None and self.rom_file is not None and self.xml_data:
            self.analyze_btn.config(state=tk.NORMAL)

    def analyze(self):
        if self.csv_file is None or self.rom_file is None or not self.xml_data:
            messagebox.showerror("Error", "Please load all required files before analyzing!")
            return
        
        max_boost = self.csv_file.get('Manifold Absolute Pressure (psi)', pd.Series([0])).max()
        max_knock_feedback = self.csv_file.get('Feedback Knock Correction (1-byte)** (degrees)', pd.Series([0])).max()
        max_knock_learning = self.csv_file.get('Fine Learning Knock Correction (degrees)', pd.Series([0])).max()
        max_injector_duty = self.csv_file.get('Injector Duty Cycle (%)', pd.Series([0])).max()

        self.log(f"Max Boost: {max_boost} psi")
        self.log(f"Max Feedback Knock: {max_knock_feedback} degrees")
        self.log(f"Max Fine Learning Knock: {max_knock_learning} degrees")
        self.log(f"Max Injector Duty Cycle: {max_injector_duty} %")

        self.plot_data()

    def plot_data(self):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        
        fig, axs = plt.subplots(2, 1, figsize=(8, 6))
        
        if 'Engine Speed (rpm)' in self.csv_file.columns and 'Manifold Absolute Pressure (psi)' in self.csv_file.columns:
            axs[0].plot(self.csv_file['Engine Speed (rpm)'], self.csv_file['Manifold Absolute Pressure (psi)'], label='Boost Pressure', color='blue')
            axs[0].set_xlabel('RPM')
            axs[0].set_ylabel('Boost (psi)')
            axs[0].set_title('Boost Pressure vs RPM')
            axs[0].legend()
            axs[0].grid(True)
        
        if 'Engine Speed (rpm)' in self.csv_file.columns and 'Feedback Knock Correction (1-byte)** (degrees)' in self.csv_file.columns:
            axs[1].plot(self.csv_file['Engine Speed (rpm)'], self.csv_file['Feedback Knock Correction (1-byte)** (degrees)'], label='Knock Correction', color='red')
            axs[1].set_xlabel('RPM')
            axs[1].set_ylabel('Knock Correction (degrees)')
            axs[1].set_title('Knock Correction vs RPM')
            axs[1].legend()
            axs[1].grid(True)
        
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = SubaruECULogAnalyzer(root)
    root.mainloop()
