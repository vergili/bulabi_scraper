from scrapy.conf import settings
from scrapy.contrib.exporter import CsvItemExporter
import csv


class CSVPipeline(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        delimiter = settings.get('CSV_DELIMITER', ',')
        quotechar = settings.get('CSV_QUOTECHAR', '"')
        escapechar = settings.get('CSV_ESCAPECHAR', '\\')
        doublequote = False
        quoting = csv.QUOTE_MINIMAL

        kwargs['delimiter'] = delimiter
        kwargs['quotechar'] = quotechar
        kwargs['escapechar'] = escapechar
        kwargs['doublequote'] = doublequote
        kwargs['quoting'] = quoting

        super(CSVPipeline, self).__init__(*args, **kwargs)

