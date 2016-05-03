#!/usr/bin/env python

# from omero_basics import OMEROConnectionManager
import requests
import re

# conn_manager = OMEROConnectionManager()
#
# # TODO Perhaps exclude datasets that already have the data extracted from the
# # PPMS form
# q = """
#     select dataset.id,
#            dataset.name,
#            dataset.description
#     from Dataset dataset
#     """
#
# # Run the query
# rows = conn_manager.hql_query(q)
#
# for row in rows:
#     print(row)

# curl -d "action=GetSessionDetails&sessionid=12589&apikey=br8RfjAT7Bto4phxyfN5SKEaAetnmyDd&coreid=2" https://ppms.us/hms-lsp/API2/
# curl -d "action=GetBookingFormContent&sessionid=12589&apikey=br8RfjAT7Bto4phxyfN5SKEaAetnmyDd&coreid=2" https://ppms.us/hms-lsp/API2/

# resp = requests.post(
#     'https://ppms.us/hms-lsp/API2/',
#     {
#         'action': 'GetSessionDetails',
#         'sessionid': '12589',
#         'apikey': 'br8RfjAT7Bto4phxyfN5SKEaAetnmyDd',
#         'coreid': '2'
#     }
# )

resp = requests.post(
    'https://ppms.us/hms-lsp/API2/',
    {
        'action': 'GetBookingFormContent',
        'sessionid': '12871',
        'apikey': 'br8RfjAT7Bto4phxyfN5SKEaAetnmyDd',
        'coreid': '2'
    }
)

if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('POST GetSessionDetails {}'.format(resp.status_code))

# print resp.json()

for item in resp.json():
    # print item.keys()
    print item['content']
    print
    print

    m = re.split(u'^[!]{3}.+$', item['content'], flags=re.MULTILINE)
    for i in m:
        # print i

        # Get the key and value of each item
        # TODO Probably have to exclude lines starting with (_) and include
        # (but remove the indicator) (x)
        # kv = re.search(u'^(.+?):(?:\n|\r\n?)\[(.*)\]', i, flags=re.MULTILINE)
        k = re.search(r'^(.+?):', i, flags=re.MULTILINE)
        if k:
            print k.group(1)

        v = re.search(r'^\[(.+)\]', i, flags=re.MULTILINE)
        if v:
            print v.group(1)

        # If there is no corresponding value for this, instead look for radio
        # or checkbox syntax. they are the same so we must find all instances
        # of (x)
        else:
            vs = re.findall(r'^\(x\)(.*)', i, flags=re.MULTILINE)
            if vs:
                for v in vs:
                    print v.group(1)
        # if kv:
        #     k = kv.group(1).strip()
        #     v = kv.group(2).strip()
        #     print "'%s'='%s'" % (k, v)
