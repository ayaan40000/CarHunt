#!/usr/bin/env python3
"""CarHunt board transform (2026-11-18): trait chips + representative images +
negotiation blocks + slim header + Visual view, applied to index.html from
data/listings.json (the DB export). Idempotency-guarded: refuses to run twice.

Preserves every METHOD.md contract block: app-link script, inline manifest,
icon/manifest head links, Finalists tab + Phase 1/2 script, data stamp (moved
to one line; full run notes preserved verbatim in the FAQ 'About this board'
section). Run: python3 tools/apply_traits.py
"""
import json, re, sys, html as htmllib

BASE = '/home/hatch/workspace/reserved-1'
recs = json.load(open(f'{BASE}/data/listings.json'))
doc = open(f'{BASE}/index.html').read()

if 'class="trait"' in doc:
    sys.exit('ABORT: trait chips already present (transform already applied)')

by_item = {}
for r in recs:
    m = re.search(r'/marketplace/item/(\d+)/', r['url'])
    by_item[m.group(1)] = r

# ---------- glyphs (24x24 stroke icons, currentColor) ----------
def svg(paths):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true">{paths}</svg>')
GLYPHS = {
 'sedan': svg('<path d="M3.5 14.5 5.4 10a2 2 0 0 1 1.8-1.3h5.6l3.4 2 3 .7c.8.2 1.3.9 1.3 1.7v1.4"/><path d="M2.5 14.5h19"/><circle cx="7.2" cy="17.2" r="1.8"/><circle cx="16.8" cy="17.2" r="1.8"/><path d="M9 17.2h6"/>'),
 'suv': svg('<path d="M4.5 14.5V8.2A1.7 1.7 0 0 1 6.2 6.5h8.3c.5 0 1 .2 1.4.6l2.9 3.2 1.2.5c.8.3 1.3 1 1.3 1.9v1.8"/><path d="M2.5 14.5h19"/><circle cx="7.2" cy="17.2" r="1.8"/><circle cx="16.8" cy="17.2" r="1.8"/><path d="M9 17.2h6"/><path d="M9.8 6.5v4.2M14.6 7v3.7"/>'),
 'hatchback': svg('<path d="M3.5 14.5 5.4 10a2 2 0 0 1 1.8-1.3h5.4l3.4 2 2.4 3.3"/><path d="M2.5 14.5h19"/><circle cx="7.2" cy="17.2" r="1.8"/><circle cx="16.8" cy="17.2" r="1.8"/><path d="M9 17.2h6"/>'),
 'coupe': svg('<path d="M3 14.8c2.5-1 4-4.3 7-5.3 3.2-1.1 6.5.2 8.6 1.7l1.9.8c.7.3 1 1 1 1.7v1.1"/><path d="M2.5 14.8h19"/><circle cx="7.2" cy="17.2" r="1.8"/><circle cx="16.8" cy="17.2" r="1.8"/><path d="M9 17.2h6"/>'),
 'wagon': svg('<path d="M3.5 14.5 5.2 9.8A2 2 0 0 1 7.1 8.5h7.2l4.2 2.4 1.9.8c.7.3 1.1 1 1.1 1.7v1.1"/><path d="M2.5 14.5h19"/><circle cx="7.2" cy="17.2" r="1.8"/><circle cx="16.8" cy="17.2" r="1.8"/><path d="M9 17.2h6"/>'),
 'van': svg('<path d="M4 14.5V7.8A1.8 1.8 0 0 1 5.8 6h8.4l4.4 4.4 1.3.6c.8.3 1.1 1 1.1 1.8v1.7"/><path d="M2.5 14.5h19"/><circle cx="7.2" cy="17.2" r="1.8"/><circle cx="16.8" cy="17.2" r="1.8"/><path d="M9 17.2h6"/>'),
 'leaf': svg('<path d="M5.5 18.5C5.5 11 11 5.5 19.5 5c0 8.5-5 13.5-12 13.5"/><path d="M5.5 18.5c1.8-4.8 4.8-7.8 8.8-9.7"/>'),
 'person': svg('<circle cx="12" cy="8" r="3.3"/><path d="M5.5 19.5c1.3-3.4 3.7-4.8 6.5-4.8s5.2 1.4 6.5 4.8"/>'),
 'storefront': svg('<path d="M4.5 8.5 6 4.5h12l1.5 4"/><path d="M4.5 8.5h15"/><path d="M6 8.5V19h12V8.5"/><path d="M9.8 19v-4.5h4.4V19"/>'),
 'star': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 3.4l2.6 5.3 5.8.8-4.2 4.1 1 5.8-5.2-2.8-5.2 2.8 1-5.8-4.2-4.1 5.8-.8z"/></svg>',
 'shield': svg('<path d="M12 3.2 19 5.7v6c0 4.5-2.9 7.4-7 9.1-4.1-1.7-7-4.6-7-9.1v-6z"/><path d="M8.8 11.7l2.2 2.2 4.2-4.4"/>'),
}
BODY_LABEL = {'sedan': 'Sedan', 'suv': 'SUV', 'hatchback': 'Hatchback',
              'coupe': 'Coupe', 'wagon': 'Wagon', 'van': 'Van'}

def chip(trait, value, glyph, label, title):
    return (f'<button type="button" class="trait" data-trait="{trait}" '
            f'data-value="{value}" aria-pressed="false" title="{title}">'
            f'{GLYPHS[glyph]}<span>{label}</span></button>')

def traits_row(r):
    chips = []
    bt = (r.get('body_type') or '').lower()
    if bt in GLYPHS and bt in BODY_LABEL:
        chips.append(chip('body', bt, bt, BODY_LABEL[bt], f'Filter: {BODY_LABEL[bt]} only'))
    if r.get('hybrid') is True:
        chips.append(chip('hybrid', 'true', 'leaf', 'Hybrid', 'Filter: hybrids only'))
    st = r.get('seller_type')
    if st == 'private':
        chips.append(chip('seller', 'private', 'person', 'Private', 'Filter: private sellers only'))
    elif st == 'dealer':
        chips.append(chip('seller', 'dealer', 'storefront', 'Dealer', 'Filter: dealers only'))
    g = r.get('grade')
    if g:
        band = g[0]
        chips.append(chip('grade', band, 'star', f'Grade {g}', f'Filter: grade {band} band'))
    rel = r.get('reliability_score')
    if rel is not None:
        rv = '%g' % rel
        chips.append(chip('rel', rv, 'shield', f'Rel {rv}/5', f'Filter: reliability {rv}/5 or better'))
    return '<p class="traits" role="group" aria-label="Traits — tap an icon to filter">' + ''.join(chips) + '</p>'

def img_label(r):
    src = r.get('representative_image_source') or ''
    return src.split('—', 1)[1].split('(File:')[0].strip() if '—' in src else f"{r['year']} {r['make']} {r['model']}"

# ---------- per-card transforms ----------
card_re = re.compile(r'<article class="card".*?</article>', re.S)
cards = card_re.findall(doc)
assert len(cards) == len(recs) == 47, f'card count {len(cards)}'

def fix_card(block):
    m = re.search(r'/marketplace/item/(\d+)/', block)
    r = by_item[m.group(1)]
    # opening tag: seller/rel data attrs + hybrid value from record
    tag_end = block.index('>')
    tag = block[:tag_end]
    hv = 'true' if r['hybrid'] is True else ('false' if r['hybrid'] is False else 'null')
    tag = re.sub(r'data-hybrid="(?:true|false)"', f'data-hybrid="{hv}"', tag)
    assert 'data-seller' not in tag
    tag = tag + f' data-seller="{r["seller_type"]}" data-rel="{"%g" % r["reliability_score"]}"'
    block = tag + block[tag_end:]
    # representative image after h3
    label = img_label(r)
    fig = (f'<figure class="repimg"><img src="{r["representative_image"]}" '
           f'alt="Representative image — not the actual car: {htmllib.escape(label, quote=True)}" '
           f'loading="lazy" onerror="this.parentNode.style.display=\'none\'">'
           f'<figcaption>Representative image — not the actual car</figcaption></figure>')
    block = re.sub(r'(</h3>)', r'\1\n' + fig, block, count=1)
    # traits row after badges paragraph
    block = re.sub(r'(<p class="badges">.*?</p>)', r'\1\n' + traits_row(r), block, count=1, flags=re.S)
    # negotiation block inside card-more
    neg = (f'<div class="negot"><p class="small"><b>Negotiation:</b> '
           f'{htmllib.escape(r["negotiation_notes"], quote=False)}</p></div>\n')
    if '<details><summary>Full sweep notes</summary>' in block:
        block = block.replace('<details><summary>Full sweep notes</summary>',
                              neg + '<details><summary>Full sweep notes</summary>', 1)
    else:
        idx = block.rfind('</div>')
        block = block[:idx] + neg + block[idx:]
    return block

doc = card_re.sub(lambda m: fix_card(m.group(0)), doc)

# ---------- measurement: above-the-fold prose before ----------
def vis_text(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s)).strip()
old_header = re.search(r'<header>.*?</header>', doc, re.S).group(0)
old_stamp = re.search(r'<div class="stamp">(.*?)</div>', doc, re.S).group(1)
before_chars = len(vis_text(old_header)) + len(vis_text(old_stamp))

# ---------- slim header + one-line stamp (prose moved verbatim to FAQ) ----------
favicon = re.search(r'<link rel="icon" href="([^"]+)">', doc).group(1)
paras = re.findall(r'<p>.*?</p>', old_header, re.S)
assert len(paras) == 2, f'header paragraphs: {len(paras)}'
meets = sum(1 for r in recs if r['meets_criteria'])
new_header = ('<header><div class="brandrow">'
              f'<img class="brandlogo" src="{favicon}" alt="" width="34" height="34">'
              '<h1>Reliable car under $15,000 — Houston</h1></div>'
              f'<p class="boardsum">{len(recs)} listings · {meets} meet all must-haves · Nov 18, 2026</p></header>')
doc = doc.replace(old_header, new_header, 1)
new_stamp = 'Listings from Facebook Marketplace sweeps, Nov 18, 2026 — listings sell fast; a car shown here may already be gone.'
doc = re.sub(r'<div class="stamp">.*?</div>', f'<div class="stamp">{new_stamp}</div>', doc, count=1, flags=re.S)
after_chars = len(vis_text(new_header)) + len(new_stamp)

about = ('<h3>About this board</h3>\n' + paras[0] + '\n' + paras[1] +
         '\n<h3>Run notes — Nov 18, 2026</h3>\n<p class="small">' + old_stamp + '</p>\n')
anchor = '<div id="view-faq" hidden>\n<section class="help"><h2>FAQ &amp; Help</h2>'
assert anchor in doc
doc = doc.replace(anchor, anchor + '\n' + about, 1)

# ---------- tabs: Visual ----------
tab_anchor = '<button id="tabPaper" onclick="showTab(\'paper\')">Paperwork (TX)</button>'
assert tab_anchor in doc
doc = doc.replace(tab_anchor, tab_anchor + '<button id="tabVisual" onclick="showTab(\'visual\')">Visual</button>', 1)

old_showtab = re.search(r"function showTab\(t\)\{[^}]*\}", doc).group(0)
new_showtab = ("function showTab(t){document.getElementById('view-list').hidden=t!=='list';"
 "document.getElementById('view-fin').hidden=t!=='fin';document.getElementById('view-faq').hidden=t!=='faq';"
 "document.getElementById('view-paper').hidden=t!=='paper';document.getElementById('view-visual').hidden=t!=='visual';"
 "document.getElementById('toolbar').hidden=t!=='list';document.getElementById('tabList').classList.toggle('active',t==='list');"
 "document.getElementById('tabFin').classList.toggle('active',t==='fin');document.getElementById('tabFaq').classList.toggle('active',t==='faq');"
 "document.getElementById('tabPaper').classList.toggle('active',t==='paper');document.getElementById('tabVisual').classList.toggle('active',t==='visual');}")
doc = doc.replace(old_showtab, new_showtab, 1)

# ---------- Visual view ----------
groups = {}
for r in recs:
    groups.setdefault(r['representative_image'], []).append(r)
vg = []
for url, rs in sorted(groups.items(), key=lambda kv: (-len(kv[1]), img_label(kv[1][0]))):
    r0 = rs[0]
    label = img_label(r0)
    yrs = sorted(x['year'] for x in rs)
    ytxt = f'{yrs[0]}' if yrs[0] == yrs[-1] else f'{yrs[0]}–{yrs[-1]}'
    low = min(x['price'] for x in rs)
    model = f"{r0['make']} {r0['model']}"
    vg.append(f'<section class="vgroup"><img src="{url}" alt="Representative image — not the actual car: {htmllib.escape(label, quote=True)}" loading="lazy" onerror="this.style.display=\'none\'">'
              f'<div class="vinfo"><h3>{htmllib.escape(label)}</h3>'
              f'<p class="small muted">{ytxt} · {len(rs)} listing{"s" if len(rs) != 1 else ""} · from ${low:,}</p>'
              f'<button type="button" class="slim-btn2 vshow" data-model="{htmllib.escape(model, quote=True)}">Show in Listings</button></div></section>')
visual = '<div id="view-visual" hidden>\n<div class="vgrid">' + '\n'.join(vg) + '</div>\n</div>\n'
paper_end = '</section></div>\n</main>'
assert paper_end in doc
doc = doc.replace(paper_end, '</section></div>\n' + visual + '</main>', 1)

# ---------- filters panel: seller / grade / reliability + clear-all ----------
body_div_end = 'Van / minivan</option></select></label></div>'
assert body_div_end in doc
doc = doc.replace(body_div_end, body_div_end +
  '\n<div><label>Seller <select id="fSeller"><option value="">All sellers</option><option value="private">Private</option><option value="dealer">Dealer</option></select></label></div>'
  '\n<div><label>Grade band <select id="fGrade"><option value="">All grades</option><option value="A">A band</option><option value="B">B band</option><option value="C">C band</option><option value="D">D band</option></select></label></div>', 1)
model_div_end = 'Toyota RAV4</option></select></label></div>'
assert model_div_end in doc
doc = doc.replace(model_div_end, model_div_end +
  '\n<div><label>Min reliability <select id="fRel"><option value="">Any</option><option value="3">3 / 5 +</option><option value="3.5">3.5 / 5 +</option><option value="4">4 / 5 +</option></select></label></div>', 1)
clear_anchor = 'cap at C+.</p>\n</div>'
assert clear_anchor in doc
doc = doc.replace(clear_anchor, 'cap at C+.</p>\n<div class="clearrow"><button type="button" class="filters-btn slim-btn" id="fClear">Clear all filters</button></div>\n</div>', 1)

# ---------- apply(): new conditions, badge terms, trait sync, listeners ----------
def rep1(old, new):
    global doc
    assert doc.count(old) == 1, f'anchor not unique/found: {old[:60]}... count={doc.count(old)}'
    doc = doc.replace(old, new, 1)

rep1("bt=document.getElementById('fBody').value;",
     "bt=document.getElementById('fBody').value, se=document.getElementById('fSeller').value, gb=document.getElementById('fGrade').value, rm=document.getElementById('fRel').value;")
rep1("&&(!de||d.deal==='true');",
     "&&(!de||d.deal==='true')&&(!se||d.seller===se)&&(!gb||(d.grade||'').charAt(0)===gb)&&(!rm||parseFloat(d.rel)>=parseFloat(rm));")
rep1("+(de?1:0));",
     "+(de?1:0)+(se?1:0)+(gb?1:0)+(rm?1:0)); if(window.__syncTraits)window.__syncTraits({body:bt,hybrid:hy,seller:se,grade:gb,rel:rm});")
rep1("'fPrice','fMiles','fModel','fBody','fSort','fHybrid','fAA','fMeets','fDeal'",
     "'fPrice','fMiles','fModel','fBody','fSort','fHybrid','fAA','fMeets','fDeal','fSeller','fGrade','fRel'")

# ---------- CSS ----------
css = """
/* Traits + slim header + visual view (2026-11-18) */
.brandrow{display:flex;align-items:center;gap:10px}
.brandlogo{border-radius:7px;flex:none}
header h1{margin:0}
.boardsum{margin:4px 0 0;font-size:13.5px;color:#cfe0cf}
.stamp{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.traits{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 10px}
.trait{display:inline-flex;align-items:center;gap:5px;min-height:32px;padding:4px 9px;border:1.5px solid #9db3a4;border-radius:99px;background:#f4f7f2;color:var(--green);font-size:12.5px;font-weight:700;cursor:pointer}
.trait svg{width:17px;height:17px;flex:none}
.trait.on{background:var(--green);color:#fff;border-color:var(--green)}
.repimg{margin:0 0 10px}
.repimg img{width:100%;height:132px;object-fit:cover;border-radius:10px;display:block;background:#dfe5dc}
.repimg figcaption{font-size:11.5px;color:var(--muted);margin-top:3px}
.negot{background:#fdf6e0;border:1px solid #e6cf8a;border-radius:10px;padding:9px 11px;margin:0 0 9px}
.negot p{margin:0}
.clearrow{margin-top:12px}
.vgrid{display:grid;grid-template-columns:1fr;gap:14px;margin-top:14px}
.vgroup{background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:0 1px 3px rgba(18,53,36,.10)}
.vgroup img{width:100%;height:190px;object-fit:cover;display:block;background:#dfe5dc}
.vinfo{padding:12px 14px}
.vinfo h3{margin:0 0 4px;font-size:17px}
.vinfo p{margin:0 0 10px}
@media (min-width:720px){.vgrid{grid-template-columns:repeat(2,1fr)}}
@media (min-width:1024px){.vgrid{grid-template-columns:repeat(3,1fr)}}
"""
assert '</style>' in doc
doc = doc.replace('</style>', css + '</style>', 1)
rep1('#view-paper{display:none!important}', '#view-paper,#view-visual{display:none!important}')

# ---------- trait/visual script (appended last; breaks no existing block) ----------
script = """<script>
// Trait chips + clear-all + Visual view wiring (2026-11-18). apply() and
// showTab() are defined above; window.__syncTraits is called by apply().
(function(){
 function $(id){return document.getElementById(id)}
 window.__syncTraits=function(st){
  document.querySelectorAll('.trait').forEach(function(ch){
   var t=ch.getAttribute('data-trait'),v=ch.getAttribute('data-value'),on=false;
   if(t==='body')on=st.body===v;
   else if(t==='hybrid')on=!!st.hybrid;
   else if(t==='seller')on=st.seller===v;
   else if(t==='grade')on=st.grade===v;
   else if(t==='rel')on=st.rel!==''&&parseFloat(st.rel)===parseFloat(v);
   ch.classList.toggle('on',on); ch.setAttribute('aria-pressed',on?'true':'false');
  });
 };
 document.querySelectorAll('.trait').forEach(function(ch){
  ch.addEventListener('click',function(){
   var t=ch.getAttribute('data-trait'),v=ch.getAttribute('data-value');
   if(t==='body'){var e=$('fBody'); e.value=(e.value===v?'':v);}
   else if(t==='hybrid'){var h=$('fHybrid'); h.checked=!h.checked;}
   else if(t==='seller'){var s=$('fSeller'); s.value=(s.value===v?'':v);}
   else if(t==='grade'){var g=$('fGrade'); g.value=(g.value===v?'':v);}
   else if(t==='rel'){var r=$('fRel'); r.value=(r.value===v?'':v);}
   apply();
  });
 });
 var clr=$('fClear');
 if(clr)clr.addEventListener('click',function(){
  ['fPrice','fMiles'].forEach(function(id){$(id).value='';});
  ['fBody','fModel','fSeller','fGrade','fRel','fSort'].forEach(function(id){$(id).value='';});
  ['fHybrid','fAA','fMeets','fDeal'].forEach(function(id){$(id).checked=false;});
  apply();
 });
 document.querySelectorAll('.vshow').forEach(function(b){
  b.addEventListener('click',function(){
   $('fModel').value=b.getAttribute('data-model'); showTab('list'); apply();
   var g=$('grid'); if(g)g.scrollIntoView();
  });
 });
 window.__syncTraits({body:$('fBody').value,hybrid:$('fHybrid').checked,seller:$('fSeller').value,grade:$('fGrade').value,rel:$('fRel').value});
})();
</script>
"""
assert doc.endswith('</script>\n</body></html>')
doc = doc.replace('</script>\n</body></html>', '</script>\n' + script + '</body></html>', 1)

open(f'{BASE}/index.html', 'w').write(doc)
print(f'OK: cards={len(cards)} visual_groups={len(groups)}')
print(f'above-fold prose: before={before_chars} chars, after={after_chars} chars '
      f'({100 - round(100 * after_chars / before_chars)}% reduction)')
