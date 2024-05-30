"""Python library for interacting with the CHESS metadata service"""

import json
import os
import requests

# URL = 'https://chessdata.classe.cornell.edu:8243'
URL = 'https://chessdata.classe.cornell.edu:8244'

def get_ticket(file):
    """Return the contents of a file as a byte string.

    :param file: name of a file
    :type file: str
    :return: the contents of `file` as a byte str
    :rtype: str
    """
    file = os.path.expanduser(file)
    with open(file, 'rb') as f:
        contents = f.read()
    return contents

def get_token(ticket):
    """Get the kerberos token from a ticket"""
    # foxden token create read/write
    return 'bla'

def query(query, krb_file='~/krb5_ccache', url=URL):
    """Search the chess metadata database and return matching records
    as JSON
                                                                                                                         
    :param query: query string to look up records
    :type query: str
    :param krb_file: name of a Kerberos 5 credentials (ticket) cache
        file, defults to '~/krb5_ccache'
    :type krb_file: str, optional
    :param url: CHESS metadata server URL, defaults to
        'https://chessdata.classe.cornell.edu:8244'
    :type url: str, optional
    :return: list of matching records
    :rtype: list[dict]
    """
    ticket = get_ticket(krb_file)
    resp = requests.post(
        f'{url}/search',
        data={
            'query': query,
            'name': os.path.basename(krb_file),
            'ticket': ticket,
            'client': 'cli'
        },
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'bearer {get_token(ticket)}'
        }
    )
    return resp.json()

def insert(record, schema, krb_file='~/krb5_ccache', url=URL):
    """Submit a new record to the metadata database.

    :param record: name of a JSON file containing the record to be
        submitted
    :type record: str
    :param schema: name of the schema against which the new record
        will be validated
    :type schema: str
    :param krb_file: name of a Kerberos 5 credentials (ticket) cache
        file, defults to '~/krb5_ccache'
    :type krb_file: str, optional
    :param url: CHESS metadata server URL, defaults to
        'https://chessdata.classe.cornell.edu:8244'
    :type url: str, optional
    :return: response from the CHESS metadata server
    :rtype: requests.Response
    """
    ticket = get_ticket(krb_file)
    resp = requests.post(
        f'{url}/api',
        data={
            'record': get_contents(record),
            'SchemaName': schema,
            'name': os.path.basename(krb_file),
            'ticket': ticket
        },
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'bearer {get_token(ticket)}'
        }
    )
    return resp
