import copy
import json
import os
import shutil

import dataset
import yaml

from cleaner import DataReader

db = dataset.connect('sqlite:///:memory:')

def load_data(key, state_name_field=None):
    def attach_state_code(d, name_field=state_name_field):
        if name_field is not None:
            state_name = d[name_field]
            node = db['alias'].find_one(name=state_name)
            code = None
            if node:
                code = node['code']
            d['state_code'] = code
        return d

    reader = DataReader(key=key, prepfunction=attach_state_code)
    table = db[key]
    for row in reader.data:
        table.insert(row)
    return table

MAPTABLES = {
    'states': 'state_or_union_territory',
    'area': 'state_territory',
    'population': 'state_or_union_territory',
    'hiv_awareness': 'state',
    'hdi': 'state_union_territory'
}

def load_tables(table=None):
    if table is not None:
        load_data(table)
    else:
        load_data('alias')
        load_data('state_codes')
        for k, v in MAPTABLES.items():
            load_data(k, state_name_field=v)

def export_tables():
    BUILD_DIR = '../static/json'
    try:
        shutil.rmtree(BUILD_DIR)
    except FileNotFoundError:
        pass

    os.makedirs(BUILD_DIR)

    states = db['state_codes'].all()
    states = list(states)
    with open('{}/states.json'.format(BUILD_DIR), 'w') as f:
        json.dump(states, f)

    for state in states:
        print("Preparing {}".format(state['code']))
        fname = "{}.json".format(state['code'].lower())
        d = copy.deepcopy(state)
        for metrics in MAPTABLES.keys():
            _metrics = db[metrics].find_one(state_code=state['code'])
            if _metrics:
                for k in ['id', 'state_code', MAPTABLES[metrics]]:
                    if k in _metrics:
                        del _metrics[k]
            d[metrics] = _metrics
        with open('{}/{}'.format(BUILD_DIR, fname), 'w') as f:
            json.dump(d, f)


def check_table_linking(tablename):
    for i in db[tablename].all():
        if i['state_code'] == None:
            print(i)

if __name__ == '__main__':
    load_tables()
    export_tables()
