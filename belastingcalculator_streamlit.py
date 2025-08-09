import streamlit as st
from typing import Dict, List, Tuple

# ------------------------------
# Config en stijl
# ------------------------------
st.set_page_config(page_title="Belastingcalculator 2025 – Box 1", page_icon="💶", layout="wide")

PRIMARY = "#1AC6C6"  # turquoise
PRIMARY_DARK = "#0D8F8F"  # donker turquoise
BACKGROUND = "#FFFFFF"  # wit
TEXT = "#000000"  # zwart
MUTED = "#000000"  # zwart
CARD_BG = "#FFFFFF"  # wit
BORDER = "#D6F5F5"
BORDER_STRONG = "#7CCCCC"  # iets donkerder voor duidelijke lijnen

st.markdown(
    f"""
    <style>
      :root {{
        --primary: {PRIMARY};
        --primary-dark: {PRIMARY_DARK};
        --bg: {BACKGROUND};
        --text: {TEXT};
        --muted: {MUTED};
        --cardbg: {CARD_BG};
        --border: {BORDER};
        --border-strong: {BORDER_STRONG};
      }}
      .block-container {{
        padding-top: 2rem;
        padding-bottom: 4rem;
        color: var(--text);
        background: var(--bg);
      }}
      .pill {{
        display: inline-block;
        padding: .25rem .6rem;
        border-radius: 999px;
        background: var(--primary);
        color: var(--text);
        font-weight: 600;
        font-size: .8rem;
      }}
      .card {{
        border: 2px solid var(--border-strong);
        background: var(--cardbg);
        padding: 1rem 1.2rem;
        border-radius: 16px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        color: var(--text);
      }}
      .section-title {{
        color: var(--text);
        font-weight: 700;
        margin-top: 1.2rem;
        margin-bottom: .75rem;
        text-transform: uppercase;
        letter-spacing: .04em;
      }}
      .total {{
        font-size: 1.4rem; font-weight: 800;
        color: var(--text);
      }}
      .metric {{
        font-weight: 700;
        color: var(--text);
      }}
      .muted {{ color: #333; opacity: .85; }}

      /* Forceer tekstkleur voor Streamlit-componenten (labels/captions) */
      /* Forceer lichte achtergrond overal */
      :root, html, body, .stApp,
      [data-testid="stAppViewContainer"],
      section.main, .block-container {{
        background: var(--bg) !important;
        background-color: var(--bg) !important;
        color: var(--text) !important;
      }}
      label,
      [data-testid="stMarkdownContainer"],
      [data-testid="stMarkdownContainer"] *,
      [data-testid="stCaptionContainer"],
      .stCheckbox, .stRadio, .stSlider, .stSelectbox, .stTextInput, .stNumberInput {{
        color: var(--text) !important;
      }}
      [data-testid="stCaptionContainer"] {{
        opacity: 1 !important; /* maak caption goed leesbaar */
      }}
      /* BaseWeb components die Streamlit onder water gebruikt */
      [data-baseweb] {{
        color: var(--text) !important;
      }}
      /* Metrics altijd zwarte tekst en witte achtergrond */
      div[data-testid='stMetricValue'],
      div[data-testid='stMetricLabel'] {{
        color: var(--text) !important;
      }}
      div[data-testid='stMetric'] {{
        background: var(--cardbg) !important;
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
        padding: .75rem 1rem !important;
      }}
      /* Slider – dikker spoor en grotere duim */
      .stSlider [data-baseweb="slider"] > div:nth-child(1) > div {{
        height: 8px !important;
        background: var(--border) !important;
      }}
      .stSlider [data-baseweb="slider"] > div:nth-child(1) > div > div {{
        background: var(--primary) !important; /* actieve track */
      }}
      .stSlider [data-baseweb="slider"] [role="slider"] {{
        width: 22px !important;
        height: 22px !important;
        background: var(--primary) !important;
        border: 2px solid var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(26, 198, 198, 0.15) !important;
      }}
      /* Slider-waardetekst (rode cijfers) → donker turquoise */
      .stSlider [data-baseweb="slider"] ~ div,
      .stSlider [data-baseweb="slider"] + div,
      .stSlider [data-baseweb="slider"] + div span {{
        color: var(--primary-dark) !important;
      }}
      .stSlider [data-baseweb="slider"] [class*="value"],
      .stSlider [data-baseweb="slider"] [class*="ThumbValue"],
      .stSlider [data-baseweb="slider"] [class*="thumb-value"] {{
        color: var(--primary-dark) !important;
      }}
      /* Radio/checkbox accenten in turquoise */
      input[type="checkbox"], input[type="radio"] {{
        accent-color: var(--primary) !important;
      }}
      .stCheckbox svg, .stCheckbox path, .stRadio svg, .stRadio path {{
        fill: var(--primary) !important;
        stroke: var(--primary) !important;
      }}
      .stRadio [data-baseweb="radio"] label:before {{
        border-color: var(--primary-dark) !important;
      }}
      .stRadio [data-baseweb="radio"] label:after {{
        background-color: var(--primary) !important;
      }}
      .stCheckbox [data-baseweb="checkbox"] label:before {{
        border-color: var(--primary-dark) !important;
      }}
      .stCheckbox [data-baseweb="checkbox"] label:after {{
        background-color: var(--primary) !important;
      }}
      /* Expander als card-stijl box met afgeronde hoeken */
      .stExpander {{
        border: 2px solid var(--border-strong) !important;
        border-radius: 16px !important;
        background: var(--cardbg) !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
      }}
      .stExpander details > summary {{
        color: var(--text) !important;
        background: var(--cardbg) !important;
        border-bottom: 2px solid var(--border-strong) !important;
        padding: .6rem .9rem !important;
        border-top-left-radius: 16px !important;
        border-top-right-radius: 16px !important;
      }}
      .stExpander details > div {{
        padding: .75rem 1rem !important;
        background: var(--cardbg) !important;
        border-bottom-left-radius: 16px !important;
        border-bottom-right-radius: 16px !important;
      }}

      /* Duidelijke horizontale scheidingslijn tussen secties */
      hr.section-divider {{
        border: none;
        border-top: 2px solid var(--border-strong);
        margin: 1.5rem 0 1rem 0;
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------
# Constantes – 2025 (indicatief)
# ------------------------------
# Box 1 – uitsluitend inkomstenbelasting (IB) per schijf
# Schijf 1 is 8,17% IB; Volksverzekeringen worden apart berekend
BRACKETS_IB_2025: List[Tuple[float, float]] = [
    (38_441, 0.0817),
    (76_817, 0.3748),
    (float("inf"), 0.4950),
]

ALG_HEFFINGSKORTING_MAX = 3_068.0
ALG_HEFFINGSKORTING_START = 28_406.0
ALG_HEFFINGSKORTING_NIHIL = 76_817.0

ARBEIDSKORTING_MAX = 5_599.0
ARBEIDSKORTING_AFBouw_START = 43_071.0
ARBEIDSKORTING_AFBouw_EIND = 129_078.0

# ZVW – toegepast op winst uit onderneming en resultaat overig werk (indicatief)
ZVW_PERCENT = 0.0526  # 5,26% (voor aanslag / zelfstandigen)
ZVW_MAX_INKOMEN = 75_864.0  # maximale bijdragegrondslag 2025

# Volksverzekeringen – alleen over inkomen tot en met grens schijf 1
VV_AOW = 0.179
VV_ANW = 0.001
VV_WLZ = 0.0965

# Ondernemersaftrekken
ZELFSTANDIGENAFTREK_2025 = 2_470.0
STARTERSAFTREK_2025 = 2_123.0
MKB_WINSTVRIJSTELLING_PCT = 0.127  # 12,7%


# ------------------------------
# Hulpfuncties
# ------------------------------
def euro(amount: float) -> str:
    amount = 0.0 if amount is None else amount
    return f"€ {amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def bereken_schijven(belastbaar_inkomen: float, brackets: List[Tuple[float, float]]) -> List[Tuple[float, float, float]]:
    """Geeft lijst met (belastbaar_in_schijf, tarief, belasting)"""
    resterend = max(belastbaar_inkomen, 0.0)
    vorig_plafond = 0.0
    uitsplitsing: List[Tuple[float, float, float]] = []
    for plafond, tarief in brackets:
        if resterend <= 0:
            break
        ruimte = plafond - vorig_plafond
        in_schijf = min(resterend, ruimte)
        belasting = in_schijf * tarief
        uitsplitsing.append((in_schijf, tarief, belasting))
        resterend -= in_schijf
        vorig_plafond = plafond
    return uitsplitsing


def algemene_heffingskorting(grondslag: float) -> float:
    if grondslag <= ALG_HEFFINGSKORTING_START:
        return ALG_HEFFINGSKORTING_MAX
    if grondslag >= ALG_HEFFINGSKORTING_NIHIL:
        return 0.0
    # lineaire afbouw
    verhouding = (grondslag - ALG_HEFFINGSKORTING_START) / (
        ALG_HEFFINGSKORTING_NIHIL - ALG_HEFFINGSKORTING_START
    )
    return max(ALG_HEFFINGSKORTING_MAX * (1 - verhouding), 0.0)


def computeArbeidskorting(arbeidsinkomenEuro: float) -> float:
    """Bereken arbeidskorting 2025 (niet-AOW) exact volgens staffel.

    - Input: bruto arbeidsinkomen in euro's (float of int). Niet-numeriek of negatief → 0.
    - Output: arbeidskorting in euro's als float (niet afgerond, nooit < 0).

    Staffel 2025 (niet AOW-gerechtigd in 2025):
    1) y ≤ 12.169 → 8,053% × y
    2) 12.169 < y ≤ 26.288 → 980 + 30,030% × (y − 12.169)
    3) 26.288 < y ≤ 43.071 → 5.220 + 2,258% × (y − 26.288)
    4) 43.071 < y ≤ 129.078 → 5.599 − 6,510% × (y − 43.071)
    5) y > 129.078 → 0

    Bron: Belastingdienst – Tabel arbeidskorting 2025
    https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/prive/inkomstenbelasting/heffingskortingen_boxen_tarieven/heffingskortingen/arbeidskorting/tabel-arbeidskorting-2025
    """
    try:
        y = float(arbeidsinkomenEuro)
    except (TypeError, ValueError):
        return 0.0
    if y <= 0:
        return 0.0
    if y <= 12_169:
        return 0.08053 * y
    if y <= 26_288:
        return 980.0 + 0.30030 * (y - 12_169)
    if y <= 43_071:
        return 5_220.0 + 0.02258 * (y - 26_288)
    if y <= 129_078:
        return max(5_599.0 - 0.06510 * (y - 43_071), 0.0)
    return 0.0


def arbeidskorting(arbeidsinkomen: float) -> float:
    """Compatibele wrapper die dezelfde 2025-staffel gebruikt als computeArbeidskorting.
    Houdt dezelfde signatuur als de bestaande code in deze app.
    """
    return computeArbeidskorting(arbeidsinkomen)


def zvw_bijdrage(ondernemingswinst: float, overig_werk: float) -> float:
    bijdragegrondslag = max(min(ondernemingswinst + overig_werk, ZVW_MAX_INKOMEN), 0.0)
    return bijdragegrondslag * ZVW_PERCENT


def premie_volksverzekeringen(belastbaar_inkomen: float) -> Tuple[float, Dict[str, float], float]:
    """Bereken premies volksverzekeringen over inkomen t/m schijf-1 grens.
    Retourneert: (grondslag, breakdown, totaal)
    """
    grondslag = max(min(belastbaar_inkomen, BRACKETS_IB_2025[0][0]), 0.0)
    aow = grondslag * VV_AOW
    anw = grondslag * VV_ANW
    wlz = grondslag * VV_WLZ
    totaal = aow + anw + wlz
    return grondslag, {"AOW": aow, "Anw": anw, "Wlz": wlz}, totaal


# ------------------------------
# UI – invoer
# ------------------------------
st.title("Belastingcalculator 2025 – Box 1")


inkomens: Dict[str, float] = {"loondienst": 0.0, "onderneming": 0.0, "overig": 0.0}
bron_loon = bron_onderneming = bron_overig = False
ondernemers_aftrek = 0.0
urencriterium_gehaald = False
kies_starters = False
kies_zsa = False
kies_mkb = False

col1, col2, col3 = st.columns(3)
with col1:
    with st.expander("Loondienst", expanded=True):
        bron_loon = st.checkbox("Actief", value=False, key="bron_loon_actief")
        if bron_loon:
            invoerwijze_loon = st.radio("Invoerwijze", ["Slider", "Handmatig"], horizontal=True, key="invoer_loon")
            if invoerwijze_loon == "Slider":
                inkomens["loondienst"] = float(st.slider("Bruto jaarsalaris", 0, 100_000, 0, step=500))
            else:
                inkomens["loondienst"] = float(st.number_input("Bruto jaarsalaris", min_value=0, max_value=1_000_000, value=0, step=100))
            st.caption("Bruto jaarsalaris.")
with col2:
    with st.expander("Winst uit onderneming", expanded=True):
        bron_onderneming = st.checkbox("Actief", value=False, key="bron_onderneming_actief")
        if bron_onderneming:
            invoerwijze_wo = st.radio("Invoerwijze", ["Slider", "Handmatig"], horizontal=True, key="invoer_wo")
            if invoerwijze_wo == "Slider":
                inkomens["onderneming"] = float(st.slider("Winst uit onderneming", 0, 100_000, 0, step=500))
            else:
                inkomens["onderneming"] = float(st.number_input("Winst uit onderneming", min_value=0, max_value=1_000_000, value=0, step=100, key="num_wo"))
            st.markdown("<div class=\"section-title\" style=\"margin-top:.25rem\">Aftrekken</div>", unsafe_allow_html=True)
            kies_starters = st.checkbox(f"Startersaftrek ({euro(STARTERSAFTREK_2025)})", key="kies_starters")
            kies_zsa = st.checkbox(f"Zelfstandigenaftrek (ZSA) ({euro(ZELFSTANDIGENAFTREK_2025)})", key="kies_zsa")
            kies_mkb = st.checkbox("MKB-winstvrijstelling toepassen (12,7%)", value=True, key="kies_mkb")
            if kies_zsa:
                urencriterium_gehaald = st.checkbox("Ik heb ≥ 1.225 uur gewerkt", key="urencriterium")
            with st.expander("Wanneer startersaftrek/ZSA?", expanded=False):
                st.markdown(
                    "- Startersaftrek: beginnende ondernemer; binnen 5 jaar max 3x toepassen.\n"
                    "- ZSA: alleen bij urencriterium (≥ 1.225 uur) en winst uit onderneming.")
with col3:
    with st.expander("Winst uit overig werk", expanded=True):
        bron_overig = st.checkbox("Actief", value=False, key="bron_overig_actief")
        if bron_overig:
            invoerwijze_ow = st.radio("Invoerwijze", ["Slider", "Handmatig"], horizontal=True, key="invoer_ow")
            if invoerwijze_ow == "Slider":
                inkomens["overig"] = float(st.slider("Winst uit overig werk", 0, 100_000, 0, step=500))
            else:
                inkomens["overig"] = float(st.number_input("Winst uit overig werk", min_value=0, max_value=1_000_000, value=0, step=100, key="num_ow"))

if bron_onderneming:
    if kies_starters:
        ondernemers_aftrek += STARTERSAFTREK_2025
    if kies_zsa and urencriterium_gehaald:
        ondernemers_aftrek += ZELFSTANDIGENAFTREK_2025


# ------------------------------
# Berekeningen
# ------------------------------
bel_loon = max(inkomens["loondienst"], 0.0)
bel_overig = max(inkomens["overig"], 0.0)
bruto_winst_onderneming = max(inkomens["onderneming"], 0.0)
ondernemingsgrondslag_na_oa = max(bruto_winst_onderneming - ondernemers_aftrek, 0.0)
mkb_winstvrijstelling = (ondernemingsgrondslag_na_oa * MKB_WINSTVRIJSTELLING_PCT) if (bron_onderneming and kies_mkb) else 0.0
bel_onderneming = max(ondernemingsgrondslag_na_oa - mkb_winstvrijstelling, 0.0)

totale_belastbare_grondslag = bel_loon + bel_overig + bel_onderneming

# Heffingskortingen
# Arbeidskorting: berekend op arbeidsinkomen (bruto loon + bruto winst + bruto overig werk)
arbeidsinkomen_korting = max(inkomens["loondienst"], 0.0) + max(inkomens["onderneming"], 0.0) + max(inkomens["overig"], 0.0)
ak = arbeidskorting(arbeidsinkomen_korting)
ahk = algemene_heffingskorting(totale_belastbare_grondslag)

# Inkomstenbelasting per schijf (IB)
schijven_ib = bereken_schijven(totale_belastbare_grondslag, BRACKETS_IB_2025)
belasting_bruto_ib = sum(bedrag for _, _, bedrag in schijven_ib)

# Netto IB na kortingen (niet negatief)
belasting_netto = max(belasting_bruto_ib - ak - ahk, 0.0)

# ZVW – alleen over ondernemingswinst + overig werk
zvw = zvw_bijdrage(bel_onderneming, bel_overig)

# Volksverzekeringen – berekend los van IB
vv_grondslag, vv_parts, vv_totaal = premie_volksverzekeringen(totale_belastbare_grondslag)

# IB + VV na heffingskortingen (zoals Belastingdienst presenteert)
ib_vv_na_kortingen = max(belasting_bruto_ib + vv_totaal - (ak + ahk), 0.0)

# ------------------------------
# Samenvatting bovenaan – totaal belastbaar inkomen
# ------------------------------
st.markdown("<div class=\"section-title\">Totaal belastbaar inkomen</div>", unsafe_allow_html=True)
st.markdown(
    f"""
<div class="card">
  <div>Loondienst: {euro(bel_loon)}</div>
  <div>Winst uit onderneming: {euro(bel_onderneming)}</div>
  <div>Winst uit overig werk: {euro(bel_overig)}</div>
  <div class="metric">Totaal: {euro(totale_belastbare_grondslag)}</div>
</div>
""",
    unsafe_allow_html=True,
)


# ------------------------------
# Presentatie
# ------------------------------
st.markdown("<div class=\"section-title\">Belastbare bedragen per onderdeel</div>", unsafe_allow_html=True)
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
colp, colq, colr = st.columns(3)
with colp:
    st.markdown(
        f"""
<div class="card">
  <strong>Loondienst</strong>
  <div>Belastbaar: {euro(bel_loon)}</div>
</div>
""",
        unsafe_allow_html=True,
    )
with colq:
    st.markdown(
        f"""
<div class="card">
  <strong>Winst uit onderneming</strong>
  <div>Bruto winst: {euro(bruto_winst_onderneming)}</div>
  <div>Ondernemersaftrek: − {euro(ondernemers_aftrek)}</div>
  <div>MKB-winstvrijstelling (12,7%): − {euro(mkb_winstvrijstelling)}</div>
  <div>Belastbaar: {euro(bel_onderneming)}</div>
</div>
""",
        unsafe_allow_html=True,
    )
with colr:
    st.markdown(
        f"""
<div class="card">
  <strong>Winst uit overig werk</strong>
  <div>Belastbaar: {euro(bel_overig)}</div>
</div>
""",
        unsafe_allow_html=True,
    )


st.markdown("<div class=\"section-title\">Box 1 – inkomstenbelasting per schijf (excl. volksverzekeringen)</div>", unsafe_allow_html=True)
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
for idx, (grondslag, tarief, bedrag) in enumerate(schijven_ib, start=1):
    st.markdown(f"- Schijf {idx}: {euro(grondslag)} × {tarief*100:.2f}% = **{euro(bedrag)}**")

st.markdown("<div class=\"section-title\">Premie volksverzekeringen (indicatief)</div>", unsafe_allow_html=True)
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown(
    f"""
<div class="card">
  <div>Grondslag tot schijf 1: {euro(vv_grondslag)}</div>
  <div>- AOW (17,9%): {euro(vv_parts['AOW'])}</div>
  <div>- Anw (0,1%): {euro(vv_parts['Anw'])}</div>
  <div>- Wlz (9,65%): {euro(vv_parts['Wlz'])}</div>
  <div><strong>Totaal premie volksverzekeringen: {euro(vv_totaal)}</strong></div>
</div>
""",
    unsafe_allow_html=True,
)

# Extra container: Bijdrage-inkomen zorgverzekeringswet
st.markdown("<div class=\"section-title\">Bijdrage-inkomen Zorgverzekeringswet</div>", unsafe_allow_html=True)
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
zvw_grondslag = min(bel_onderneming + bel_overig, ZVW_MAX_INKOMEN)
st.markdown(
    f"""
<div class="card">
  <div>Belastbare winst uit onderneming + overig werk: {euro(bel_onderneming + bel_overig)}</div>
  <div>Grondslag ZVW (gemaximeerd op {euro(ZVW_MAX_INKOMEN)}): {euro(zvw_grondslag)}</div>
  <div>Bijdragepercentage: {ZVW_PERCENT*100:.2f}%</div>
  <div>ZVW-bijdrage: <strong>{euro(zvw)}</strong></div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("<div class=\"section-title\">Heffingskortingen</div>", unsafe_allow_html=True)
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
wrap_left, wrap_center, wrap_right = st.columns([1,2,1])
with wrap_center:
    st.markdown(
        f"""
<div class="card">
  <div>Arbeidskorting (verlaagt uw belasting): <strong>{euro(ak)}</strong></div>
  <div>Algemene heffingskorting: <strong>{euro(ahk)}</strong></div>
</div>
""",
        unsafe_allow_html=True,
    )

st.markdown("<div class=\"section-title\">Totaal te betalen</div>", unsafe_allow_html=True)
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
colt1, colt2, colt3 = st.columns(3)
with colt1:
    st.metric("IB + Volksverzekeringen (na kortingen)", euro(ib_vv_na_kortingen))
with colt2:
    st.metric("Zorgverzekeringswet (ZVW)", euro(zvw))
with colt3:
    st.metric("Totaal te betalen", euro(ib_vv_na_kortingen + zvw))

st.caption(
    "Indicatieve berekening 2025. Tarieven: 35,82% / 37,48% / 49,50%. "
    "Heffingskortingen en ZVW benaderd voor snelle inschatting."
)

