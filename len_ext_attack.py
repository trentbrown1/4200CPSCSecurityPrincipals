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
    print(url.token)
    print(url.suffix)

    orig_msg = url.suffix.encode()
    orig_len = len(orig_msg)

    padded_message_len = orig_msg + padding(orig_len)

    h1 = sha256(state=bytes.fromhex(url.token),count=len(padded_message_len))
    
    x = quote("command=UnlocksSafes")
    h1.update(x.encode())
    # print(h2.hexdigest())
    newToken = h1.hexdigest()
    url.token = newToken # + padding and suffix?
    url.suffix += x

    print(newToken)
    print(url)


if __name__ == '__main__':
    main()
