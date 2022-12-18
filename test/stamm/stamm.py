import diagramLib as dL

dL.load_file('test/schiff/schiff.xmi')

# tests
dL.exist_class("Stamm")
dL.exist_attribute("Stamm", "name", "String")
dL.exist_attribute("Stamm", "gruendung", "int")

dL.exist_class("Zwerg")
dL.exist_attribute("Zwerg", "name", "String")
dL.exist_attribute("Zwerg", "alter", "int")
dL.exist_attribute("Zwerg", "machtfaktor", "int")

dL.exist_class("MagischerGegenstand")
dL.exist_attribute("MagischerGegenstand", "typ", "String")
dL.exist_attribute("MagischerGegenstand", "faktor", "int")

dL.exist_association("Zwerg","Stamm")
dL.exist_association("Zwerg","Stamm","*","1")

dL.exist_association("Zwerg","MagischerGegenstand")
dL.exist_association("Zwerg","MagischerGegenstand","1","*")
