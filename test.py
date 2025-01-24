# Dies ist das Hauptfile für den Revit Plugin "LostData". Der Plugin läuft auf Revit 22. 
# Beim Erstellen eines Projektes in Revit, gehen Daten verloren oder es wurde vergessen einzelne Daten abzufüllen. Mittels LostData werden die bestehenden Daten von den ausgewählten Bauteilen visualisiert, überprüft und angepasst. 
# 
# Downloade ironpythonstubs from https://github.com/gtalarico/ironpython-stubs unzip it and place it somewhere on the computer. Copy the stubs.min folder into the lib folder in your projekt. 
# Copy the link to the location of the stubs.min, go to visualstudiocode/extentions:python/rightclick/

import pandas as pd
import matplotlib as mt
import Autodesk.Revit.DB as DB

from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Analysis import *
from Autodesk.Revit.UI import *

from pyrevit import revit




print("hello")
