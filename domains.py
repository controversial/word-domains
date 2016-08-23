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


def get_matches():
    """Match TLDs with words to generate domains that look like words."""
    tlds = get_tlds()
    simpletlds = [tld.replace(".", "") for tld in tlds]
    words = get_words()

    print("Generating matches...")

    results = {tld: [] for tld in tlds}

    for i, ext in enumerate(simpletlds):
        matches = [w for w in words if w.endswith(ext) and w != ext]
        for match in matches:
            results[tlds[i]].append(match[:-len(ext)] + "." + tlds[i])
        if results[tlds[i]]:
            print("." + tlds[i], end=" ")

    # Filter out extensions with no results
    return {
        ext: results[ext]
        for ext in results
        if [r for r in results[ext] if r.replace(".", "") != ext]
    }


if __name__ == "__main__":
    matches = get_matches()
