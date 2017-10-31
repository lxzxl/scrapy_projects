#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by steven on 2016/11/13
from scrapy.exporters import CsvItemExporter
from mohurd.items import CompanyItem


class CompExporter(CsvItemExporter):
    def __init__(self, *args, **kwargs):
        kwargs['include_headers_line'] = False
        kwargs['fields_to_export'] = [
            'id',
            'name',
        ]

        super(CompExporter, self).__init__(*args, **kwargs)

    def start_exporting(self):
        self.stream.seek(0)
        self.stream.truncate()
        fields = CompanyItem.fields
        row = list(self._build_row((fields[f]['display_name'] for f in self.fields_to_export)))
        self.csv_writer.writerow(row)
