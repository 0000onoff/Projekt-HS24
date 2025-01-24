
import os, sys

# This is the description of the button.
__title__= "GetData"
__doc__= """Description:
This is a button for selecting and editting a parameter of selected element or type.

Select an Element
Click on the button
Select the ID-Element, you want to change
Change the Parameter
Enter"""

# Imports
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
    print("Keine Elemente ausgewählt.")

#The conecting part of the code, so we get out of the selection the parameters with no problems, is currently not fuli working, thats why following is an example how it wil work.
wall_id = ElementId(2475124)
wall= doc.GetElement(wall_id)
print (wall)
#print (list(wall.Parameters))

#for p in wall.Parameters:
#    print(p)
#    print(".Name:{}".format(p.Definition.Name))
#    print(".IsShared:{}".format(p.IsShared))

# Creats a dictionary for all available parameters of the selection.
def get_all_parameters(wall):
    parameter_map = {}
    try:
        for p in wall.Parameters:
            if p and p.Definition:
                parameter_map[p.Definition.Name] = p
    except Exception as e:
        print("Error: {}".format(e))
    return parameter_map

# Get the parameters of the wall.
parameter_map = get_all_parameters(wall)

# Selecting the parameter.
if parameter_map:
    parameter_names_sorted = sorted(parameter_map.keys())
    selected_name = forms.ask_for_one_item(
        parameter_names_sorted,
        default=None,
        prompt="Wählen Sie einen Parameter aus",
        title="Parameter auswählen")

    if selected_name:
        selected_parameter = parameter_map[selected_name]   
    else:
        print("Keine Auswahl vorgenommen.")
        sys.exit()
else:
    print("Keine Parameter verfügbar.")
    sys.exit()

# Prints for control.
print(selected_parameter)
print("Selected Parameter Name:{}".format(selected_parameter.Definition.Name))
print("BuiltInParameter: {}".format(selected_parameter.Definition.BuiltInParameter))
print("Storage Type: {}".format(selected_parameter.StorageType))

# When parameter is typebased.
#wall_type= wall.WallType
#wall_manufacturer = wall_type.get_Parameter(BuiltInParameter.ALL_MODEL_MANUFACTURER).AsValueString()
#print(wall_manufacturer)
# When parameter is builtin.
wall_comment = wall.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS).AsValueString()
#print(wall_comment)

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
    wall_comment = wall.get_Parameter(BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)
    
    if wall_comment and not wall_comment.IsReadOnly:
        wall_comment.Set(input_newparametervalue)
        print(wall_comment.AsValueString())
    
    else:
        if wall_comment is None:
            print("Parameter nicht vorhanden.")
        elif wall_comment.IsReadOnly:
            print("Parameter kann nicht bearbeitet werden.")

    t.Commit()
    
except Exception as e:
    print("Error", e)
    t.RollBack()