from staruml_classdiagramm import load_file
from staruml_classdiagramm import exist_class
from staruml_classdiagramm import exist_attribute
from staruml_classdiagramm import exist_association
from staruml_classdiagramm import exist_inheritance
from staruml_classdiagramm import version
from staruml_classdiagramm import alternative

version()

file = load_file('Klasse_Raumschiffe_neu.mdj')

alternative('*',['0..*'])

# tests
exist_association('Handelsstation', 'Sonnensystem', '*', '1')
exist_association('Handelsstation', 'Ladung', '1', ['*','0..*'])