from staruml_classdiagramm import load_file
from staruml_classdiagramm import exist_class
from staruml_classdiagramm import exist_attribute
from staruml_classdiagramm import exist_association
from staruml_classdiagramm import exist_inheritance
from staruml_classdiagramm import version
from staruml_classdiagramm import list_diagram_class

file = load_file('Klasse.mdj')

exist_inheritance("Person", "Schüler")
exist_inheritance("Person", "Lehrer")