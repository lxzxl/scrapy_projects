# -*- coding: utf-8 -*-
from scrapy.exporters import CsvItemExporter
from .items import CompanyItem


class MyCsvItemExporter(CsvItemExporter):
    def __init__(self, *args, **kwargs):
        kwargs['include_headers_line'] = False
        kwargs['fields_to_export'] = [
            'area',
            'name',
            'domains',
            'address',
            'contact',
            'phone'
        ]

        super(MyCsvItemExporter, self).__init__(*args, **kwargs)

    def start_exporting(self):
        self.stream.seek(0)
        self.stream.truncate()
        fields = CompanyItem.fields
        row = list(self._build_row((fields[f]['display_name'] for f in self.fields_to_export)))
        self.csv_writer.writerow(row)
