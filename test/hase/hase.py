from staruml_classdiagramm import load_file
from staruml_classdiagramm import exist_class
from staruml_classdiagramm import exist_attribute
from staruml_classdiagramm import exist_association
from staruml_classdiagramm import exist_inheritance
from staruml_classdiagramm import version

version()

file = load_file('hase2.mdj')

# tests
exist_class("Person")
exist_attribute("Person", "id", "int", "#")
exist_attribute("Person", "lastname", "String", "#")
exist_attribute("Person", "firstname", "String", "#")
exist_attribute("Person", "email", "String", "#")
exist_attribute("Person", "telephone", "String", "#")

exist_class("Person", "abstract")

exist_inheritance("Person", "Customer")
exist_class("Customer", "abstract")
exist_attribute("Customer", "status", "char", "#")
exist_attribute("Customer", "paymentType", "char", "#")

exist_inheritance("Customer", "Consumer")
exist_attribute("Consumer", "birthday")

exist_inheritance("Customer", "Company")
exist_attribute("Company", "name", "String", "-")
exist_attribute("Company", "contact", "String", "-")
