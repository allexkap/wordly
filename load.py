import os
import subprocess
import sys

url = 'https://www.opencorpora.org/files/export/dict/dict.opcorpora.txt.bz2'
cache_filename = 'dict.opcorpora.txt.bz2'
filename = 'five.txt'


def parse(block: str) -> str:
    word, _, info = block.split('\n')[1].partition('\t')
    if (
        any(info.startswith(part) for part in ('NOUN', 'INFN', 'NUMR'))
        and all(
            prop not in info
            for prop in ('Abbr', 'Name', 'Surn', 'Patr', 'Geox', 'Orgn', 'Trad')
        )
        and len(word) == 5
        and word.isalpha()
    ):
        return word.lower()
    return ''


if len(sys.argv) != 1 or not os.path.exists(cache_filename):
    import requests

    response = requests.get(url)
    assert response.status_code == 200
    content = response.content
    with open(cache_filename, 'wb') as file:
        file.write(content)
else:
    with open(cache_filename, 'rb') as file:
        content = file.read()

extracted_content = subprocess.run(
    ('bzcat'),
    input=content,
    stdout=subprocess.PIPE,
    check=True,
).stdout.decode()


words = set(map(parse, extracted_content.strip().split('\n\n'))) - {''}

with open(filename, 'w') as file:
    file.write('\n'.join(words))

print('words:', len(words))
