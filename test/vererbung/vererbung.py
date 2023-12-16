from libV2 import load_file
from libV2 import exist_class
from libV2 import exist_attribute
from libV2 import exist_association
from libV2 import exist_inheritance
from libV2 import version
from libV2 import alternative

version()

file = load_file('vererbung1.mdj')


# test1
exist_class("Person2")
exist_class("Person31")
exist_attribute("Person", "id1", "int", "#")
exist_attribute("Person", "lastname", "String", "#")
exist_attribute("Person", "firstname", "String", "#")
exist_attribute("Person", "email", "String", "#")
exist_attribute("Person", "telephone", "String", "#")
exist_inheritance("Person", "Lehrer")

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

exist_inheritance("Person", "Employee")
exist_class("Employee", "abstract")