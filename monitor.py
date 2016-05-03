#!/usr/bin/env python

# from omero_basics import OMEROConnectionManager
import requests

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
        'sessionid': '12589',
        'apikey': 'br8RfjAT7Bto4phxyfN5SKEaAetnmyDd',
        'coreid': '2'
    }
)

if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('POST GetSessionDetails {}'.format(resp.status_code))

# print resp.json()

for item in resp.json():
    print item.keys()
    print item['comments']

# for todo_item in resp.json():
#     print('{} {}'.format(todo_item['id'], todo_item['summary']))
