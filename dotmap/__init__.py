from __future__ import print_function
from collections import OrderedDict, MutableMapping
from inspect import ismethod

IPYTHON_CANNARY = '_ipython_canary_method_should_not_exist_'


class DotMap(MutableMapping, OrderedDict):

    def __init__(self, *args, **kwargs):
        self._map = OrderedDict()
        if args:
            assert len(args) == 1
            d = args[0]
            if isinstance(d, dict):
                for k, v in self.__call_items(d):
                    if isinstance(v, dict):
                        v = DotMap(v)
                    if isinstance(v, list):
                        l = []
                        for i in v:
                            n = i
                            if isinstance(i, dict):
                                n = DotMap(i)
                            l.append(n)
                        v = l
                    self._map[k] = v
        if kwargs:
            for k, v in self.__call_items(kwargs):
                self._map[k] = v

    def __call_items(self, obj):
        if hasattr(obj, 'iteritems') and ismethod(getattr(obj, 'iteritems')):
            return obj.iteritems()
        return obj.items()

    def items(self):
        return self.iteritems()

    def iteritems(self):
        return self.__call_items(self._map)

    def __iter__(self):
        return self._map.__iter__()

    def next(self):
        return self._map.next()

    def __setitem__(self, k, v):
        self._map[k] = v

    def __getitem__(self, k):
        if k not in self._map and k != IPYTHON_CANNARY:
            # automatically extend to new DotMap
            self[k] = DotMap()
        return self._map[k]

    def __setattr__(self, k, v):
        if k in {'_map', IPYTHON_CANNARY}:
            super(DotMap, self).__setattr__(k, v)
        else:
            self[k] = v

    def __getattr__(self, k):
        if k == {'_map', IPYTHON_CANNARY}:
            super(DotMap, self).__getattr__(k)
        else:
            return self[k]

    def __delattr__(self, key):
        return self._map.__delitem__(key)

    def __contains__(self, k):
        return self._map.__contains__(k)

    def __str__(self):
        items = []
        for k, v in self.__call_items(self._map):
            if id(v) == id(self):
                items.append('{0}=DotMap(...)'.format(k))
            else:
                items.append('{0}={1}'.format(k, repr(v)))
        joined = ', '.join(items)
        out = '{0}({1})'.format(self.__class__.__name__, joined)
        return out

    __repr__ = __str__

    def toDict(self):
        d = {}
        for k, v in self.items():
            if isinstance(v, DotMap):
                if id(v) == id(self):
                    v = d
                else:
                    v = v.toDict()
            elif isinstance(v, (list, tuple)):
                l = []
                for i in v:
                    n = i
                    if type(i) is DotMap:
                        n = i.toDict()
                    l.append(n)
                if isinstance(v, tuple):
                    v = tuple(l)
                else:
                    v = l
            d[k] = v
        return d

    def empty(self):
        return (not any(self))

    def values(self):
        return self._map.values()

    # ipython support
    def __dir__(self):
        return self.keys()

    @classmethod
    def parse_other(cls, other):
        if isinstance(other, DotMap):
            return other._map
        return other

    def __cmp__(self, other):
        other = DotMap.parse_other(other)
        return self._map.__cmp__(other)

    def __eq__(self, other):
        other = DotMap.parse_other(other)
        if not isinstance(other, dict):
            return False
        return self._map.__eq__(other)

    def __ge__(self, other):
        other = DotMap.parse_other(other)
        return self._map.__ge__(other)

    def __gt__(self, other):
        other = DotMap.parse_other(other)
        return self._map.__gt__(other)

    def __le__(self, other):
        other = DotMap.parse_other(other)
        return self._map.__le__(other)

    def __lt__(self, other):
        other = DotMap.parse_other(other)
        return self._map.__lt__(other)

    def __ne__(self, other):
        other = DotMap.parse_other(other)
        return self._map.__ne__(other)

    def __delitem__(self, key):
        return self._map.__delitem__(key)

    def __len__(self):
        return self._map.__len__()

    def clear(self):
        self._map.clear()

    def copy(self):
        return DotMap(self)

    def __copy__(self):
        return self.copy()

    def __deepcopy__(self, memo=None):
        return self.copy()

    def get(self, key, default=None):
        return self._map.get(key, default)

    def has_key(self, key):
        return key in self._map

    def iterkeys(self):
        return self._map.iterkeys()

    def itervalues(self):
        return self._map.itervalues()

    def keys(self):
        return self._map.keys()

    def pop(self, key, default=None):
        return self._map.pop(key, default)

    def popitem(self):
        return self._map.popitem()

    def setdefault(self, key, default=None):
        self._map.setdefault(key, default)

    def update(self, *args, **kwargs):
        if len(args) != 0:
            self._map.update(*args)
        self._map.update(kwargs)

    def viewitems(self):
        return self._map.viewitems()

    def viewkeys(self):
        return self._map.viewkeys()

    def viewvalues(self):
        return self._map.viewvalues()

    @classmethod
    def fromkeys(cls, seq, value=None):
        d = DotMap()
        d._map = OrderedDict.fromkeys(seq, value)
        return d

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)
