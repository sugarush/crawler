import re

from cgi import escape
from xml.etree.ElementTree import fromstring

from util import check_pipeline, MongoDBPipeline

from pprint import pprint


def get_stamp(meta):
    return '{congress}/{session}/{type}/{number}/{format}'.format(**meta)


class Bill(MongoDBPipeline):

    def initialize(self):
        collection = self.settings.get('mongodb_collection', 'bill')

        self.collection = self.db.get_collection(collection)
        self.duplicates = self.db.get_collection(collection + '_duplicates')

    @check_pipeline
    def process_item(self, item, spider):
        data = self.to_json.data(fromstring(item['xml'].replace('&', '&amp;')))

        _data = data.get('resolution')

        if not _data:
            _data = data.get('bill')

        if not _data:
            _data = data.get('amendment-doc')

        metadata = _data.get('metadata')
        if metadata:
            del(metadata['dublinCore'])

        data['url'] = item['url']
        data['meta'] = item['meta']
        data['stamp'] = get_stamp(item['meta'])

        existing = self.collection.find_one({ 'stamp': data['stamp'] })

        if existing:
            if self.settings['mongodb_ignore_duplicate']:
                return None
            self.duplicates.insert_one(data)
            self.stats.inc_value('duplicate')
            return None

        self.collection.insert_one(data)
        self.stats.inc_value('processed')
        return data
