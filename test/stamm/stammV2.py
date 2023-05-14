import libV2 as lib

file = lib.load_file('stamm.mdj')

# tests
lib.exist_class("Stamm")
lib.exist_attribute("Stamm", "name", "String")
lib.exist_attribute("Stamm", "gruendung", "int")

lib.exist_class("Zwerg")
lib.exist_attribute("Zwerg", "name", "String")
lib.exist_attribute("Zwerg", "alter", "int")
lib.exist_attribute("Zwerg", "machtfaktor", "int")

lib.exist_class("MagischerGegenstand")
lib.exist_attribute("MagischerGegenstand", "typ", "String")
lib.exist_attribute("MagischerGegenstand", "faktor", "int")

lib.exist_association("Zwerg","Stamm")
lib.exist_association("Zwerg2","Stamm")
lib.exist_association("MagischerGegenstand","Stamm")
lib.exist_association("Zwerg","Stamm","*","1")

lib.exist_association("Zwerg","MagischerGegenstand")
lib.exist_association("Zwerg","MagischerGegenstand","1","*")