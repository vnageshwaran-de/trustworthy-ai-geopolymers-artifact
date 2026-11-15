"""Deterministic keyword-heuristic classifier for the geopolymer-AI review corpus.

Usage: python3 keyword_classifier.py <scopus_export.csv> <extraction_master.csv> <out.csv> [supplementary_abstracts.csv] [excluded_records.csv]

Reads the lexicon from lexicon.json beside this script. For every record in extraction_master.csv it
matches the lexicon (case-insensitive substring matching) against title + abstract + author keywords +
index keywords taken from the Scopus export (joined on EID), and writes one row of codes per record.
Records that are not in the Scopus export take their abstract from the optional supplementary file
(id, doi, source, abstract; see fetch_supplementary_abstracts.py). Records with no abstract from either
source are coded from the title alone and flagged needs_human_verification=Y. Records listed in the optional
exclusions file (id, reason) are still coded but carry status=excluded and are left out of all statistics.
Same inputs always give the same output; no language model is involved.
"""
import csv, json, os, sys
csv.field_size_limit(10**9)

def load(path):
    with open(path, encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def classify(text, lex):
    t = ' ' + text.lower() + ' '
    hit = lambda terms: any(k in t for k in terms)
    m = [lab for lab, terms in lex['M_material'].items() if hit(terms)]
    if 'fly-ash' in m and 'slag' in m:
        m = ['FA-slag'] + [x for x in m if x not in ('fly-ash', 'slag')]
    if not m:
        m = ['mixed/other-AAM']
    task = lex['T_default']
    for lab, terms in lex['T_task_priority']:
        if hit(terms):
            task = lab
            break
    if hit(lex['P_physics']['III+ (claimed or candidate)']):
        p = 'III+flag'
    elif hit(lex['P_physics']['II']):
        p = 'II'
    else:
        p = 'I'
    e = [lab for lab, terms in lex['E_env'].items() if hit(terms)] or ['none-explicit']
    tr = [lab for lab, terms in lex['trust'].items() if hit(terms)] or ['none-detected']
    return ';'.join(m), task, p, ';'.join(e), ';'.join(tr)

def main(scopus, master, out, supp=None, excl=None):
    lex = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lexicon.json'), encoding='utf-8'))
    sc = {r['EID']: r for r in load(scopus)}
    sup = {r['id']: r for r in load(supp)} if supp else {}
    ex = {r['id']: r['reason'] for r in load(excl)} if excl else {}
    rows = []
    for r in load(master):
        s = sc.get(r['id'])
        if s and len(s.get('Abstract', '')) > 100:
            text = ' '.join([s['Title'], s['Abstract'], s.get('Author Keywords', ''), s.get('Index Keywords', '')])
            depth, flag = 'title+abstract+keywords', 'N'
        elif len(sup.get(r['id'], {}).get('abstract', '')) > 100:
            text, depth, flag = r['title'] + ' ' + sup[r['id']]['abstract'], 'title+abstract (supplementary source)', 'N'
        else:
            text, depth, flag = r['title'], 'title-only', 'Y'
        m, t, p, e, tr = classify(text, lex)
        rows.append({'id': r['id'], 'doi': r['doi'], 'year': r['year'], 'duplicate_of': r.get('duplicate_of', ''),
                     'M_material': m, 'T_task': t, 'P_physics': p, 'E_env': e, 'trust_flags': tr,
                     'coding_depth': depth, 'classification_method': 'keyword_heuristic',
                     'needs_human_verification': flag,
                     'status': 'excluded: ' + ex[r['id']] if r['id'] in ex else 'included'})
    with open(out, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f'{len(rows)} records coded; {sum(r["needs_human_verification"]=="Y" for r in rows)} title-only')

if __name__ == '__main__':
    main(*sys.argv[1:6])
