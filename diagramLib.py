# Version 2

from xml.dom import minidom

# file = None


def _att(att, name):
    value = att.attributes[name].value.lower()
    value = value.replace("%5b", "[")
    value = value.replace("%5d", "]")
    return value


def load_file(name):
    global file
    file = minidom.parse(name)


def get_diagram_class(name):
    classes = file.getElementsByTagName('packagedElement')
    for e in classes:
        if e.attributes['xmi:type'].value == "uml:Class" and e.attributes['name'].value.lower() == name.lower():
            return e
    return False


def get_diagram_attribute(cname, name):
    cl = get_diagram_class(cname)
    if not cl:
        return False
    ol = cl.getElementsByTagName('ownedAttribute')
    for e in ol:
        if e.attributes['xmi:type'].value == "uml:Property" and e.attributes['name'].value.lower() == name.lower():
            return e
    return False


def get_diagram_method(cname, name):
    cl = get_diagram_class(cname)
    if not cl:
        return False
    ol = cl.getElementsByTagName('ownedOperation')
    for e in ol:
        if e.attributes['xmi:type'].value == "uml:Operation" and e.attributes['name'].value.lower() == name.lower():
            return e
    return False


def get_diagram_association(c1name, c2name):
    id1 = get_diagram_class(c1name).attributes['xmi:id'].value
    id1_found = False
    id2 = get_diagram_class(c2name).attributes['xmi:id'].value
    id2_found = False
    ass = file.getElementsByTagName('ownedMember')
    for e in ass:
        if not e.attributes['xmi:type'].value == "uml:Association":
            continue

        ends = e.getElementsByTagName('ownedEnd')
        for en in ends:
            if not id1_found and en.attributes['type'].value == id1:
                id1_found = True
                continue
            if not id2_found and en.attributes['type'].value == id2:
                id2_found = True
                continue
        if id1_found and id2_found:
            return e
        else:
            id1_found = False
            id2_found = False
    return False


def exist_class(name):
    print("Klasse",name,"existiert", end="")
    if not get_diagram_class(name):
        print(" nicht!")
    else:
        print(".")


def exist_attribute(cname, name, data=None):
    print("In Klasse", cname, "existiert Attribut", name, end="")
    att = get_diagram_attribute(cname, name)
    if not att:
        print(" nicht!")
        return

    if not att.attributes['visibility'].value == "private":
        print(" mit falscher Sichtbarkeit!")

    if data is None:
        print(".")
        return

    print(" mit Datentyp",data, end="")
    if not _att(att,'type')[:-3] == data.lower():
        print(" nicht!")
    else:
        print(".")


def exist_method(cname, name, parameter_in=None, parameter_out=None):
    print("In Klasse", cname, "existiert Methode", name, end="")
    att = get_diagram_method(cname, name)
    if not att:
        print(" nicht!")
        return

    if parameter_in is None or parameter_out is None:
        print(".")
        return

    parameter_in_found = False
    if parameter_in is not None:
        print(" mit Parameter", parameter_in, end="")
        for p in att.getElementsByTagName('ownedParameter'):
            if p.attributes['direction'].value == "in" and _att(p,'name') == parameter_in.lower():
                parameter_in_found = True

    parameter_out_found = False
    if parameter_out is not None:
        print(" mit Return", parameter_out, end="")
        for p in att.getElementsByTagName('ownedParameter'):
            if p.attributes['direction'].value == "out" and _att(p,'name') == parameter_in.lower():
                parameter_out_found = True

    if (parameter_in is not None and parameter_in_found) or (parameter_out is not None and parameter_out_found):
        print(".")
    else:
        print(" nicht!")


def exist_association(c1name, c2name, c1multi=None, c2multi=None):
    print("Beziehung zwischen",c1name,"und",c2name,"existiert", end="")
    ass = get_diagram_association(c1name, c2name)
    if c1multi is None:
        if not ass:
            print(" nicht!")
        else:
            print(".")
    else:
        print(" mit Multiplizität",c1multi,"und",c2multi, end="")
        id1 = get_diagram_class(c1name).attributes['xmi:id'].value
        id1_found = False
        id2 = get_diagram_class(c2name).attributes['xmi:id'].value
        id2_found = False

        ends = ass.getElementsByTagName('ownedEnd')
        for en in ends:
            a = en.getElementsByTagName('lowerValue')[0].attributes["value"].value
            if not id1_found and en.attributes['type'].value == id1 and a == c1multi:
                id1_found = True
                continue
            if not id2_found and en.attributes['type'].value == id2 and a == c2multi:
                id2_found = True
                continue
        if id1_found and id2_found:
            print(".")
        else:
            print(" nicht!")