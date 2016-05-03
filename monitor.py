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
        'sessionid': '12872',
        'apikey': 'br8RfjAT7Bto4phxyfN5SKEaAetnmyDd',
        'coreid': '2'
    }
)

if resp.status_code != 200:
    # This means something went wrong.
    raise ApiError('POST GetSessionDetails {}'.format(resp.status_code))

# print resp.json()

with open("form.txt") as f:
# for item in resp.json():
#     # print item.keys()
#     print item['content']
#     print
#     print


    content = f.read()
    # content = item['content']

    m = re.split(u'^[!]{3}.+$', content, flags=re.MULTILINE)
    for i in m:
        # print i

        # Get the key and value of each item
        # TODO Probably have to exclude lines starting with (_) and include
        # (but remove the indicator) (x)
        # kv = re.search(u'^(.+?):(?:\n|\r\n?)\[(.*)\]', i, flags=re.MULTILINE)
        k = re.search(r'^(.+?):', i, flags=re.MULTILINE)
        if k:
            print k.group(1)

            # Look for square bracketed responses. If there are multiple then
            # these are checkboxes
            v = re.findall(r'^\[(.+)\][\b]*(.*)', i, flags=re.MULTILINE)
            if v and len(v) > 1:
                for c in v:
                    print "\tc %s" % c[1].strip()
                    # if c.group(1) != 'left empty':
                    #     print c.group(2)

            elif len(v) == 1:
                if v[0][0].strip() != 'left empty':
                    print "\t%s" % v[0][0].strip()
                else:
                    print '\tNULL'

            else:
                v = re.search(r'^\(x\)[\b]*(.*)', i, flags=re.MULTILINE)
                if v:
                    print '\ts %s' % v.group(1).strip()




        # if kv:
        #     k = kv.group(1).strip()
        #     v = kv.group(2).strip()
        #     print "'%s'='%s'" % (k, v)
