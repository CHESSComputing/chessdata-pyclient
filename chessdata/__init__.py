"""Python library for interacting with the CHESS metadata service"""

import os
import requests

VERSION = '0.0.0'

# URL = 'https://chessdata.classe.cornell.edu:8243'
URL = 'https://chessdata.classe.cornell.edu:8244'

def get_ticket(krb_file):
    """Return the contents of a Kerberos 5 credentials (ticket) cache file

    :param krb_file: name of a Kerberos 5 credentials (ticket) cache file
    :type krb_file: str
    :return: the contents of `krb_file` as a byte str
    :rtype: str
    """
    krb_file = os.path.expanduser(krb_file)
    with open(krb_file, 'rb') as kf:
        ticket = kf.read()
    return ticket

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
    resp = requests.post(
        f'{url}/search',
        data={
            'query': query,
            'name': os.path.basename(krb_file),
            'ticket': get_ticket(krb_file),
            'client': 'cli'
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )
    return resp.json()
