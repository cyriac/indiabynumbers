import csv

from slugify import slugify

class DataReader(object):
    RAW_DATA_FOLDER = 'csv'
    key = None
    prepfunction = None

    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def get_data_from_csv(self):
        with open('{}/{}.csv'.format(self.RAW_DATA_FOLDER, self.key)) as f:
            reader = csv.DictReader(f)
            for row in reader:
                d = {}
                for key, value in row.items():
                    key_slug = slugify(key, to_lower=True, separator='_')       # Optimize
                    key_slug = '_id' if key_slug == 'id' else key_slug
                    d[key_slug] = value
                if self.prepfunction:
                    d = self.prepfunction(d)
                yield d

    @property
    def data(self):
        if self.key:
            value = self.get_data_from_csv()
        else:
            value = []
        return value
