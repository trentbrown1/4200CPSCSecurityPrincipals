#!/usr/bin/python3

# Run me like this:
# $ python3 len_ext_attack.py "http://cpsc4200.mpese.com/uniqname/lengthextension/api?token=...."
# or select "Length Extension" from the VS Code debugger

import sys
from urllib.parse import quote
from pysha256 import sha256, padding


class URL:
    def __init__(self, url: str):
        # prefix is the slice of the URL from "http://" to "token=", inclusive.
        self.prefix = url[:url.find('=') + 1]
        self.token = url[url.find('=') + 1:url.find('&')]
        # suffix starts at the first "command=" and goes to the end of the URL
        self.suffix = url[url.find('&') + 1:]

    def __str__(self) -> str:
        return f'{self.prefix}{self.token}&{self.suffix}'

    def __repr__(self) -> str:
        return f'{type(self).__name__}({str(self).__repr__()})'


def main():
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} URL_TO_EXTEND", file=sys.stderr)
        sys.exit(-1)

    url = URL(sys.argv[1])

    #
    # TODO: Modify the URL
    #
    m = quote(url) # .encode() converts str to bytes
    h1 = sha256()
    h1.update(m)
    padded_message_len = len(m) + len(padding(len(m)))
    h2 = sha256(
    state=bytes.fromhex(h1.hexdigest()),
    count=padded_message_len,
    )
    url.token = 'daa8921e8feb2d610cf0658a50ce532f345b5f1fda9263c9d549e89daffeae9b'
    url.suffix += '&command=UnlockSafes'

    print(url)


if __name__ == '__main__':
    main()
