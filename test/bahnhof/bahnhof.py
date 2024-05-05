from staruml_classdiagramm import load_file
from staruml_classdiagramm import exist_class
from staruml_classdiagramm import exist_attribute
from staruml_classdiagramm import exist_association
from staruml_classdiagramm import exist_inheritance
from staruml_classdiagramm import version

version()

file = load_file('bahnhof.mdj')

# tests
exist_association("Bahnhof", "Bahnlinie", "1..*", ["*","1..*"])
exist_association("Fahrt", "Bahnlinie", "1..*", "1")
exist_association("Fahrt", "Zug", ["1..*","*"], "1")
# exist_association("Fahrt", "Stopp", "1", "1..*", "composite")
exist_association("Bahnhof", "Stopp", "1", "1..*", "composite")


exist_association("Bahnhof", "Stopp")