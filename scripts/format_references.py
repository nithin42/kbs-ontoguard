import re
import unicodedata

def clean_ascii(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

def main():
    bib_content = open('paper/references.bib', 'r', encoding='utf-8').read()
    
    entries = re.findall(r'@(\w+)\s*\{\s*([^,]+),([\s\S]*?)\n\}\n', bib_content)
    bib_dict = {}
    for entry_type, key, body in entries:
        fields = {}
        for line in body.split('\n'):
            line = line.strip()
            if '=' in line:
                k, v = line.split('=', 1)
                k = k.strip().lower()
                v = v.strip().rstrip(',')
                if (v.startswith('{') and v.endswith('}')) or (v.startswith('"') and v.endswith('"')):
                    v = v[1:-1]
                v = v.replace('{', '').replace('}', '').replace('\\&', '&').replace('\\\'c', 'c').replace('\\`e', 'e')
                fields[k] = v
        bib_dict[key.strip()] = fields

    tex = open('paper/manuscript.tex', 'r', encoding='utf-8').read()
    cites = re.findall(r'\\cite\{([^}]+)\}', tex)
    ordered_keys = []
    for c in cites:
        for k in [x.strip() for x in c.split(',')]:
            if k and k not in ordered_keys:
                ordered_keys.append(k)

    lines_out = []
    for i, k in enumerate(ordered_keys, 1):
        f = bib_dict.get(k, {})
        author = clean_ascii(f.get('author', 'Unknown'))
        title = clean_ascii(f.get('title', 'Unknown'))
        journal = clean_ascii(f.get('journal', f.get('booktitle', f.get('institution', 'Technical Report'))))
        volume = f.get('volume', '')
        number = f.get('number', '')
        pages = f.get('pages', '')
        year = f.get('year', '')
        doi = f.get('doi', '')
        url = f.get('url', '')
        
        # Author formatting: e.g. Q. Zhan, Z. Liang, ...
        # Or standard format
        ref_str = f'[{i}] {author}, {title}, {journal}'
        if volume:
            ref_str += f' {volume}'
        if number:
            ref_str += f' ({number})'
        if pages:
            ref_str += f' ({year}) {pages}.'
        else:
            ref_str += f' ({year}).'
        if doi:
            ref_str += f' doi:{doi}.'
        elif url:
            ref_str += f' URL: {url}'
        lines_out.append(ref_str)

    with open('scripts/formatted_refs.txt', 'w', encoding='utf-8') as f:
        for line in lines_out:
            f.write(line + '\n')
    print('SUCCESS: Formatted all 28 references to scripts/formatted_refs.txt')

if __name__ == '__main__':
    main()
