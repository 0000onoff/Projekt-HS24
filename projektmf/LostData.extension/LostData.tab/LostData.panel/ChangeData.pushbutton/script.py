# This Python file uses the following encoding: utf-8

# This is the description of the button.
__title__= "ChangeData"
__doc__= """Description:
This is a button for selecting and editting a parameter of selected element or type.

Select an Element
Click on the button
Select the ID-Element, you want to change
Change the Parameter
Enter"""

# Imports
import os, sys

from Autodesk.Revit import DB
from Autodesk.Revit import UI

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

from pyrevit import revit, forms, script

# Variables
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Gets the element-ids of the selechtet elements.
selected_ids = uidoc.Selection.GetElementIds()

if selected_ids.Count > 0:
    for element_id in selected_ids:
        print("Ausgewählte Element-ID: {}".format(element_id.IntegerValue))
else:
    forms.alert("Sie haben keine Auswahl vorgenommen. Bitte wählen Sie Elemente aus und versuchen es erneut!")
    exit()

# Gets the categories of the selected elements.
def get_all_categories(doc, selected_ids):
    category_names = []
    for elem_id in selected_ids:
        elem = doc.GetElement(elem_id)
        if elem and elem.Category:
            category_names.append(elem.Category.Name)
        else:
            category_names.append("Keine Kategorie")

# Remove duplicates and sort the list
    unique_categories = sorted(set(category_names))
    return unique_categories

# Example usage of the function
def select_category(doc, selected_ids):
    # Get all unique categories from the selected elements
    unique_categories = get_all_categories(doc, selected_ids)
    
    if unique_categories:
        # Ask the user to select one category
        selected_category = forms.ask_for_one_item(
            unique_categories,
            default=None,
            prompt="Wählen Sie eine Kategorie aus",
            title="Kategorie auswählen"
        )
        
        # Handle the user's selection
        if selected_category:
            TaskDialog.Show("Ausgewählte Kategorie", "Die ausgewählte Kategorie ist: {}".format(selected_category))
        else:
            TaskDialog.Show("Keine Auswahl", "Keine Kategorie wurde ausgewählt.")
    else:
        TaskDialog.Show("Keine Kategorien", "Keine Kategorien verfügbar.")
        
    return selected_category

if not selected_ids:
    TaskDialog.Show("Keine Auswahl", "Es wurden keine Elemente ausgewählt.")
else:
    selected_category_name = select_category(doc, selected_ids)
    
#Zu testzwecken, alles io wird richtig ausgegeben
print (selected_category_name)

def selected_category():
    return "Walls"

def get_all_parameters(doc, selected_category_name):
    parameter_map = {}
    
    # Call the function to get the category name (i.e., "Walls", "Floors", etc.)
    category_name = selected_category_name()
    
    try:
        # Get the BuiltInCategory based on the category name
        category_enum = getattr(BuiltInCategory, "OST_{}".format(category_name.replace(" ", "")), None)

        if category_enum is None:
            print("Falscher Kategoriename: {}".format(category_name))
            return {}

        # Collect all elements in the selected category
        elements_in_category = FilteredElementCollector(doc) \
            .OfCategory(category_enum) \
            .WhereElementIsNotElementType()

        # Collect parameters from the first element in the category
        if elements_in_category:
            first_element = next(iter(elements_in_category))  # Get the first element
            for p in first_element.Parameters:
                if p and p.Definition:
                    parameter_map[p.Definition.Name] = p
        else:
            print("Keine Elemente in der Kategorie.")

    except Exception as e:
        print("Fehler bei Parameter: {}".format(e))

    return parameter_map

#Achtung defoltwert wall
parameter_map = get_all_parameters(doc, selected_category)
#parameter_map = get_all_parameters(doc, selected_category_name)
 
if parameter_map:
    print("Parameter in der Kategorie:")
    for param_name, param in parameter_map.items():  
        print("{}: {}".format(param_name, param))  
else:
    print("Keine Parameter gefunden.") 


# Function to select a parameter from the parameter map
def select_parameter(parameter_map):
    if parameter_map:
        parameter_names_sorted = sorted(parameter_map.keys())
        selected_param_name = forms.ask_for_one_item(
            parameter_names_sorted,
            default=None,
            prompt="Wählen Sie einen Parameter aus",
            title="Parameter auswählen"
        )

        if selected_param_name:
            selected_parameter = parameter_map[selected_param_name]
            print("Der ausgewählte Parameter ist: {}".format(selected_param_name))
            return selected_parameter
        else:
            print("Keine Auswahl vorgenommen.")
            return None
    else:
        print("Keine Parameter verfügbar.")
        return None

# Call the function to let the user select a parameter
selected_parameter = select_parameter(parameter_map)

if selected_parameter:
    print("Name des ausgewählten Parameters: {}".format(selected_parameter.Definition.Name))
    print("BuiltInParameter: {}".format(selected_parameter.Definition.BuiltInParameter))
    print("Format: {}".format(selected_parameter.StorageType))
else:
    print("Es wurde kein Parameter ausgewählt.")

print(selected_parameter)


# Input text for new value for the parameter.
input_newparametervalue = forms.ask_for_string(
    prompt="Bitte geben Sie den neuen Wert für den Parameter ein:",
    title="Wert Eingabe",
    default="Neuen Wert eingeben...")

if input_newparametervalue:
    forms.alert("Sie haben eingegeben: {}".format(input_newparametervalue), title="Eingabe", ok=True)
else:
    forms.alert("Keine Eingabe vorgenommen.", title="Eingabe", ok=True)

print (input_newparametervalue)


# Transaction is specific for Revit and is needed to enter the new value to the parameter. The code uses the curenty open document and the Name of the transaction.
t=Transaction(doc,"Inhalt geändert")

try:
    t.Start()
    for elem_id in selected_ids:
        element = doc.GetElement(elem_id)
        if element.Category and element.Category.Name == selected_category_name:
            param = element.LookupParameter(selected_parameter.Definition.Name)
            if param:
                if not param.IsReadOnly:
                    
                    # Set the new value
                    if param.StorageType == StorageType.String:
                        param.Set(input_newparametervalue)
                        print("Updated Parameter '{}' für Element ID {} und Wert: {}".format(
                            selected_parameter.Definition.Name,
                            elem_id.IntegerValue,
                            input_newparametervalue
                        ))
                    else:
                        print("Parameter '{}' unterstützt kein String.".format(
                            selected_parameter.Definition.Name
                        ))
                else:
                    print("Parameter '{}' von Element ID {} kann nur gelesen werden.".format(
                        selected_parameter.Definition.Name,
                        elem_id.IntegerValue
                    ))
            else:
                print("Parameter '{}' nicht gefunden in Element ID {}.".format(
                    selected_parameter.Definition.Name,
                    elem_id.IntegerValue
                ))
    t.Commit()
    print("Parameter updated.")

except Exception as e:
    print("Error:", e)
    t.RollBack()
