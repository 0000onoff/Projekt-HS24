# LostData

LostData is an extention for pyRevit, Revit22, writen with python.

## Installation

To install you have to download Revit22, pyRevit, RevitLookup, Revit Python Shell, VisualStudioCode, and get the stubs.min from ironpython-stubs-master. The folderstructur is to reference within the Revit project.

## Usage

In the folder are two buttons. One is CheckData and the other is ChangeData. 

CheckData will export a csv file. In the code you have to show a new path, where to put it. Te file will be read by the file Datenbearbeitung that is located under Scripts in the outer laier. It will generate a circlediagramm in which you find the categories to choose from.

ChangeData will ask you to select elements in Revit22. After this it will ask for an category and for a parameter to change. Then you have the ability to tipe a new value in. The selected elements will take on this new value. However only the sringinputs will change at the moment.

## Support

There is currently no support, because the extension is not finished as it is.

## Roadmap 

Further development will be for:

-A script, that is compleatly operable from the open Revit22
-A better userinterface
-A more structured script
-The ability to choose more parameters

## Project status
The Project is currently under construction.