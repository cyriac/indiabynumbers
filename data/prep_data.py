import copy
import json
import os
import shutil

import dataset
import yaml

from halo import Halo

from cleaner import DataReader


MAPTABLES = yaml.load(open('config.yml'))
BUILD_DIR = '../static/json'
DB = dataset.connect('sqlite:///:memory:')

def load_data(key, state_name_field=None):
    def attach_state_code(d, name_field=state_name_field):
        if name_field is not None:
            state_name = d[name_field]
            node = DB['alias'].find_one(name=state_name)
            code = None
            if node:
                code = node['code']
            d['state_code'] = code
        return d

    reader = DataReader(key=key, prepfunction=attach_state_code)
    table = DB[key]
    for row in reader.data:
        table.insert(row)
    return table

def load_csvs(table=None):
    if table is not None:
        load_data(table)
    else:
        load_data('alias')
        load_data('state_codes')

        spinner = Halo({'text': 'Loading', 'spinner': 'dots'})
        spinner.start()

        for k, v in MAPTABLES.items():
            spinner.text = "Loading {}".format(k)
            load_data(k, state_name_field=v)

        spinner.succeed("Load complete")

def export_state_data():
    try:
        shutil.rmtree(BUILD_DIR)
    except FileNotFoundError:
        pass

    os.makedirs(BUILD_DIR)
    os.makedirs("{}/states_level".format(BUILD_DIR))
    os.makedirs("{}/metrics_level".format(BUILD_DIR))

    states = DB['state_codes'].all()
    states = list(states)

    spinner = Halo({'text': 'Exporting state data', 'spinner': 'dots'})
    spinner.start()

    with open('{}/states_level/states.json'.format(BUILD_DIR), 'w') as f:
        msg = "Exporting {}".format("states")
        json.dump(states, f)

    for state in states:
        msg = "Exporting {}".format(state['code'])
        spinner.text = msg
        fname = "{}.json".format(state['code'].lower())
        d = copy.deepcopy(state)
        for metrics in MAPTABLES.keys():
            _metrics = DB[metrics].find_one(state_code=state['code'])
            if _metrics:
                for k in ['id', 'state_code', MAPTABLES[metrics]]:
                    if k in _metrics:
                        del _metrics[k]
            d[metrics] = _metrics
        with open('{}/states_level/{}'.format(BUILD_DIR, fname), 'w') as f:
            json.dump(d, f)

    spinner.succeed("Export state data complete")

def export_metrics_data():
    spinner = Halo({'text': 'Exporting metrics data', 'spinner': 'dots'})
    spinner.start()

    metrickeys = []
    for metrics in MAPTABLES.keys():
        if metrics == 'states':
            continue
        metrickeys.append(metrics)
        msg = "Exporting {} metrics".format(metrics)
        metrics_data = []
        for m in DB[metrics].all():
            m['state_data'] = DB['states'].find_one(state_code=m['state_code'])
            metrics_data.append(m)
        with open('{}/metrics_level/{}.json'.format(BUILD_DIR, metrics), 'w') as f:
            json.dump(metrics_data, f)

    with open('{}/metrics_level/metrics_list.json'.format(BUILD_DIR), 'w') as f:
        msg = "Exporting metrics list"
        json.dump(metrickeys, f)

    spinner.succeed("Export metrics data complete")

def _check_table_linking(tablename):
    for i in DB[tablename].all():
        if i['state_code'] == None:
            yield i

def check_table_linking():
    for metrics in MAPTABLES.keys():
        missing_links = list(_check_table_linking(metrics))
        if len(missing_links) > 0:
            print("\nMissing links in {}".format(metrics))
            for i in missing_links:
                print(i)


if __name__ == '__main__':
    load_csvs()
    export_state_data()
    export_metrics_data()
    check_table_linking()
