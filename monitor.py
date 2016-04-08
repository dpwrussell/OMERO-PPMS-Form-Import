#!/usr/bin/env python

from omero_basics import OMEROConnectionManager

conn_manager = OMEROConnectionManager()

# TODO Perhaps exclude datasets that already have the data extracted from the
# PPMS form
q = """
    select dataset.id,
           dataset.name,
           dataset.description
    from Dataset dataset
    """

# Run the query
rows = conn_manager.hql_query(q)

for row in rows:
    print(row)
