from libV2 import load_file
from libV2 import exist_class
from libV2 import exist_attribute
from libV2 import exist_association
from libV2 import exist_inheritance
from libV2 import version
from libV2 import list_diagram_class

version()

file = load_file('stundenplan.mdj')

list_diagram_class()

# test1
exist_class("Schüler")
exist_class("Klasse")
exist_class("Lehrer")
exist_class("Unterricht")
exist_class("Fach")
exist_class("Raum")
exist_class("Klasse")
exist_class("Person")

# test2
exist_attribute("Person", "name")
exist_attribute("Person", "geschlecht")
exist_attribute("Person", "geburt")

# test3
exist_attribute("Klasse", "name")
exist_attribute("Klasse", "einschulung")

# test4
# TODO exist_attribute("Lehrer", "name")

# test5
exist_attribute("Unterricht", "block")
exist_attribute("Unterricht", "tag")

exist_attribute("Fach", "name")
exist_attribute("Fach", "bezeichnung")

exist_attribute("Raum", "name")
exist_attribute("Raum", "platz")

exist_association("Klasse", "Lehrer", "*", "1")

exist_association("Lehrer", "Fach", "*", "*")

exist_association("Lehrer", "Unterricht", "1", "*")

exist_association("Raum", "Unterricht", "1", "*")

exist_association("Klasse", "Unterricht", "1", "1..*")

# TODO exist_association("Klasse", "Schüler", "1", "1..*")

exist_inheritance("Person", "Schüler")

exist_inheritance("Person", "Lehrer")