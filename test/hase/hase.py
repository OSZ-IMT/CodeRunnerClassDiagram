from libV2 import load_file
from libV2 import exist_class
from libV2 import exist_attribute
from libV2 import exist_association
from libV2 import exist_inheritance

file = load_file('hase.mdj')

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
exist_attribute("Consumer", "numberOfOrder", "int", "-")
exist_attribute("Consumer", "birthday")

exist_inheritance("Customer", "Company")
exist_attribute("Company", "name", "String", "-")
exist_attribute("Company", "contract", "String", "-")
