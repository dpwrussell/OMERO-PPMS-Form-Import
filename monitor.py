#!/usr/bin/env python

from omero_basics import OMEROConnectionManager
import omero
import requests
import re

conn_manager = OMEROConnectionManager()

# TODO Perhaps exclude datasets that already have the data extracted from the
# PPMS form. How do we know which ones are already processed?
q = """
    SELECT dataset.id, anno
    FROM Dataset dataset
    JOIN dataset.annotationLinks links
    JOIN links.child anno
    JOIN anno.mapValue mapValues
    WHERE anno.class = MapAnnotation
    AND mapValues.name = 'dpwrkey'
    """
    # WHERE dataset.description LIKE '%Session #%'
    # JOIN anno.annotationLinks anno2
# Run the query
rows = conn_manager.hql_query(q)

for row in rows:
    dataset_id = row[0]
    anno = row[1]
    print('Dataset %i' % dataset_id)
    for pair in anno.getMapValue():
        print '\t%s = %s' % (pair.name, pair.value)

    # datasetId = row[0]
    # sessionId = re.search(r'Session #([0-9]*)', row[1])
    # print sessionId.group(1)
exit(1)
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

    pairs = []

    m = re.split(u'^[!]{3}.+$', content, flags=re.MULTILINE)
    for i in m:


        # print i

        # Get the key and value of each item
        # TODO Probably have to exclude lines starting with (_) and include
        # (but remove the indicator) (x)
        # kv = re.search(u'^(.+?):(?:\n|\r\n?)\[(.*)\]', i, flags=re.MULTILINE)
        k = re.search(r'^(.+?):', i, flags=re.MULTILINE)
        if k:
            # print k.group(1)
            key = k.group(1)

            # Look for square bracketed responses. If there are multiple then
            # these are checkboxes
            v = re.findall(r'^\[(.+)\][\b]*(.*)', i, flags=re.MULTILINE)
            if v and len(v) > 1:
                for c in v:
                    if c[0] == 'x':
                        # print "\tc %s" % c[1].strip()
                        value = c[1].strip()
                        pairs.append([key, value])

            elif len(v) == 1:
                if v[0][0].strip() != 'left empty':
                    # print "\t%s" % v[0][0].strip()
                    value = v[0][0].strip()
                    pairs.append([key, value])
                # else:
                    # print '\tEmpty'

            else:
                v = re.search(r'^\(x\)[\b]*(.*)', i, flags=re.MULTILINE)
                if v:
                    # print '\ts %s' % v.group(1).strip()
                    value = v.group(1).strip()
                    pairs.append([key, value])

    for pair in pairs:
        print pair

    conn = conn_manager.connect()
    conn.SERVICE_OPTS.setOmeroGroup(53)
    mapAnn = omero.gateway.MapAnnotationWrapper(conn)
    # Use 'client' namespace to allow editing in Insight & web
    namespace = omero.constants.metadata.NSCLIENTMAPANNOTATION
    mapAnn.setNs(namespace)
    mapAnn.setValue(pairs)
    mapAnn.save()
    dataset = conn.getObject("Dataset", 151)
    # NB: only link a client map annotation to a single object
    dataset.linkAnnotation(mapAnn)

        # if kv:
        #     k = kv.group(1).strip()
        #     v = kv.group(2).strip()
        #     print "'%s'='%s'" % (k, v)
