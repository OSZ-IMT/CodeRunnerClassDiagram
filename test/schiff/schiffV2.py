import libV2 as lib

file = lib.load_file('schiff.mdj')

# tests
lib.exist_class("Schiff")
lib.exist_attribute("Schiff", "laenge", "int")
lib.exist_attribute("Schiff", "treffer", "int")
lib.exist_attribute("Schiff", "bezeichnung", "String")
lib.exist_attribute("Schiff", "koordinaten", "String[]")


lib.exist_method("Schiff", "Schiff")
lib.exist_method("Schiff", "zerstoert", parameter_out="bool")
lib.exist_method("Schiff", "hatKoordinate", parameter_in="String", parameter_out="bool")
lib.exist_method("Schiff", "getLaenge", parameter_out="int")
lib.exist_method("Schiff", "setLaenge", parameter_in="int", parameter_out="void")