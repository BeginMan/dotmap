from collections import OrderedDict
from dotmap import DotMap

# basics
print('\n== basics ==')
d = {
    'a': 1,
    'b': 2,
    'subD': {'c': 3, 'd': 4}
}
dd = DotMap(d)
print(dd)
print(len(dd))
print(dd.copy())
print(dd)
print(OrderedDict.fromkeys([1,2,3]))
print(DotMap.fromkeys([1,2,3], 'a'))
print(dd.get('a'))
print(dd.get('f',33))
print(dd.get('f'))
print(dd.has_key('a'))
dd.update([('rat', 5), ('bum', 4)], dog=7, cat=9)
dd.update({'lol': 1, 'ba': 2})
print(dd)


for k in dd:
    print(k)
print('a' in dd)
print('c' in dd)
dd.c.a = 1
print(dd.toDict())
print(dd.values())
dm = DotMap(name='Steve', job='programmer')
print(dm)
print(issubclass(dm.__class__, dict))
am = DotMap()
am.some.deep.path.cuz.we = 'can'
print(am)
del am.some.deep
print(am)
parentDict = {
    'name': 'Father1',
    'children': [
        {'name': 'Child1'},
        {'name': 'Child2'},
        {'name': 'Child3'},
    ]
}
parent = DotMap(parentDict)
print([x.name for x in parent.children])

# pickle
print('\n== pickle ==')
import pickle
s = pickle.dumps(parent)
d = pickle.loads(s)
print(d)

# init from DotMap
print('\n== init from DotMap ==')
e = DotMap(d)
print(e)

# empty
print('\n== empty() ==')
d = DotMap()
print(d.empty())
d.a = 1
print(d.empty())
print()
x = DotMap({'a': 'b'})
print(x.b.empty())  # True (and creates empty DotMap)
print(x.b)          # DotMap()
print(x.b.empty())  # also True


d = {'sub':{'a':1}}
dm = DotMap(d)
print(dm)
dm.still.works
dm.sub.still.works
print(dm)

dm2 = DotMap(d)
try:
    dm.sub.yes.creation
    print(dm)
    dm2.sub.no.creation
    print(dm)
except KeyError:
    print('KeyError caught')

# _dynamic
print('\n== toDict() ==')
conf = DotMap()
conf.dep = DotMap(
    facts=DotMap(
        operating_systems=DotMap(
            os_CentOS_7=True),
        virtual_data_centers=[
            DotMap(name='vdc1',
                   members=['sp1'],
                   options=DotMap(secret_key='badsecret', description='My First VDC')),
            DotMap(name='vdc2',
                   members=['sp2'],
                   options=DotMap(secret_key='badsecret', description='My Second VDC'))],
        install_node='192.168.2.200',
        replication_group_defaults=DotMap(
            full_replication=False,
            enable_rebalancing=False,
            description='Default replication group description',
            allow_all_namespaces=False),
        node_defaults=DotMap(
            ntp_servers=['192.168.2.2'],
            ecs_root_user='root',
            dns_servers=['192.168.2.2'],
            dns_domain='local',
            ecs_root_pass='badpassword'),
        storage_pools=[DotMap(name='sp1', members=['192.168.2.220'],
                              options=DotMap(ecs_block_devices=['/dev/vdb'],
                                             description='My First SP')),
                       DotMap(name='sp2', members=['192.168.2.221'],
                              options=DotMap(
                                  protected=False,
                                  ecs_block_devices=['/dev/vdb'],
                                  description='My Second SP'))],
        storage_pool_defaults=DotMap(
            cold_storage_enabled=False,
            protected=False,
            ecs_block_devices=['/dev/vdc'],
            description='Default storage pool description'),
        virtual_data_center_defaults=DotMap(
            secret_key='badsecret',
            description='Default virtual data center description'),
        management_clients=['192.168.2.0/24'],
        replication_groups=[DotMap(name='rg1', members=['vdc1', 'vdc2'],
                                   options=DotMap(description='My RG'))]),
    lawyers=DotMap(license_accepted=True))
print(conf.dep.toDict()['facts']['replication_groups'])

# recursive assignment
print('\n== recursive assignment ==')
# dict
d = dict()
d['a'] = 5
print(id(d))
d['recursive'] = d
print(d)
print(d['recursive']['recursive']['recursive'])

# DotMap
m = DotMap()
m.a = 5
print(id(m))
m.recursive = m
print(m.recursive.recursive.recursive)
print(m)
print(m.toDict())

# kwarg
print('\n== kwarg ==')


def test(**kwargs):
    print(kwargs)


class D:
    def keys(self):
        return ['a', 'b']

    def __getitem__(self, key):
        return 0

a = {'1': 'a', '2': 'b'}
b = DotMap(a)
o = OrderedDict(a)
test(**a)
test(**b.toDict())
test(**o)
test(**D())

# ordering
print('\n== ordering ==')
m = DotMap()
m.alpha = 1
m.bravo = 2
m.charlie = 3
m.delta = 4
for k, v in m.items():
    print(k, v)

# subclassing
print('\n== subclassing ==')
d = DotMap()
o = OrderedDict()
print(isinstance(d, dict))
print(isinstance(o, dict))
e = DotMap(m)
print(e)

# deepcopy
print('\n== deepcopy ==')
import copy
t = DotMap()
t.a = 1
t.b = 3
f = copy.deepcopy(t)
t.a = 2
print(t)
print(f)

# copy order preservation
print('\n== copy order preservation ==')
t = DotMap()
t.a = 1
t.b = 2
t.c = 3
copies = []
print(id(t))
for i in range(3):
    copyMap = copy.deepcopy(t)
    copies.append(copyMap)
    print(id(copyMap))


for copyMap in copies:
    for k, v in copyMap.items():
        print(k, v)

# sub-DotMap deepcopy
print('\n== sub-DotMap deepcopy ==')
import copy
l = []
d = {'d1': {'d2': ''}}
m = DotMap(d)

for i in range(3):
    x = copy.deepcopy(m)
    x.d1.d2 = i
    l.append(x)

for m in l:
    print(m)

# tuple toDict
print('\n== DotMap tuple toDict ==')
m = DotMap({'a': 1, 'b': (11, 22, DotMap({'c': 3}))})
d = m.toDict()
print(d)