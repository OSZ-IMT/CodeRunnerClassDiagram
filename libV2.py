# Version 2 - 231115

import json
from types import SimpleNamespace
from pathlib import Path

file = None
visDict = {'-': 'private', '+': 'public', '#': 'protected'}


def version():
    print("231118")


def load_file(name):
    """
    Parse mdj JSON into an object with attributes corresponding to dict keys.
    :param name: file name
    :return: opened file as simpleobject map
    """
    try:
        global file
        data = Path(name).read_text()
        file = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        return file
    except:
        print("StarUML Klassendiagramm " + name + " nicht gefunden")
        raise Exception("StarUML Klassendiagramm " + name + " nicht gefunden")


def get_diagram_class(name):
    """
    Return a diagram class, if exist
    :param name: name of the class
    :return: False, if not found or class data
    """
    for e in file.ownedElements[0].ownedElements:
        if e._type == "UMLClass" and e.name.lower() == name.lower():
            return e
    return False


# Return a diagram class, if exist
def get_diagram_class_id(name):
    c = get_diagram_class(name)
    if c is False:
        return False
    return c._id


def get_diagram_attribute(cname, name):
    cl = get_diagram_class(cname)
    if not cl:
        return False
    for e in cl.attributes:
        if e._type == "UMLAttribute" and e.name.lower() == name.lower():
            return e
    return False


def get_diagram_method(cname, name):
    cl = get_diagram_class(cname)
    if not cl:
        return False

    for e in cl.operations:
        if e._type == "UMLOperation" and e.name.lower() == name.lower():
            return e
    return False


def get_diagram_association(c1name, c2name):
    id1 = get_diagram_class_id(c1name)
    id1_found = False
    id2 = get_diagram_class_id(c2name)
    id2_found = False

    # exist?
    if id1 is False or id2 is False:
        return False

    # run over all ass and search a match
    for c in file.ownedElements[0].ownedElements:
        if not hasattr(c, 'ownedElements'):
            continue

        for a in c.ownedElements:
            if a._type != 'UMLAssociation':
                continue

            # check both ends
            if not id1_found and a.end1.reference.__dict__['$ref'] == id1:
                id1_found = True
            if not id1_found and a.end2.reference.__dict__['$ref'] == id1:
                id1_found = True
            if not id2_found and a.end1.reference.__dict__['$ref'] == id2:
                id2_found = True
            if not id2_found and a.end2.reference.__dict__['$ref'] == id2:
                id2_found = True

            # found?
            if id1_found and id2_found:
                return a

            # reset
            id1_found = False
            id2_found = False

    return False


def get_diagram_inheritance(parent_name, child_name):
    parent = get_diagram_class(parent_name)
    child = get_diagram_class(child_name)

    # exist?
    if parent is False or child is False:
        return False

    # run over all child ass and search a match
    if hasattr(child,'ownedElements'):
        for a in child.ownedElements:
            if a._type != 'UMLGeneralization':
                continue

            if a.target.__dict__['$ref'] == parent._id:
                return True


    # run over all parent ass and search a match
    if hasattr(parent,'ownedElements'):
        for a in parent.ownedElements:
            if a._type != 'UMLGeneralization':
                continue

            if a.source.__dict__['$ref'] == child._id:
                return a

    return False


def exist_class(name, abstract=False):
    """
    Check if class exist and print a message
    :param name: name of class
    :param abstract: special stereotype exist
    :return: None
    """
    print("Klasse", name, "ist", end="")
    cls = get_diagram_class(name)
    if not cls:
        print(" nicht!")
        return

    if abstract is False:
        print(".")
        return

    print(" abstract", end="")

    if ('isAbstract' in cls.__dict__ and cls.isAbstract is True) or ('stereotype' in cls.__dict__ and cls.stereotype == 'abstract'):
        print(".")
    else:
        print(" nicht!")


def exist_attribute(cname, name, data=None, visibility=None):
    """
    Check if attribute of this class exist and print a message
    :param cname: name of class
    :param name: name of attribute
    :param data: (Optional) datatype of attribute
    :param visibility: (Optional) datatype of attribute: +,#,-
    :return: None
    """
    print("In Klasse", cname, "ist Attribut", name, end="")
    att = get_diagram_attribute(cname, name)
    if not att:
        print(" nicht!")
        return

    if visibility is not None and not att.visibility == visDict[visibility]:
        print(" mit falscher Sichtbarkeit!", end="")

    if data is None:
        print(".")
        return

    print(" mit Datentyp", data, end="")
    if att.type.lower() == data.lower():
        print(".")
    else:
        print(" nicht!")


def exist_method(cname, name, parameter_in=None, parameter_out=None):
    """
    Check if method of this class exist and print a message
    :param cname: name of class
    :param name: name of method
    :param parameter_in: (optional) datatype of parameter
    :param parameter_out: (optional) datatype of return value
    :return: None
    """
    print("In Klasse", cname, "ist Methode", name, end="")
    att = get_diagram_method(cname, name)
    if not att:
        print(" nicht!")
        return

    if parameter_in is None and parameter_out is None:
        print(".")
        return

    parameter_in_found = False
    if parameter_in is not None:
        print(" mit Parameter", parameter_in, end="")
        for p in att.parameters:
            if p.type == "" and p.name.lower() == parameter_in.lower():
                parameter_in_found = True
    else:
        parameter_in_found = True

    parameter_out_found = False
    if parameter_out is not None:
        print(" mit Return", parameter_out, end="")
        for p in att.parameters:
            if hasattr(p, 'direction') and p.direction == "return" and p.type.lower() == parameter_out.lower():
                parameter_out_found = True
    else:
        parameter_out_found = True

    if parameter_in_found and parameter_out_found:
        print(".")
    else:
        print(" nicht!")


def exist_association(c1name, c2name, c1multi=None, c2multi=None):
    print("Beziehung zwischen", c1name, "und", c2name, "ist", end="")
    ass = get_diagram_association(c1name, c2name)
    if c1multi is None:
        if not ass:
            print(" nicht!")
        else:
            print(".")
    else:
        print(" mit Multiplizität", c1multi, "und", c2multi, end="")

        if not ass:
            print(" nicht!")

        id1 = get_diagram_class_id(c1name)
        id1_found = False
        id2 = get_diagram_class_id(c2name)
        id2_found = False

        # need to check both ends
        if id1_found is False and ass.end1.reference.__dict__['$ref'] == id1 and ass.end1.multiplicity == c1multi:
            id1_found = True
        if id1_found is False and ass.end2.reference.__dict__['$ref'] == id1 and ass.end2.multiplicity == c1multi:
            id1_found = True
        if id2_found is False and ass.end1.reference.__dict__['$ref'] == id2 and ass.end1.multiplicity == c2multi:
            id2_found = True
        if id2_found is False and ass.end2.reference.__dict__['$ref'] == id2 and ass.end2.multiplicity == c2multi:
            id2_found = True

        if id1_found and id2_found:
            print(".")
        else:
            print(" nicht!")


def exist_inheritance(c1name, c2name):
    print("Vererbung zwischen", c1name, "und", c2name, "ist", end="")
    ass = get_diagram_inheritance(c1name, c2name)

    if not ass:
        print(" nicht!")
    else:
        print(".")


