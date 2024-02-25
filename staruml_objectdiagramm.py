# Version 1 - 240225

import json
from types import SimpleNamespace

file = None
ignore_case = True
alternative_dir = {}
diagram = None
objects_known = {}

lang = {
    'de': {
        'file_missing': 'Datei StarUML Objectdiagramm "{arg0}" nicht gefunden.',
        'file_no_diagram': 'In Datei "{arg0}" kein StarUML Objectdiagramm gefunden.',
        'object': 'Objekt {arg0} mit Attribute {arg1} existiert.',
        'object.no': '!Objekt {arg0} mit Attribute {arg1} existiert nicht.'
    }
}
lang_default = 'de'


def version():
    print("240225")


def lower(a, b):
    global ignore_case

    # convert to list
    if not type(a) is list:
        a = [a]
    if not type(b) is list:
        b = [b]

    # convert case?
    if ignore_case:
        for i in range(0,len(a)):
            a[i] = a[i].lower()

        for i in range(0,len(b)):
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
    """
    try:
        global file
        global diagram
        # data = Path(name).read_text()
        with open(name, "r", encoding="utf-8") as f:
            data = f.read()
        file = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))

        # find diagram
        for e in file.ownedElements:
            if e._type != "UMLModel":
                continue

            # check all elements from this model
            for u in e.ownedElements:
                if u._type == "UMLObject":
                    diagram = e.ownedElements
                    return

        # no diagram found
        print(_('file_no_diagram', name))
        raise Exception(_('file_no_diagram', name))

    except:
        print(_('file_missing', name))
        raise Exception(_('file_missing', name))


def print_objects():
    global diagram

    for o in diagram:
        if o._type != "UMLObject":
            continue

        print(o.name)
        # has values?
        if not 'slots' in o.__dict__:
            continue

        for s in o.slots:
            print(s.name+'='+s.value)


def get_diagram_object(name, values):
    global diagram, objects_known

    # exist in cache?
    if name in objects_known:
        return objects_known[name]

    # search otherwise
    for o in diagram:
        if o._type != "UMLObject":
            continue

        # has values?
        if not 'slots' in o.__dict__:
            continue

        # check values
        found_all = True
        for v in values:
            found = False
            for s in o.slots:
                if lower(s.name, v[0]) and lower(s.value, v[1]):
                    found = True
                    break

            if not found:
                found_all = False
                break

        # all values are present
        if found_all:
            objects_known[name] = o
            return o

    # not found
    return None


def exist_object(name, values):
    obj = get_diagram_object(name, values)

    print(_t('object', obj is not None, name, values))