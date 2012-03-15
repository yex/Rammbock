from binary_tools import to_0xhex
from OrderedDict import OrderedDict


class _StructuredElement(object):

    def __init__(self, name):
        self._name = '%s %s' % (self._type, name)
        self._fields = OrderedDict()

    def __setitem__(self, name, value):
        self._fields[name] = value

    def __getitem__(self, name):
        return self._fields[str(name)]

    def __getattr__(self, name):
        return self[name]

    def __str__(self):
        return self._name

    def __repr__(self):
        result = '%s\n' % self._name
        for field in self._fields.values():
            result +=self._format_indented('%s' % repr(field))
        return result

    def __contains__(self, key):
        return key in self._fields

    def _format_indented(self, text):
        return ''.join(['  %s\n' % line for line in text.splitlines()])

    @property
    def _raw(self):
        return self._get_raw_bytes()
        
    def _get_raw_bytes(self):
        return ''.join((field._raw for field in self._fields.values()))

    def __len__(self):
        return sum(len(field) for field in self._fields.values())


class List(_StructuredElement):

    _type = 'List'

    def __init__(self, name, type_name):
        self._name = '%s %s[]' % (type_name, name)
        self._fields = OrderedDict()


class Struct(_StructuredElement):

    _type = 'Struct'

    def __init__(self, name, type_name):
        self._name = '%s %s' % (type_name, name)
        self._fields = OrderedDict()


class Union(_StructuredElement):

    _type = 'Union'

    def __init__(self, name, length):
        self._length = length
        _StructuredElement.__init__(self, name)

    def _get_raw_bytes(self):
        raw_bytes = [field._raw for field in self._fields.values()]
        max_raw = ''
        for raw in raw_bytes:
            if len(raw) > len(max_raw):
                max_raw = raw
        return max_raw.ljust(self._length, '\x00')


class Message(_StructuredElement):

    _type = 'Message'

    def _add_header(self, header):
        new = OrderedDict({'_header':header})
        new.update(self._fields)
        self._fields = new


class Header(_StructuredElement):

    _type = 'Header'


class Field(object):

    def __init__(self, type, name, value, aligned_len=None, little_endian=False):
        self._type = type
        self._name = name
        self._original_value = value
        self._length = aligned_len if aligned_len else len(value)
        self._little_endian = little_endian

    @property
    def _value(self):
        return self._original_value[::-1] if self._little_endian else self._original_value
    # TODO: If needed, original value and raw value can be precalculated
    # in __init__

    @property
    def name(self):
        return self._name

    @property
    def int(self):
        return int(self)

    def __int__(self):
        return int(to_0xhex(self._value), 16)

    @property
    def hex(self):
        return hex(self)

    def __hex__(self):
        return to_0xhex(self._value)

    @property
    def bytes(self):
        return self._value

    @property
    def chars(self):
        return str(self._value)

    @property
    def ascii(self):
        return ''.join(i for i in self._value if 128 > ord(i) >= 32)

    @property
    def _raw(self):
        return self._original_value.ljust(self._length, '\x00')

    def __str__(self):
        return self.hex

    def __repr__(self):
        return '%s = %s' % (self.name, str(self))

    def __len__(self):
        return self._length
