# requires
# pip install airtable
# pip install airtable-python-wrapper

import json
import airtable
from airtable import Airtable

BASE_ID = "app38cZA2uPDxdTL8" # found in url of API documentation for table
TABLE_NAME = "Services"

def airtable_call():
    airtable = Airtable(BASE_ID, TABLE_NAME)
    records = airtable.get_all()

    service_list = []
    for record in records:
        od = {} # Original Dictionary
        od['icons'] = []
        try:
            od['id'] = record['fields']['ID']
        except KeyError:
            continue # every record needs an ID, skip if there is not one
        try:
            od['name'] = record['fields']['Name']
        except KeyError:
            pass
        try:
            od['desc'] = record['fields']['Desc']
        except KeyError:
            pass
        try:
            for index, record_id in enumerate(record['fields']['Icons']):
                record = airtable.get(record_id)
                od['icons'].append({
                    "text" : "",
                    "icon" : ""
                })
                try:
                    od['icons'][index]['text'] = record['fields']['text']
                except KeyError:
                    pass
                try:
                    od['icons'][index]['icon'] = record['fields']['icon']
                except KeyError:
                    pass
        except KeyError:
            pass
        if od['icons'] == []:
            del od['icons']

        service_list.append(od)

    with open("output.json", "w") as f:
        json.dump(service_list, f, indent=2)

    return service_list