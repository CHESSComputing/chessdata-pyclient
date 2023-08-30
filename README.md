# chessdata-pyclient
Python library for interacting with the CHESS metadata service

# Installation
1. In an environment of your choosing, run `python setup.py install`
2. Set the environment variable `REQUESTS_CA_BUNDLE` to a path to a CA bundle to use (for SSL).
3. (optional, but recommended) Run `kinit -c ~/krb5_ccache <user>`

# Examples
- Search the CHESS metadata database for records on tomography scans taken at ID3A:
  ```python
  from chessdata import query
  records = query('{"beamline":"3a" "technique":"tomography"}')
  ```
- Submit a new record to the CHESS metadata database from a file, `record.json`, under the `'test'` schema:
  ```python
  from chessdata import insert
  insert('record.json', 'test')
  ```
