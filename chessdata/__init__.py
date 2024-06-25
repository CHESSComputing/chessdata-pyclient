"""Python library for interacting with the CHESS metadata service"""

import json
import os
import requests
import warnings

URL = 'https://foxden-meta.classe.cornell.edu:8300'


def get_token(ticket):
    """Get a foxden read token from a kerberos ticket.

    :param ticket: The name of a file containing a kerberos ticket, OR
        the name of an environment variable containing the ticket
        string, OR the ticket string.
    :type ticket: string
    :returns: Kerberos token
    :rtype string
    """
    if str(ticket) in os.environ:
        return os.environ[ticket]

    ticket_file = os.path.expanduser(ticket)
    if os.path.isfile(ticket_file):
        from re import search
        foxden_create_cmd = f'foxden token create read --kfile={ticket_file}'
        with os.popen(foxden_create_cmd, 'r') as pipe:
            out = pipe.read()
        if not len(out) == 0:
            token = search(r'(?P<token>[\S]+)').groups('token')
        else:
            foxden_view_cmd = f'foxden token view'
            with os.popen(foxden_view_cmd, 'r') as pipe:
                out = pipe.read()
            token = search(r'AccessToken  :  (?P<token>[\S]+)',
                           out).groups('token')[0]
        return token
    else:
        # `ticket` is the ACTUAL ticket string
        raise NotImplementedError


def query(query, ticket='~/krb5_ccache', krb_file=None, url=URL):
    """Search the chess metadata database and return matching records
    as JSON

    :param query: query string to look up records
    :type query: str
    :param ticket:
    :type ticket:
    :param ticket: The name of a file containing a kerberos ticket, OR
        the name of an environment variable containing the ticket
        string, OR the ticket string. Used to obtain a foxden read
        token. Defults to '~/krb5_ccache'
    :type ticket: string
    :param krb_file: Deprecatued, use the `ticket` parameter
        instead. Name of a Kerberos 5 credentials (ticket) cache
        file. Defaults to None.
    :type krb_file: str, optional
    :param url: CHESS metadata server URL, defaults to
        'https://chessdata.classe.cornell.edu:8244'
    :type url: str, optional
    :return: list of matching records
    :rtype: list[dict]
    """
    if krb_file is not None:
        warnings.warn(
            'Use of "krb_file" kwarg is deprecated; use "ticket" kwarg instead.',
            DeprecationWarning)
        ticket = krb_file

    resp = requests.post(
        f'{url}/search',
        data=json.dumps(
            {
                'service_query':
                {
                    'query': query
                }
            }
        ),
        headers={
            'Authorization': f'bearer {get_token(ticket)}'
        }
    )
    return resp.json()
