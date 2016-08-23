import collections
import os

import requests


GH_BASE = "https://raw.githubusercontent.com/"
TLD_URL = os.path.join(
    GH_BASE,
    "publicsuffix/list/master/public_suffix_list.dat"
)


def get_tlds():
    """Get a list of registerable TLDs."""

    print("Downloading TLD list...")

    return [
        tld.lower() for tld in
        requests.get(TLD_URL).text.splitlines()
        if not tld.startswith("//") and tld
    ]


def get_words():
    """Rip a of common english words from Randall Munroe's website."""

    print("Downloading word list...")

    r = requests.get("http://xkcd.com/simplewriter/words.js")
    return r.text.split('"')[1].split("|")


class DomainFinder(collections.Mapping):
    _tlds = get_tlds()
    _words = get_words()

    def __getitem__(self, ext):
        if ext not in self._tlds:
            raise KeyError(ext)
        else:
            simple_ext = ext.replace(".", "")

            return [w[:-len(simple_ext)] + "." + ext for w in
                    self._words
                    if w.endswith(simple_ext) and w != simple_ext]

    def __iter__(self):
        return iter(self._tlds)

    def __len__(self):
        return len(self._tlds)


domains = DomainFinder()
