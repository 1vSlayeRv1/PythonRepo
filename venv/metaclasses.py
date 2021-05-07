def upper_attr(future_class_name, future_class_parents, future_class_attr):
    attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith("__"))
    uppercase_attr = dict((name.upper(), value) for name, value in attrs)
    return type(future_class_name, future_class_parents, uppercase_attr)


class Foo(metaclass=upper_attr):
    bar = 'rip'

print("bar is",hasattr(Foo, 'bar'))
print("BAR is",hasattr(Foo, 'BAR'))


class UpperAttr(type):
    def __new__(cls, future_class_name, future_class_parents, future_class_arg):
        attrs = ((name, value) for name, value in future_class_arg.items() if not name.startswith("__"))
        uppercase_attr = dict((name.upper(), value) for name, value in attrs)

        return type.__new__(cls, future_class_name, future_class_parents, uppercase_attr)


class Foo2(metaclass=UpperAttr):
    kek = 'lol'

print("kek is",hasattr(Foo2,'kek'))
print("KEK is",hasattr(Foo2,'KEK'))