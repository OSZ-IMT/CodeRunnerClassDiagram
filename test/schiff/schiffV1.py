import diagramLib as dL

dL.load_file('schiff.xmi')

# tests
dL.exist_class("Schiff")
dL.exist_attribute("Schiff", "laenge", "int")
dL.exist_attribute("Schiff", "treffer", "int")
dL.exist_attribute("Schiff", "bezeichnung", "String")
dL.exist_attribute("Schiff", "koordinaten", "String[]")


dL.exist_method("Schiff", "Schiff")
dL.exist_method("Schiff", "zerstoert", parameter_out="bool")
dL.exist_method("Schiff", "hatKoordinate", parameter_in="String", parameter_out="bool")
dL.exist_method("Schiff", "getLaenge", parameter_out="int")
dL.exist_method("Schiff", "setLaenge", parameter_in="int", parameter_out="void")