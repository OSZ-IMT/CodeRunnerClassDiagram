from staruml_objectdiagramm import load_file
from staruml_objectdiagramm import version
from staruml_objectdiagramm import print_objects
from staruml_objectdiagramm import exist_object

version()

load_file('A23.mdj')

# tests
print_objects()
exist_object('Nanostruktur', [['name','Nanostruktur'],['gewicht','1400'],['volumen','60'],['typ','Baustoff']])
