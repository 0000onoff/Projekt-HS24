#This Python file uses the following encoding: utf-8
import os, sys

# This is the description of the button.
__title__= "CheckData"
__doc__= """Description:
This button exports the selected elements from the active view in the active document, including their categories and parameters.

Click on the button
Enter"""

# Imports
import os
import csv

from Autodesk.Revit import DB
from Autodesk.Revit import UI

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

from pyrevit import revit, forms, script

# Variables
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Gets selected elements
selection = [doc.GetElement(id) for id in uidoc.Selection.GetElementIds()]

if not selection:
    script.get_output().print_md("Keine Auswahl vorgenommen. Wähle Elemente aus und führe die Aktion nochmals aus.")
    script.exit()
    
# Prepare data for CSV
header = ["Element ID", "Category", "Parameter Name", "Parameter Value"]
data = []

for element in selection:
    element_id = element.Id.IntegerValue
    category_name = element.Category.Name if element.Category else "Keine Kategorie"

    for param in element.Parameters:
        if param and param.Definition:
            param_name = param.Definition.Name

            # Gets parameter value based on storage type
            if param.StorageType == DB.StorageType.String:
                param_value = param.AsString()
            elif param.StorageType == DB.StorageType.Double:
                param_value = param.AsDouble()
            elif param.StorageType == DB.StorageType.Integer:
                param_value = param.AsInteger()
            elif param.StorageType == DB.StorageType.ElementId:
                param_value = str(param.AsElementId().IntegerValue)
            else:
                param_value = "Kein Wert"

            data.append([element_id, category_name, param_name, param_value])

# Specifies the file path to save the CSV
#csv_file_path = r"C:\Users\mario\Desktop\active_view_export.csv"
#csv_file_path = os.path.expanduser("~/Desktop/active_view_export.csv")
desktop = os.path.join(os.environ["USERPROFILE"], "Desktop") # Attention!
csv_file_path = os.path.join(desktop, "active_view_export.csv")

# Write CSV
with open(csv_file_path, mode='wb') as file:
    writer = csv.writer(file, lineterminator='\n')
    writer.writerow(header)
    writer.writerows(data)

# Print
script.get_output().print_md("CSV-File exportiert nach: {}".format(csv_file_path))