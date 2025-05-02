"""Utilities for generating provenance records for raw datasets."""

from chessdata import query

def make_provenance_record(
        did,
        input_files=None,
        metadata_url='https://foxden-meta.classe.cornell.edu:8300',
        specscans_url='https://foxden-scans.classe.cornell.edu:8390'):
    """Return a provenance record for the raw dataset with `did`
    provided.

    :param did: DID of raw dataset.
    :type did: str
    :param input_files: Value to use for `input_files` field of
        provenance record, defaults to `None`.
    :type input_files: list[str], optional
    :param metadata_url: URL of metadata service, defaults to
        `'https://foxden-meta.classe.cornell.edu:8300'`.
    :type metadata_url: str, optional
    :param specscans_url: URL of specscans service, defaults to
        `'https://foxden-scans.classe.cornell.edu:8390'`.
    :type specscans_url: str, optional
    :return: Provenance record.
    :rtype: dict[str, object]
    """
    from functools import cmp_to_key
    import os

    _query = f'{{"did": "{did}"}}'

    # Get metadata record for this DID
    try:
        metadata = query(_query, url=metadata_url)[0]
    except Exception as exc:
        raise RuntimeError(
            f'Cannot get metadata record for did {did}') from exc
    
    # Get output_files field for prv record from data_location_raw
    # field of meta record
    try:
        #output_files = os.listdir(metadata['data_location_raw'])
        output_files = list_files(metadata['data_location_raw'])
    except Exception as exc:
        raise RuntimeError(
            f'Cannot get list of output files for did {did}') from exc

    # Get spec scan records for this DID and get scripts field for
    # prov record from spec_command field of spec scans records
    try:
        scans = query(_query, url=specscans_url)
    except Exception as exc:
        raise RuntimeError(
            f'Cannot get spec scan records for did {did}') from exc
    def order_scans(scan1, scan2):
        return (scan1['start_time'] < scan2['start_time'])
    scans = sorted(scans, key=cmp_to_key(order_scans))
    scripts = []
    for i, scan in enumerate(scans):
        command = scan['command'].split(' ' , 1)
        if len(command) == 2:
            name = command[0]
            options = command[1]
        else:
            name = scan['command']
            options = ''
        scripts.append({'name': name, 'options': options, 'order_idx': i})

    if input_files is None:
        input_files = []
        
    prov = {
        'did': did,
        'input_files': input_files,
        'output_files': output_files,
        'scripts': scripts,
        'site': 'CHESS',
        'osinfo': osinfo(),
    }

    return prov

def osinfo():
    """
    Helper function to provide osinfo
    """
    import platform
    os_info = {
        "name": platform.system().lower() + "-" + platform.release(),
        "kernel": platform.version(),
        "version": platform.platform()
    }
    return os_info

def list_files(directory):
    """
    Helper function to list all files underneath a directory
    """
    import os
    files = []
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(dirpath, filename))
    return files
