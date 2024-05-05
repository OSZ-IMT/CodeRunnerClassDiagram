from staruml_classdiagramm import load_file
from staruml_classdiagramm import exist_class
from staruml_classdiagramm import exist_attribute
from staruml_classdiagramm import exist_association
from staruml_classdiagramm import exist_inheritance
from staruml_classdiagramm import exist_method
from staruml_classdiagramm import version
from staruml_classdiagramm import alternative

version()

file = load_file('A34.mdj')

alternative('*',['0..*'])

# tests
# exist_method('Ladung', 'getName', None, 'String')
# exist_method('Ladung', 'setName', 'String')
#
# exist_method('Raumschiff', 'addLadung', 'Ladung')
# exist_method('Raumschiff', 'removeLadung', 'Ladung')
#
# exist_method('Ladung', 'getVolumen', None, ['int', 'double', 'float'])
# exist_method('Ladung', 'setVolumen', ['int', 'double', 'float'])
#
# exist_method('Raumschiff', 'fliegen', 'int')
exist_method('Raumschiff', 'schiessen', 'Raumschiff')
exist_method('Raumschiff', 'treffer', 'Raumschiff')