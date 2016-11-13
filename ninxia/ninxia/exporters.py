#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by steven on 2016/11/13
from scrapy.exporters import CsvItemExporter
from ninxia.items import UserItem


class MyCsvItemExporter(CsvItemExporter):
    def __init__(self, *args, **kwargs):
        kwargs['include_headers_line'] = False
        kwargs['fields_to_export'] = [
            'type',
            'name',
            'name_sub',
            'phone',
            'office_phone',
            'fax',
            'address',
            'contact_name',
            'contact_phone',
            'contact_office_phone',
        ]

        super(MyCsvItemExporter, self).__init__(*args, **kwargs)

    def start_exporting(self):
        fields = UserItem.fields
        row = list(self._build_row((fields[f]['display_name'] for f in self.fields_to_export)))
        self.csv_writer.writerow(row)
