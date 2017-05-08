#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by steven on 2016/11/13
from scrapy.exporters import CsvItemExporter
from nasg.items import NasgItem


class MyCsvItemExporter(CsvItemExporter):
    def __init__(self, *args, **kwargs):
        kwargs['include_headers_line'] = False
        kwargs['fields_to_export'] = [
            'name',
            'address',
            'zipcode',
            'contact_name',
            'phone',
            'cert_number',
        ]

        super(MyCsvItemExporter, self).__init__(*args, **kwargs)

    def start_exporting(self):
        fields = NasgItem.fields
        row = list(self._build_row((fields[f]['display_name'] for f in self.fields_to_export)))
        self.csv_writer.writerow(row)
