#import 
import numpy as np
import csv
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk

class PieChartApp:
    def __init__(self, root, file_path, category_column, parameter_column, parameter_value):
        self.root = root
        self.file_path = file_path
        self.category_column = category_column
        self.parameter_column = parameter_column
        self.parameter_value = parameter_value

        # Window
        self.root.geometry("1200x600")

        # Load csv
        self.df = pd.read_csv(self.file_path, encoding='latin1')

        # Is there anything?
        if self.category_column not in self.df.columns:
            raise KeyError(f"Kategorie '{self.category_column}' nicht gefunden.")
        if self.parameter_column not in self.df.columns:
            raise KeyError(f"Parameter '{self.parameter_column}' nicht gefunden.")
        if self.parameter_value not in self.df[self.parameter_column].unique():
            raise ValueError(f"Wert '{self.parameter_value}' nicht in '{self.parameter_column}'.")

        # Filter
        self.filtered_df = self.df[self.df[self.parameter_column] == self.parameter_value]

        # Count
        self.category_counts = self.filtered_df[self.category_column].value_counts()

        # UI
        self.root.title("CheckData")

        # Dropdown button
        self.dropdown_frame = tk.Frame(root)
        self.dropdown_frame.pack(pady=5)
        self.dropdown_label = tk.Label(self.dropdown_frame, text="Kategorie auswählen:")
        self.dropdown_label.grid(row=0, column=0, padx=5)
        self.category_dropdown = ttk.Combobox(self.dropdown_frame, values=self.category_counts.index.tolist(), state="readonly")
        self.category_dropdown.grid(row=0, column=1, padx=5)
        self.category_dropdown.bind("<<ComboboxSelected>>", self.update_chart)
        if len(self.category_counts) > 0:
            self.category_dropdown.set(self.category_counts.index[0])

        # Dropdown parameter
        self.parameter_label = tk.Label(self.dropdown_frame, text="Parameter auswählen:")
        self.parameter_label.grid(row=0, column=2, padx=5)
        self.parameter_dropdown = ttk.Combobox(self.dropdown_frame, values=self.df[self.parameter_column].unique().tolist(), state="readonly")
        self.parameter_dropdown.grid(row=0, column=3, padx=5)
        self.parameter_dropdown.bind("<<ComboboxSelected>>", self.update_parameter)
        self.parameter_dropdown.set(self.parameter_value)

        # Escape button
        self.escape_button = tk.Button(root, text="Ansicht zurücksetzen", command=self.reset_chart)
        self.escape_button.pack(pady=10)

        # Diagramm
        self.figure, self.ax = plt.subplots(1, 2, figsize=(16, 8))
        self.canvas = FigureCanvasTkAgg(self.figure, root)
        self.chart_widget = self.canvas.get_tk_widget()
        self.chart_widget.pack()

        self.draw_pie_chart(self.category_counts, 0)

    def draw_pie_chart(self, data, index):
        def absolute_value(val):
            total = sum(data)
            absolute = int(round(val * total / 100))
            return f'{absolute}'

        self.ax[index].clear()
        self.ax[index].pie(
            data.values,
            labels=data.index,
            autopct=absolute_value,
            startangle=90,
            colors=plt.cm.Paired.colors)
        
        title = "Kategorien" if index == 0 else "Parameter-Werte"
        self.ax[index].set_title(f"Kreisdiagramm {title}")
        self.ax[index].axis('equal')
        self.canvas.draw()

    # Filter selection
    def update_chart(self, event):
        selected_category = self.category_dropdown.get()

        filtered_data = self.filtered_df[self.filtered_df[self.category_column] == selected_category]
        category_values = filtered_data[self.category_column].value_counts()

        self.draw_pie_chart(category_values, 0)

    # Filter selection 2
    def update_parameter(self, event):
        self.parameter_value = self.parameter_dropdown.get()

        self.filtered_df = self.df[self.df[self.parameter_column] == self.parameter_value]

        selected_category = self.category_dropdown.get()
        if selected_category in self.filtered_df[self.category_column].values:
            filtered_data = self.filtered_df[self.filtered_df[self.category_column] == selected_category]
            parameter_values = filtered_data[self.parameter_column].value_counts()
            self.draw_pie_chart(parameter_values, 1)
        else:
            self.ax[1].clear()
            self.ax[1].set_title("Keine Daten verfügbar")
            self.canvas.draw()

        #self.category_counts = self.filtered_df[self.category_column].value_counts()
        #self.category_dropdown['values'] = self.category_counts.index.tolist()
        #if len(self.category_counts) > 0:
        #    self.category_dropdown.set(self.category_counts.index[0])
        #    self.update_chart(None)

    def reset_chart(self):
        self.filtered_df = self.df[self.df[self.parameter_column] == self.parameter_value]
        self.category_counts = self.filtered_df[self.category_column].value_counts()
        self.category_dropdown['values'] = self.category_counts.index.tolist()
        if len(self.category_counts) > 0:
            self.category_dropdown.set(self.category_counts.index[0])
        self.draw_pie_chart(self.category_counts, 0)
        self.ax[1].clear()
        self.ax[1].set_title("Parameter Werte")
        self.canvas.draw()

if __name__ == "__main__":
    file_path = r'C:\Users\mario\Desktop\active_view_export.csv'
    category_column = 'Category'
    parameter_column = 'Parameter Name'
    parameter_value = 'Volumen'

    root = tk.Tk()
    app = PieChartApp(root, file_path, category_column, parameter_column, parameter_value)
    root.mainloop()