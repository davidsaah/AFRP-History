# -*- coding: utf-8 -*-
"""The two register transliterations John Mogannam made from the Ottoman
   defters, encoded so they can be counted rather than admired.

   Source: John Mogannam, The Ramallah Family Tree Book, ch. 4 —
     · Chart 1: facsimile, Register 289 cols. 79–80, Bayt Jālā, 961 AH / 1553–54
     · Chart 2: his English transliteration of the 36 names in it
     · Chart 3: facsimile, Register 516, Ramallah, 970 AH / 1562–63
     · Chart 4: his English transliteration — 10 Muslim households, then
       63 Christian households and 8 bachelors

   Cells are stored exactly as he wrote them, query marks and all. Where he
   offered alternative readings the alternatives are kept in `alt`.
"""

# ── 1553–54 · Bayt Jālā · the group the register calls al-Kasābra ──────
# 36 households, laid out five to a row as in his table.
BAYT_JALA_1553 = [
    ('Kaʿoosh', 'Zayed'), ('Suweidan', 'Khaleel'), ('ʿAdawi', 'Hassaan'),
    ('Nuh', 'Hassaan'), ('Ibrahim', 'Hassaan'),
    ('Jareer', 'Hadeed'), ('Hadeed / Marrah? / Jarrah?', 'waʾn?'), ('Khaleel', 'Saʿid?'),
    ('Makhlouf', 'ʿAwad'), ('Rahal', 'ʿAwad'),
    ('Ibrahim', 'Zraik'), ('ʿAmeera', 'Hassaan'), ('Musa', 'Baraka'),
    ('Musa', 'Braik'), ('Attallah', 'Badr'),
    ('Najm', 'Bilal'), ('Bilal', 'Nuh'), ('Farah', 'Suweid'),
    ('Saleh', 'Shibl'), ('Hassaan', 'Nuh'),
    ('Ghneim', 'Salem'), ('Salem', 'Marrah'), ('Khaleel', 'ʿAwad'),
    ('Musa', 'Musa'), ('Marah', 'Bilal'),
    ('Saʿid', 'Sinar? / Sitar?'), ('Khaleel', 'Sadaqa'), ('Farah', 'Salem'),
    ('Rizek', 'Salem'), ('Marah', 'Salem'),
    ('ʿOmar', 'Hassaan'), ('Ishaq', 'Yaʿcoub'), ('Rayan? / Dheyab?', 'Khaleel'),
    ('Ibrahim', 'Khaleel'), ('Nuh', 'Khadr?'),
    ('Waʾel? / Dagher?', 'Hassaan'),
]

# ── 1562–63 · Ramallah · the ten Muslim households already on the hill ──
RAMALLAH_1562_MUSLIM = [
    ('Khaleel', 'Hassaan'), ('—?', 'Hasan'), ('ʿAmeer', 'ʿOmar'),
    ('ʿAmeer?', 'Hasan'), ('—?', 'Hasan'), ('Hasan', 'ʿAta'),
    ('Ahmad', 'Muhammad'),
    ('Jamal?', 'Ahmad?'), ('Rasha?', 'Hasan'), ('—?', 'Muhammad'),
]

# ── 1562–63 · Ramallah · the Christian community ──────────────────────
# 63 households and 8 bachelors. `b` marks the ones he flagged "bach."
RAMALLAH_1562_CHRISTIAN = [
    ('Ishaq', 'Yaʿcoub', 0), ('ʿAmeera', 'Hassaan', 0), ('ʿAyash', 'ʿAudi', 0),
    ('ʿOmran', 'Hassaan', 0), ('Jareer', 'Hadeed', 0),
    ('Abdallah', 'Medralady? / Malrlady?', 0), ('Musa', '—?', 0),

    ('Ibrahim', 'Yaʿcoub', 0), ('Farah', 'Suweid', 0), ('Ghneim', 'Hadeed', 0),
    ('Musa', 'Braik', 0), ('Salem', 'Haras?', 0), ('ʿAdnan', 'Khaleel', 0),
    ('Ibrahim', 'Khaleel', 0),

    ('Ghanayem', 'Hadeed', 0), ('Yaʿcoub', 'Ishaq', 0), ('Muʿammar', 'ʿAmeera', 0),
    ('Saleh', 'Musa', 0), ('Dheeb', 'Jirius?', 0), ('ʿAmer', 'Rizkallah', 0),
    ('ʿEsa', 'Musa', 0),

    ('Mansur', 'Salem', 0), ('Darraʿ', 'Salem', 0), ('Naser', 'Salem', 0),
    ('Farah', 'Salem', 0), ('Salem', 'Saʿid?', 0), ('Ghneim', 'Salem', 0),
    ('Ghanem', 'Ghanayem', 0),

    ('Saʿid', 'Sinar? / Sitar?', 0), ('Nuh', 'Khadr', 0), ('Khaleel', 'Sadaqa', 0),
    ('Yuwad? / Nuwar?', 'Masʿood', 0), ('Ibrahim', 'Saʿid', 0), ('Khaleel', 'Saʿid', 0),
    ('Naseer', 'Salem', 0),

    ('Khaleel', 'Ibrahim', 0), ('Saʿid', 'Ibrahim', 0), ('Suleiman', 'Suleiman', 0),
    ('Ghannam', 'Ghneim', 0), ('Muʿammar', 'Nuh', 0), ('Hashem?', 'Saʿda?', 0),
    ('Ibrahim', 'Hasan?', 0),

    ('Marah', 'Hilal', 0), ('Najm', 'Hilal', 0), ('Khaleel', 'Hassaan', 0),
    ('—?', 'Hassaan', 0), ('Nuh', 'Hassaan', 0), ('Hassaan', 'Nuh', 0),
    ('Farah', 'Ghneim', 0),

    ('Ghanayem', 'Shibl', 0), ('ʿAudi', 'Ziadeh', 0), ('ʿAta', 'Ziadeh', 0),
    ('Makhlouf', 'ʿAwad', 0), ('Saleh', 'Shibl', 0), ('Kaʿoosh', 'Zayed?', 0),
    ('Suweidan', 'Khaleel', 0),

    ('Sabʿa', 'ʿAta', 1), ('Nimr', 'Najm', 0), ('Khaleel', 'ʿAwad', 0),
    ('ʿAudi', 'Makhlouf', 0), ('Khaleel', 'Suweidan', 0), ('ʿEsa', 'Owais?', 0),
    ('Sabʿa', 'Najm', 0),

    ('Ibrahim', 'Makhlouf', 0), ('Ibrahim', 'Rahal', 1), ('ʿAudi', 'Kaʿoosh', 0),
    ('Dheeb', 'ʿAudi', 1), ('Salamy', 'Ibrahim', 1), ('Ibrahim', 'Suweidan', 1),
    ('Dheeb', 'Najm', 1),

    ('ʿEsa', 'Khaleel', 1),
]

# ── the five sons of Rāshid, as both traditions give them ─────────────
FIVE_SONS = ['Ḥaddād', 'Ibrāhīm', 'Jiryis', 'Shuqayr', 'Ḥassān']


def _norm(s):
    """Strip John's query marks and alternative readings down to a key."""
    s = s.split('/')[0].strip().rstrip('?').strip()
    for a, b in (('ʿ', ''), ('ʾ', ''), ('ā', 'a'), ('ī', 'i'), ('ū', 'u'),
                 ('Ḥ', 'H'), ('ḥ', 'h'), ('ṣ', 's'), ('Ṣ', 'S')):
        s = s.replace(a, b)
    return s.lower()


def matches():
    """Households present in BOTH registers under the same name and father."""
    a = {(_norm(n), _norm(f)): (n, f) for n, f in BAYT_JALA_1553}
    out = []
    for n, f, _b in RAMALLAH_1562_CHRISTIAN:
        k = (_norm(n), _norm(f))
        if k in a:
            out.append((n, f))
    seen, uniq = set(), []
    for n, f in out:
        if (n, f) not in seen:
            seen.add((n, f)); uniq.append((n, f))
    return uniq


def patronym_counts(names):
    from collections import Counter
    return Counter(_norm(f) for _n, f, *_ in names)


def sons_as_patronyms():
    """How often each of Rāshid's five sons' names appears as a FATHER in the
    1562 Christian list. A hypothesis-generator, not a finding."""
    c = patronym_counts(RAMALLAH_1562_CHRISTIAN)
    keys = {'Ḥaddād': ['hadeed', 'haddad'], 'Ibrāhīm': ['ibrahim'],
            'Jiryis': ['jirius', 'jiryis'], 'Shuqayr': ['shukair', 'shuqayr'],
            'Ḥassān': ['hassaan', 'hassan']}
    return {k: sum(c.get(x, 0) for x in v) for k, v in keys.items()}


if __name__ == '__main__':
    print('1553 Bayt Jālā households :', len(BAYT_JALA_1553))
    print('1562 Muslim households    :', len(RAMALLAH_1562_MUSLIM))
    print('1562 Christian entries    :', len(RAMALLAH_1562_CHRISTIAN),
          '=', sum(1 for *_x, b in RAMALLAH_1562_CHRISTIAN if not b), 'households +',
          sum(1 for *_x, b in RAMALLAH_1562_CHRISTIAN if b), 'marked bachelors')
    m = matches()
    print('\nsame name AND same father in both registers:', len(m))
    for n, f in m:
        print('   ', n, 'son of', f)
    print('\nRāshid’s five sons as patronyms in 1562:', sons_as_patronyms())
    print('\nany household head named Rāshid?     ',
          any(_norm(n) == 'rashid' for n, _f, _b in RAMALLAH_1562_CHRISTIAN))
    print('any household head SON OF a Rāshid? ',
          any(_norm(f) == 'rashid' for _n, f, _b in RAMALLAH_1562_CHRISTIAN))
