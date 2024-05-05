# Version 2 - 240505

import json
from types import SimpleNamespace

file = None
visDict = {'-': 'private', '+': 'public', '#': 'protected'}
ignore_case = True
alternative_dir = {}

lang = {
    'de': {
        'file_missing': 'StarUML Klassendiagramm "{arg0}" nicht gefunden.',
        'class.exist': 'Klasse {arg0} ist.',
        'class.double': '!Klasse {arg0} existiert {arg1}x im Modell.',
        'class.stereotype': '!Klasse {arg0} hat unbekannten Stereotype {arg1}.',
        'class.exist.no': 'Klasse {arg0} ist nicht!',
        'class.exist.abstract': 'Klasse {arg0} ist abstract.',
        'class.exist.abstract.no': 'Klasse {arg0} ist abstract nicht!',
        'attribute': 'In Klasse {arg0} ist Attribut {arg1}.',
        'attribute.double': '!Attribut {arg0}.{arg1} existiert {arg2}x im Modell.',
        'attribute.no': '!Attribut {arg0}.{arg1} fehlt!',
        'attribute.visibility.no': '!Attribut {arg0}.{arg1} hat falsche/keine Sichtbarkeit.',
        'attribute.data': 'In Klasse {arg0} ist Attribut {arg1} mit Datentyp {arg2}.',
        'attribute.data.no': '!Attribut {arg0}.{arg1}: {arg2} exisitiert nicht.',
        'association': 'Assoziation zwischen {arg0} und {arg1} existiert.',
        'association.no': '!Assoziation zwischen {arg0} und {arg1} existiert nicht',
        'association.double': '!Assoziation zwischen {arg0}-{arg1} existiert {arg2}x im Modell.',
        'association.multiplicity': 'Assoziation zwischen {arg2} {arg0} zu {arg3} {arg1} existiert.',
        'association.multiplicity.missing': 'Assoziation zwischen {arg0} zu {arg1} enthält keine Multiplizität.',
        'association.multiplicity.no': '!Assoziation zwischen {arg2} {arg0} zu {arg3} {arg1} existiert mit.',
        'association.aggregation': 'Aggregation {arg2} {arg0} zu {arg1} existiert.',
        'association.aggregation.no': '!Aggregation {arg2} {arg0} zu {arg1} existiert nicht.',
        'inheritance': 'Vererbung zwischen {arg0} und {arg1} ist nicht.',
        'inheritance.no': '!Vererbung zwischen {arg0} und {arg1} existiert nicht.',
        'inheritance.double': '!Vererbung zwischen {arg0} und {arg1} {arg2}x im Modell.',
        'method': 'In Klasse {arg0} ist Methode {arg1}.',
        'method.no': '!Methode {arg0}.{arg1}() existiert nicht.',
        'method.double': '!Methode {arg0}.{arg1}() existiert {arg2}x im Modell.',
        'method.parameter.no': '!Methode {arg0}.{arg1}(): hat keine Parameter ({arg2}/{arg3}).',
        'method.parameter.in': 'Methode {arg0}.{arg1}({arg2}) existiert.',
        'method.parameter.in.no': '!Methode {arg0}.{arg1}({arg2}) existiert nicht.',
        'method.parameter.out': 'Methode {arg0}.{arg1}(): {arg2} existiert.',
        'method.parameter.out.no': '!Methode {arg0}.{arg1}(): {arg2} existiert nicht.',
        'method.parameter.inout': 'Methode {arg0}.{arg1}({arg2}): {arg3} existiert.',
        'method.parameter.inout.no': '!Methode {arg0}.{arg1}({arg2}): {arg3} existiert nicht.',
    }
}
lang_default = 'de'


def version():
    print("240505")


def lower(a, b):
    global ignore_case

    # convert to list
    if not type(a) is list:
        a = [a]
    if not type(b) is list:
        b = [b]

    # convert case?
    if ignore_case:
        for i in range(0, len(a)):
            a[i] = a[i].lower()

        for i in range(0, len(b)):
            b[i] = b[i].lower()

    # add replaces
    for i in range(0, len(a)):
        if a[i] in alternative_dir:
            a = alternative_dir[a[i]] + a

    for i in range(0, len(b)):
        if b[i] in alternative_dir:
            b = alternative_dir[b[i]] + b

    for ai in a:
        for bi in b:
            if ai == bi:
                return True

    return False


def alternative(base, replace):
    """
    Replace base with replace, e.g. for attribute name, class name, and method
    :param base:
    :param replace: alternative
    :return:
    """
    alternative_dir[base] = replace


def _(txt, arg0=None, arg1=None, arg2=None, arg3=None):
    """
    Translate a text
    :param txt:
    :param arg0:
    :return:
    """
    if txt in lang[lang_default]:
        key = lang[lang_default][txt]
    else:
        key = '!!!' + txt

    if arg0 is None:
        return key
    return key.format(arg0=arg0, arg1=arg1, arg2=arg2, arg3=arg3)


def _t(txt, yes, arg0=None, arg1=None, arg2=None, arg3=None):
    """
    Translate a text
    :param txt:
    :param yes: true: use this txt, false: add .no to show the wrong text.
    :param arg0:
    :return:
    """
    if (yes):
        return _(txt, arg0, arg1, arg2, arg3)
    return _(txt + ".no", arg0, arg1, arg2, arg3)


def load_file(name):
    """
    Parse mdj JSON into an object with attributes corresponding to dict keys.
    :param name: file name
    :return: opened file as simpleobject map
    """
    try:
        global file
        # data = Path(name).read_text()
        with open(name, "r", encoding="utf-8") as f:
            data = f.read()
        file = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        return file
    except:
        print(_('file_missing', name))
        raise Exception(_('file_missing', name))


def get_diagram_class(name, print_basic_error=False):
    """
    Return the list of diagram class, with this name
    :param print_basic_error: print error message if
    :param name: name of the class
    :return: list with classes or empty list
    """
    founds = []

    for e in file.ownedElements[0].ownedElements:
        if e._type == "UMLClass":
            if lower(e.name, name):
                founds.append(e)

    if print_basic_error:
        if len(founds) != 1:
            print(_('class.double', name, len(founds)))

        if len(founds) == 1 and 'stereotype' in founds[0].__dict__:
            st = founds[0].stereotype
            if st != 'abstract' and st != 'interface':
                print(_('class.stereotype', name, st))
                return []

    return founds


def list_diagram_class():
    """
    List all found classes
    :param name: name of the class
    :return: Number of classes found
    """
    for e in file.ownedElements[0].ownedElements:
        if e._type == "UMLClass":
            print(e.name)


# Return a diagram class, if exist
def get_diagram_class_id(name):
    c = get_diagram_class(name)
    if len(c) != 1:
        return False
    return c[0]._id


def get_diagram_attribute(cname, name, print_basic_error=False):
    """
    Get Attribute of specified class
    :param cname: Name of class
    :param name: name of the attribute
    :param print_basic_error: print error message if
    :return:
    """
    founds = []

    cl = get_diagram_class(cname, print_basic_error)
    if len(cl) != 1:
        return founds

    cl = cl[0]
    for e in cl.attributes:
        if e._type == "UMLAttribute":
            if lower(e.name, name):
                founds.append(e)

    if print_basic_error and len(founds) != 1:
        print(_('attribute.double', cname, name, len(founds)))

    return founds


def get_diagram_method(cname, name, print_basic_error=False):
    cl = get_diagram_class(cname, print_basic_error)
    found = []
    if len(cl) != 1:
        return found
    cl = cl[0]

    if not 'operations' in cl.__dict__:
        if print_basic_error:
            print(_t('method', False, cname, name))
        return found

    for e in cl.operations:
        if e._type == "UMLOperation" and lower(e.name, name):
            found.append(e)

    if print_basic_error and len(found) != 1:
        print(_('method.double', cname, name, len(found)))

    return found


def get_diagram_association(c1name, c2name, print_basic_error=False):
    founds = []

    c1 = get_diagram_class(c1name, print_basic_error)
    if len(c1) != 1:
        return founds
    id1 = c1[0]._id
    id1_found = False

    c2 = get_diagram_class(c2name, print_basic_error)
    if len(c2) != 1:
        return founds
    id2 = c2[0]._id
    id2_found = False

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
                founds.append(a)

            # reset
            id1_found = False
            id2_found = False

    if print_basic_error and len(founds) > 1:
        print(_('association.double', c1name, c2name, len(founds)))

    return founds


def get_diagram_inheritance(parent_name, child_name, print_basic_error=True):
    parent = get_diagram_class(parent_name, print_basic_error)
    child = get_diagram_class(child_name, print_basic_error)
    found = []

    # exist?
    if len(parent) != 1 or len(child) != 1:
        return found
    parent = parent[0]
    child = child[0]

    # run over all child ass and search a match
    if hasattr(child, 'ownedElements'):
        for a in child.ownedElements:
            if a._type != 'UMLGeneralization':
                continue

            if a.target.__dict__['$ref'] == parent._id:
                found.append(child)

    # run over all parent ass and search a match
    if hasattr(parent, 'ownedElements'):
        for a in parent.ownedElements:
            if a._type != 'UMLGeneralization':
                continue

            if a.source.__dict__['$ref'] == child._id:
                found.append(child)

    if print_basic_error:
        if len(found) != 1:
            print(_('inheritance.double', parent_name, child_name, len(found)))

    return found


def exist_class(name, abstract=False):
    """
    Check if class exist and print a message
    :param name: name of class
    :param abstract: special stereotype exist
    :return: None
    """
    cls = get_diagram_class(name, True)
    if len(cls) != 1:
        return

    if abstract is False:
        print(_t('class.exist', True, name))
        return

    cls = cls[0]

    # check Abstract
    erg = ('isAbstract' in cls.__dict__ and cls.isAbstract is True) or (
            'stereotype' in cls.__dict__ and cls.stereotype == 'abstract')
    print(_t('class.exist.abstract', erg, name))


def exist_attribute(cname, name, data=None, visibility=None):
    """
    Check if attribute of this class exist and print a message
    :param cname: name of class
    :param name: name of attribute
    :param data: (Optional) datatype of attribute
    :param visibility: (Optional) datatype of attribute: +,#,-
    :return: None
    """
    global ignore_case

    att = get_diagram_attribute(cname, name, True)
    if len(att) != 1:
        return
    att = att[0]

    if visibility is not None and (not hasattr(att, visibility) or not att.visibility == visDict[visibility]):
        print(_t("attribute.visibility", False, cname, name))
        return

    if data is None:
        print(_("attribute", cname, name))
        return

    print(_t("attribute.data", 'type' in att.__dict__ and lower(att.type, data), cname, name, data))


def exist_method(cname, name, parameter_in=None, parameter_out=None):
    """
    Check if method of this class exist and print a message
    :param cname: name of class
    :param name: name of method
    :param parameter_in: (optional) datatype of parameter
    :param parameter_out: (optional) datatype of return value
    :return: None
    """
    att = get_diagram_method(cname, name, True)

    if len(att) != 1:
        return

    if parameter_in is None and parameter_out is None:
        print(_t('method', len(att) == 1, cname, name))
        return

    att = att[0]

    if not hasattr(att, 'parameters'):
        print(_('method.parameter.no', cname, name, parameter_in, parameter_out))
        return

    parameter_in_found = False
    if parameter_in is not None:
        parameter_in_id = get_diagram_class_id(parameter_in)
        if not parameter_in_id:
            parameter_in_id = parameter_in

        for p in att.parameters:
            if not hasattr(p, 'direction') and hasattr(p, 'type') and ((not isinstance(p.type, SimpleNamespace) and lower(parameter_in_id, p.type)) or (hasattr(p.type, '$ref') and parameter_in_id == p.type.__dict__['$ref'])):
                parameter_in_found = True

    parameter_out_found = False
    if parameter_out is not None:
        parameter_out_id = get_diagram_class_id(parameter_out)
        if not parameter_out_id:
            parameter_out_id = parameter_out

        for p in att.parameters:
            if hasattr(p, 'direction') and p.direction == "return" and hasattr(p, 'type') and ((not isinstance(p.type, SimpleNamespace) and lower(parameter_out_id, p.type)) or (hasattr(p.type, '$ref') and parameter_out_id == p.type.__dict__['$ref'])):
                parameter_out_found = True

    if not parameter_in is None and not parameter_out is None:
        print(_t('method.parameter.inout', parameter_in_found and parameter_out_found, cname, name, parameter_in,
                 parameter_out))
        return

    if not parameter_in is None:
        print(_t('method.parameter.in', parameter_in_found, cname, name, parameter_in))
        return

    print(_t('method.parameter.out', parameter_out_found, cname, name, parameter_out))


def exist_association(c1name, c2name, c1multi=None, c2multi=None, aggregation=None):
    """
    Check if the association between c1name and c2name exist with multiplicity c1multi and c2multi
    :param c1name:
    :param c2name:
    :param c1multi: multiplicity for class c1name
    :param c2multi: multiplicity for class c2name
    :param aggregation: composite or shared
    :return:
    """
    ass = get_diagram_association(c1name, c2name, True)

    if len(ass) != 1:
        return
    ass = ass[0]

    if c1multi is None and c2multi is None and aggregation is None:
        print(_('association', c1name, c2name))
        return

    id1 = get_diagram_class_id(c1name)
    id1_found = False
    id2 = get_diagram_class_id(c2name)
    id2_found = False
    ass1ref = ass.end1.reference.__dict__['$ref']
    ass2ref = ass.end2.reference.__dict__['$ref']

    if aggregation is not None:

        if id1_found is False and ass1ref == id1 and 'aggregation' in ass.end1.__dict__ and ass.end1.aggregation == aggregation:
            id1_found = True
        if id1_found is False and ass2ref == id1 and 'aggregation' in ass.end2.__dict__ and ass.end2.aggregation == aggregation:
            id1_found = True

        print(_t('association.aggregation', id1_found, c1name, c2name, aggregation))
        return

    # has muliplicity?
    if 'multiplicity' not in ass.end1.__dict__ or 'multiplicity' not in ass.end1.__dict__:
        print(_('association.multiplicity.missing', c1name, c2name))

    e1m = c1multi
    e2m = c2multi

    # need to check both ends
    if id1_found is False and ass1ref == id1 and lower(ass.end1.multiplicity, c1multi):
        id1_found = True
        e1m = ass.end1.multiplicity
    if id1_found is False and ass1ref == id2 and lower(ass.end2.multiplicity, c1multi):
        id1_found = True
        e1m = ass.end2.multiplicity
    if id2_found is False and ass2ref == id1 and lower(ass.end1.multiplicity, c2multi):
        id2_found = True
        e2m = ass.end1.multiplicity
    if id2_found is False and ass2ref == id2 and lower(ass.end2.multiplicity, c2multi):
        id2_found = True
        e2m = ass.end2.multiplicity

    print(_t('association.multiplicity', id1_found and id2_found, c1name, c2name, e1m, e2m))


def exist_inheritance(c1name, c2name):
    ass = get_diagram_inheritance(c1name, c2name, True)
    print(_t('inheritance', len(ass) == 1, c1name, c2name))
