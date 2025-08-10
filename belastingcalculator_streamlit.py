import streamlit as st
from typing import Dict, List, Tuple

# ------------------------------
# Config en stijl
# ------------------------------
st.set_page_config(page_title="Belastingcalculator – Box 1", page_icon="💶", layout="wide")

PRIMARY = "#1AC6C6"  # turquoise
PRIMARY_DARK = "#0D8F8F"  # donker turquoise
BLUE_THUMB = "#1E90FF"  # blauw voor slider-duim
BACKGROUND = "#FFFFFF"  # wit
TEXT = "#000000"  # zwart
MUTED = "#000000"  # zwart
CARD_BG = "#FFFFFF"  # wit
BORDER = "#D6F5F5"
BORDER_STRONG = "#7CCCCC"  # iets donkerder voor duidelijke lijnen

# Jaarselectie (bovenin – eerste vraag)
BELASTINGJAREN = [2024, 2025]
gekozen_jaar = st.radio("Welk jaar wil je berekenen?", BELASTINGJAREN, index=1, format_func=lambda y: f"Jaar {y}")

st.markdown(
    f"""
    <style>
      :root {{
        --primary: {PRIMARY};
        --primary-dark: {PRIMARY_DARK};
        --blue: {BLUE_THUMB};
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
      [data-testid="stHeader"],
      section.main, .block-container {{
        background: var(--bg) !important;
        background-color: var(--bg) !important;
        color: var(--text) !important;
      }}
      /* Maak de bovenbalk licht en vlak */
      [data-testid="stHeader"] {{
        background: var(--bg) !important;
        background-color: var(--bg) !important;
        box-shadow: none !important;
        border-bottom: 0 !important;
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
      /* Slider – dikker spoor en vierkante blauwe duim */
      .stSlider [data-baseweb="slider"] > div:nth-child(1) > div {{
        height: 12px !important;
        background: var(--border) !important;
      }}
      .stSlider [data-baseweb="slider"] > div:nth-child(1) > div > div {{
        background: var(--primary) !important; /* actieve track */
      }}
      .stSlider [data-baseweb="slider"] [role="slider"] {{
        width: 22px !important;
        height: 22px !important;
        background: var(--blue) !important;
        border: 2px solid var(--blue) !important;
        border-radius: 4px !important; /* vierkant */
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
      /* Radio als witte vierkante vakjes met zwarte rand en zwarte selectie */
      .stRadio [data-baseweb="radio"] label:before {{
        border: 2px solid #000 !important;
        background: #FFFFFF !important;
        border-radius: 4px !important;
        width: 20px !important;
        height: 20px !important;
      }}
      .stRadio [data-baseweb="radio"] label:after {{
        background-color: #000000 !important;
        border-radius: 2px !important;
        width: 12px !important;
        height: 12px !important;
        left: 4px !important;
        top: 4px !important;
      }}
      .stCheckbox [data-baseweb="checkbox"] label:before {{
        border-color: var(--primary-dark) !important;
      }}
      .stCheckbox [data-baseweb="checkbox"] label:after {{
        background-color: var(--primary) !important;
      }}
      /* Number inputs wit met zwarte tekst */
      .stNumberInput input {{
        background: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid var(--border-strong) !important;
        border-radius: 10px !important;
        padding: 0.25rem 0.5rem !important;
      }}
      /* Text inputs wit met zwarte tekst (geen pijltjes) */
      .stTextInput input {{
        background: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid var(--border-strong) !important;
        border-radius: 10px !important;
        padding: 0.35rem 0.6rem !important;
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
# Constantes – per jaar (indicatief)
# ------------------------------
# 2025 – Box 1 uitsluitend inkomstenbelasting (IB) per schijf
BRACKETS_IB_2025: List[Tuple[float, float]] = [
    (38_441, 0.0817),
    (76_817, 0.3748),
    (float("inf"), 0.4950),
]

# 2024 – Box 1 uitsluitend inkomstenbelasting (IB) per schijf
# Let op: in schijf 1 worden VV apart berekend, daarom is hier IB-only ca. 9,32%.
BRACKETS_IB_2024: List[Tuple[float, float]] = [
    (38_098, 0.0932),
    (75_519, 0.3697),
    (float("inf"), 0.4950),
]

# Algemene heffingskorting (per jaar) – indicatief
ALG_2025 = {
    "MAX": 3_068.0,
    "START": 28_406.0,
    "NIHIL": 76_817.0,
}
# Voor 2024 tijdelijk gelijk gezet aan 2025 (vul desgewenst exacte 2024-cijfers in)
ALG_2024 = ALG_2025.copy()

# Arbeidskorting parameters (maxima, afbouwpunten) – voor staffeltekst/UI
AK_2025 = {
    "MAX": 5_599.0,
    "AFBOUW_START": 43_071.0,
    "AFBOUW_EIND": 129_078.0,
}
AK_2024 = AK_2025.copy()

# ZVW – toegepast op winst uit onderneming en resultaat overig werk (indicatief)
ZVW_2025 = {"PCT": 0.0526, "MAX_INKOMEN": 75_864.0}
ZVW_2024 = ZVW_2025.copy()

# Volksverzekeringen – alleen over inkomen tot en met grens schijf 1
VV_2025 = {"AOW": 0.179, "ANW": 0.001, "WLZ": 0.0965}
VV_2024 = VV_2025.copy()

# Jaar-specifieke selectie
if gekozen_jaar == 2025:
    BRACKETS_IB = BRACKETS_IB_2025
    ALG = ALG_2025
    AK_META = AK_2025
    ZVW_CFG = ZVW_2025
    VV_CFG = VV_2025
else:
    BRACKETS_IB = BRACKETS_IB_2024
    ALG = ALG_2024
    AK_META = AK_2024
    ZVW_CFG = ZVW_2024
    VV_CFG = VV_2024

# Ondernemersaftrekken per jaar
ZELFSTANDIGENAFTREK_2025 = 2_470.0
ZELFSTANDIGENAFTREK_2024 = 3_750.0
STARTERSAFTREK_2025 = 2_123.0
STARTERSAFTREK_2024 = 2_123.0
MKB_WINSTVRIJSTELLING_PCT_2025 = 0.127   # 12,7%
MKB_WINSTVRIJSTELLING_PCT_2024 = 0.1331  # 13,31%

if gekozen_jaar == 2025:
    ZELFSTANDIGENAFTREK = ZELFSTANDIGENAFTREK_2025
    STARTERSAFTREK = STARTERSAFTREK_2025
    MKB_WINSTVRIJSTELLING_PCT = MKB_WINSTVRIJSTELLING_PCT_2025
else:
    ZELFSTANDIGENAFTREK = ZELFSTANDIGENAFTREK_2024
    STARTERSAFTREK = STARTERSAFTREK_2024
    MKB_WINSTVRIJSTELLING_PCT = MKB_WINSTVRIJSTELLING_PCT_2024


# Zorgtoeslag – officiële staffels Belastingdienst per jaar
# Bron: https://www.belastingdienst.nl/wps/wcm/connect/nl/zorgtoeslag/content/hoeveel-zorgtoeslag
ZORGTOESLAG_2025 = {
    "single": [
        (0, 123.0),      # 0 - 25.000: €123 per maand
        (25_000, 123.0), # 25.000 - 26.000: €123 per maand  
        (26_000, 123.0), # 26.000 - 27.000: €123 per maand
        (27_000, 123.0), # 27.000 - 28.000: €123 per maand
        (28_000, 123.0), # 28.000 - 29.000: €123 per maand
        (29_000, 123.0), # 29.000 - 30.000: €123 per maand
        (30_000, 123.0), # 30.000 - 31.000: €123 per maand
        (31_000, 123.0), # 31.000 - 32.000: €123 per maand
        (32_000, 123.0), # 32.000 - 33.000: €123 per maand
        (33_000, 123.0), # 33.000 - 34.000: €123 per maand
        (34_000, 123.0), # 34.000 - 35.000: €123 per maand
        (35_000, 123.0), # 35.000 - 36.000: €123 per maand
        (36_000, 123.0), # 36.000 - 37.000: €123 per maand
        (37_000, 123.0), # 37.000 - 38.000: €123 per maand
        (38_000, 123.0), # 38.000 - 39.000: €123 per maand
        (39_000, 123.0), # 39.000 - 39.719: €123 per maand
        (39_719, 0.0),   # 39.719+: geen zorgtoeslag
    ],
    "partner": [
        (0, 246.0),      # 0 - 30.000: €246 per maand
        (30_000, 246.0), # 30.000 - 31.000: €246 per maand
        (31_000, 246.0), # 31.000 - 32.000: €246 per maand
        (32_000, 246.0), # 32.000 - 33.000: €246 per maand
        (33_000, 246.0), # 33.000 - 34.000: €246 per maand
        (34_000, 246.0), # 34.000 - 35.000: €246 per maand
        (35_000, 246.0), # 35.000 - 36.000: €246 per maand
        (36_000, 246.0), # 36.000 - 37.000: €246 per maand
        (37_000, 246.0), # 37.000 - 38.000: €246 per maand
        (38_000, 246.0), # 38.000 - 39.000: €246 per maand
        (39_000, 246.0), # 39.000 - 40.000: €246 per maand
        (40_000, 246.0), # 40.000 - 41.000: €246 per maand
        (41_000, 246.0), # 41.000 - 42.000: €246 per maand
        (42_000, 246.0), # 42.000 - 43.000: €246 per maand
        (43_000, 246.0), # 43.000 - 44.000: €246 per maand
        (44_000, 246.0), # 44.000 - 45.000: €246 per maand
        (45_000, 246.0), # 45.000 - 46.000: €246 per maand
        (46_000, 246.0), # 46.000 - 47.000: €246 per maand
        (47_000, 246.0), # 47.000 - 48.000: €246 per maand
        (48_000, 246.0), # 48.000 - 49.000: €246 per maand
        (49_000, 246.0), # 49.000 - 50.000: €246 per maand
        (50_000, 246.0), # 50.000 - 50.206: €246 per maand
        (50_206, 0.0),   # 50.206+: geen zorgtoeslag
    ]
}

ZORGTOESLAG_2024 = {
    "single": [
        (0, 120.0),      # 0 - 24.000: €120 per maand
        (24_000, 120.0), # 24.000 - 25.000: €120 per maand
        (25_000, 120.0), # 25.000 - 26.000: €120 per maand
        (26_000, 120.0), # 26.000 - 27.000: €120 per maand
        (27_000, 120.0), # 27.000 - 28.000: €120 per maand
        (28_000, 120.0), # 28.000 - 29.000: €120 per maand
        (29_000, 120.0), # 29.000 - 30.000: €120 per maand
        (30_000, 120.0), # 30.000 - 31.000: €120 per maand
        (31_000, 120.0), # 31.000 - 32.000: €120 per maand
        (32_000, 120.0), # 32.000 - 33.000: €120 per maand
        (33_000, 120.0), # 33.000 - 34.000: €120 per maand
        (34_000, 120.0), # 34.000 - 35.000: €120 per maand
        (35_000, 120.0), # 35.000 - 36.000: €120 per maand
        (36_000, 120.0), # 36.000 - 37.000: €120 per maand
        (37_000, 120.0), # 37.000 - 38.000: €120 per maand
        (38_000, 120.0), # 38.000 - 38.520: €120 per maand
        (38_520, 0.0),   # 38.520+: geen zorgtoeslag
    ],
    "partner": [
        (0, 240.0),      # 0 - 29.000: €240 per maand
        (29_000, 240.0), # 29.000 - 30.000: €240 per maand
        (30_000, 240.0), # 30.000 - 31.000: €240 per maand
        (31_000, 240.0), # 31.000 - 32.000: €240 per maand
        (32_000, 240.0), # 32.000 - 33.000: €240 per maand
        (33_000, 240.0), # 33.000 - 34.000: €240 per maand
        (34_000, 240.0), # 34.000 - 35.000: €240 per maand
        (35_000, 240.0), # 35.000 - 36.000: €240 per maand
        (36_000, 240.0), # 36.000 - 37.000: €240 per maand
        (37_000, 240.0), # 37.000 - 38.000: €240 per maand
        (38_000, 240.0), # 38.000 - 39.000: €240 per maand
        (39_000, 240.0), # 39.000 - 40.000: €240 per maand
        (40_000, 240.0), # 40.000 - 41.000: €240 per maand
        (41_000, 240.0), # 41.000 - 42.000: €240 per maand
        (42_000, 240.0), # 42.000 - 43.000: €240 per maand
        (43_000, 240.0), # 43.000 - 44.000: €240 per maand
        (44_000, 240.0), # 44.000 - 45.000: €240 per maand
        (45_000, 240.0), # 45.000 - 46.000: €240 per maand
        (46_000, 240.0), # 46.000 - 47.000: €240 per maand
        (47_000, 240.0), # 47.000 - 48.000: €240 per maand
        (48_000, 240.0), # 48.000 - 49.000: €240 per maand
        (49_000, 240.0), # 49.000 - 49.000: €240 per maand
        (49_000, 0.0),   # 49.000+: geen zorgtoeslag
    ]
}

if gekozen_jaar == 2025:
    ZT_CFG = ZORGTOESLAG_2025
else:
    ZT_CFG = ZORGTOESLAG_2024


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
    max_korting = ALG["MAX"]
    start = ALG["START"]
    nihil = ALG["NIHIL"]
    if grondslag <= start:
        return max_korting
    if grondslag >= nihil:
        return 0.0
    # lineaire afbouw
    verhouding = (grondslag - start) / (nihil - start)
    return max(max_korting * (1 - verhouding), 0.0)


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


def arbeidskorting_details(arbeidsinkomenEuro: float) -> Dict[str, str]:
    y = max(float(arbeidsinkomenEuro), 0.0)
    if y <= 12_169:
        bracket = "1: ≤ € 12.169 (8,053%)"
    elif y <= 26_288:
        bracket = "2: € 12.169–€ 26.288 (30,030%)"
    elif y <= 43_071:
        bracket = "3: € 26.288–€ 43.071 (2,258%)"
    elif y <= 129_078:
        bracket = "4: € 43.071–€ 129.078 (afbouw 6,510%)"
    else:
        bracket = "> € 129.078 (0)"
    return {
        "arbeidsinkomen": y,
        "bracket": bracket,
        "korting": computeArbeidskorting(y),
    }


def zvw_bijdrage(ondernemingswinst: float, overig_werk: float) -> float:
    bijdragegrondslag = max(min(ondernemingswinst + overig_werk, ZVW_CFG["MAX_INKOMEN"]), 0.0)
    return bijdragegrondslag * ZVW_CFG["PCT"]


def premie_volksverzekeringen(belastbaar_inkomen: float) -> Tuple[float, Dict[str, float], float]:
    """Bereken premies volksverzekeringen over inkomen t/m schijf-1 grens.
    Retourneert: (grondslag, breakdown, totaal)
    """
    grondslag = max(min(belastbaar_inkomen, BRACKETS_IB[0][0]), 0.0)
    aow = grondslag * VV_CFG["AOW"]
    anw = grondslag * VV_CFG["ANW"]
    wlz = grondslag * VV_CFG["WLZ"]
    totaal = aow + anw + wlz
    return grondslag, {"AOW": aow, "Anw": anw, "Wlz": wlz}, totaal


def bereken_zorgtoeslag(per_jaar_inkomen: float, heeft_partner: bool) -> Tuple[float, Dict[str, float]]:
    """Officiële zorgtoeslag-berekening volgens Belastingdienst-staffels.
    
    Gebruikt de exacte inkomensgrenzen en bedragen per jaar. Berekent
    een maandbedrag en jaarbedrag op basis van de officiële staffels.
    """
    staffel = ZT_CFG["partner" if heeft_partner else "single"]
    
    # Zoek het juiste staffel-segment op basis van inkomen
    per_month = 0.0
    for i, (grens, bedrag) in enumerate(staffel):
        if per_jaar_inkomen <= grens:
            per_month = bedrag
            break
    
    return per_month * 12.0, {"per_maand": per_month}


# ------------------------------
# UI – invoer
# ------------------------------
st.title(f"Belastingcalculator {gekozen_jaar} – Box 1")


inkomens: Dict[str, float] = {"loondienst": 0.0, "onderneming": 0.0, "overig": 0.0, "ww": 0.0}
bron_loon = bron_onderneming = bron_overig = bron_ww = False
ondernemers_aftrek = 0.0
urencriterium_gehaald = False
kies_starters = False
kies_zsa = False
kies_mkb = False

# Helpers voor gekoppelde slider + number input
def _init_dual_input(base_key: str) -> None:
    if f"{base_key}_value" not in st.session_state:
        st.session_state[f"{base_key}_value"] = 0
    if f"{base_key}_slider" not in st.session_state:
        st.session_state[f"{base_key}_slider"] = st.session_state[f"{base_key}_value"]
    if f"{base_key}_num" not in st.session_state:
        st.session_state[f"{base_key}_num"] = str(st.session_state[f"{base_key}_value"])  # text input expects str


def _sync_from_slider(base_key: str, min_v: int, max_v: int) -> None:
    v = int(st.session_state.get(f"{base_key}_slider", 0))
    v = max(min(v, max_v), min_v)
    st.session_state[f"{base_key}_value"] = v
    st.session_state[f"{base_key}_num"] = str(v)


def _sync_from_number(base_key: str, min_v: int, max_v: int) -> None:
    raw = st.session_state.get(f"{base_key}_num", "0")
    try:
        v = int(str(raw).replace(".", "").replace(",", "").strip() or 0)
    except Exception:
        v = 0
    v = max(min(v, max_v), min_v)
    st.session_state[f"{base_key}_value"] = v
    # Clamp slider (visual) to its UI max (100k)
    st.session_state[f"{base_key}_slider"] = min(v, 100_000)

col1, col2, col3, col4 = st.columns(4)
with col1:
    with st.expander("Loondienst", expanded=True):
        bron_loon = st.checkbox("Actief", value=False, key="bron_loon_actief")
        if bron_loon:
            _init_dual_input("loon")
            sl_col, num_col = st.columns((2, 1))
            with sl_col:
                st.slider(
                    "Bruto jaarsalaris",
                    min_value=0,
                    max_value=100_000,
                    step=500,
                    key="loon_slider",
                    on_change=_sync_from_slider,
                    args=("loon", 0, 1_000_000),
                )
            with num_col:
                st.text_input("Of voer hier in...", value=str(st.session_state["loon_num"]), key="loon_num", on_change=_sync_from_number, args=("loon", 0, 1_000_000))
            inkomens["loondienst"] = float(st.session_state["loon_value"])  # unified waarde
            st.caption("Bruto jaarsalaris.")
with col2:
    with st.expander("Winst uit onderneming", expanded=True):
        bron_onderneming = st.checkbox("Actief", value=False, key="bron_onderneming_actief")
        if bron_onderneming:
            _init_dual_input("wo")
            sl_col, num_col = st.columns((2, 1))
            with sl_col:
                st.slider(
                    "Winst uit onderneming",
                    min_value=0,
                    max_value=100_000,
                    step=500,
                    key="wo_slider",
                    on_change=_sync_from_slider,
                    args=("wo", 0, 1_000_000),
                )
            with num_col:
                st.text_input("Of voer hier in...", value=str(st.session_state["wo_num"]), key="wo_num", on_change=_sync_from_number, args=("wo", 0, 1_000_000))
            inkomens["onderneming"] = float(st.session_state["wo_value"])  # unified waarde
            st.markdown("<div class=\"section-title\" style=\"margin-top:.25rem\">Aftrekken</div>", unsafe_allow_html=True)
            kies_starters = st.checkbox(f"Startersaftrek ({euro(STARTERSAFTREK)})", key="kies_starters")
            kies_zsa = st.checkbox(f"Zelfstandigenaftrek (ZSA) ({euro(ZELFSTANDIGENAFTREK)})", key="kies_zsa")
            kies_mkb = st.checkbox(f"MKB-winstvrijstelling toepassen ({MKB_WINSTVRIJSTELLING_PCT*100:.2f}%)", value=True, key="kies_mkb")
            with st.expander("Wat houden deze aftrekken in?", expanded=False):
                st.markdown(
                    "- Startersaftrek: extra aftrek voor beginnende ondernemers (binnen 5 jaar beperkt toepasbaar).\n"
                    "- Zelfstandigenaftrek (ZSA): vaste aftrek voor ondernemers die voldoen aan het urencriterium (≥ 1.225 uur) en winst uit onderneming hebben.")
with col3:
    with st.expander("Winst uit overig werk", expanded=True):
        bron_overig = st.checkbox("Actief", value=False, key="bron_overig_actief")
        if bron_overig:
            _init_dual_input("ow")
            sl_col, num_col = st.columns((2, 1))
            with sl_col:
                st.slider(
                    "Winst uit overig werk",
                    min_value=0,
                    max_value=100_000,
                    step=500,
                    key="ow_slider",
                    on_change=_sync_from_slider,
                    args=("ow", 0, 1_000_000),
                )
            with num_col:
                st.text_input("Of voer hier in...", value=str(st.session_state["ow_num"]), key="ow_num", on_change=_sync_from_number, args=("ow", 0, 1_000_000))
            inkomens["overig"] = float(st.session_state["ow_value"])  # unified waarde

with col4:
    with st.expander("Uitkering", expanded=True):
        bron_ww = st.checkbox("Actief", value=False, key="bron_ww_actief")
        if bron_ww:
            _init_dual_input("ww")
            sl_col, num_col = st.columns((2, 1))
            with sl_col:
                st.slider(
                    "WW-uitkering",
                    min_value=0,
                    max_value=100_000,
                    step=500,
                    key="ww_slider",
                    on_change=_sync_from_slider,
                    args=("ww", 0, 1_000_000),
                )
            with num_col:
                st.text_input(
                    "Of voer hier in...",
                    value=str(st.session_state["ww_num"]),
                    key="ww_num",
                    on_change=_sync_from_number,
                    args=("ww", 0, 1_000_000),
                )
            inkomens["ww"] = float(st.session_state["ww_value"])  # unified waarde
            st.caption("Uitkering telt mee voor volksverzekeringen (AOW/Anw/Wlz), maar niet voor de ZVW-bijdrage via aanslag.")

if bron_onderneming:
    if kies_starters:
        ondernemers_aftrek += STARTERSAFTREK
    if kies_zsa:
        ondernemers_aftrek += ZELFSTANDIGENAFTREK


# ------------------------------
# Berekeningen
# ------------------------------
bel_loon = max(inkomens["loondienst"], 0.0)
bel_overig = max(inkomens["overig"], 0.0)
bruto_winst_onderneming = max(inkomens["onderneming"], 0.0)
ondernemingsgrondslag_na_oa = max(bruto_winst_onderneming - ondernemers_aftrek, 0.0)
mkb_winstvrijstelling = (ondernemingsgrondslag_na_oa * MKB_WINSTVRIJSTELLING_PCT) if (bron_onderneming and kies_mkb) else 0.0
bel_onderneming = max(ondernemingsgrondslag_na_oa - mkb_winstvrijstelling, 0.0)

totale_belastbare_grondslag = bel_loon + bel_overig + bel_onderneming + max(inkomens.get("ww", 0.0), 0.0)

# Heffingskortingen
# Arbeidskorting: berekend op arbeidsinkomen (loondienst, winst uit onderneming, resultaat overige werkzaamheden).
# Let op: WW-uitkering telt NIET mee voor arbeidskorting.
# Voor ondernemers: gebruik winst vóór ondernemersaftrek en vóór MKB-winstvrijstelling.
arbeidsinkomen_korting = (
    max(inkomens["loondienst"], 0.0)
    + max(inkomens["overig"], 0.0)
    + (max(inkomens["onderneming"], 0.0) if bron_onderneming else 0.0)
)
ak = arbeidskorting(arbeidsinkomen_korting)
ahk = algemene_heffingskorting(totale_belastbare_grondslag)

# Inkomstenbelasting per schijf (IB)
schijven_ib = bereken_schijven(totale_belastbare_grondslag, BRACKETS_IB)
belasting_bruto_ib = sum(bedrag for _, _, bedrag in schijven_ib)

# Netto IB na kortingen (niet negatief)
# Let op: in de praktijk verlaagt arbeidskorting de te betalen belasting, niet het belastbare inkomen.
ak_rounded = round(ak)
ahk_rounded = round(ahk)
belasting_netto = max(belasting_bruto_ib - ak_rounded - ahk_rounded, 0.0)

# ZVW – alleen over ondernemingswinst + overig werk (WW is loon uit uitkering, geen ZVW via aanslag)
zvw = zvw_bijdrage(bel_onderneming, bel_overig)

# Volksverzekeringen – berekend los van IB
vv_grondslag, vv_parts, vv_totaal = premie_volksverzekeringen(totale_belastbare_grondslag)

# IB + VV na heffingskortingen (zoals Belastingdienst presenteert)
ib_vv_na_kortingen = max(belasting_bruto_ib + vv_totaal - (ak_rounded + ahk_rounded), 0.0)

# ------------------------------
# Samenvatting bovenaan – totaal belastbaar inkomen
# ------------------------------
st.markdown("<div class=\"section-title\">Totaal inkomen</div>", unsafe_allow_html=True)
st.markdown(
    f"""
<div class="card">
  <div>Loondienst: {euro(max(inkomens.get('loondienst', 0.0), 0.0))}</div>
  <div>Winst uit onderneming (bruto): {euro(max(inkomens.get('onderneming', 0.0), 0.0))}</div>
  <div>Winst uit overig werk: {euro(max(inkomens.get('overig', 0.0), 0.0))}</div>
  <div>WW-uitkering: {euro(max(inkomens.get('ww', 0.0), 0.0))}</div>
  <div class="metric">Totaal: {euro(max(inkomens.get('loondienst',0.0),0.0) + max(inkomens.get('onderneming',0.0),0.0) + max(inkomens.get('overig',0.0),0.0) + max(inkomens.get('ww',0.0),0.0))}</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("<div class=\"section-title\">Totaal belastbaar inkomen</div>", unsafe_allow_html=True)
st.markdown(
    f"""
<div class="card">
  <div>Loondienst: {euro(bel_loon)}</div>
  <div>Winst uit onderneming (na aftrekken): {euro(bel_onderneming)}</div>
  <div>Winst uit overig werk: {euro(bel_overig)}</div>
  <div>WW-uitkering: {euro(max(inkomens.get('ww', 0.0), 0.0))}</div>
  <div class="metric">Totaal belastbaar: {euro(totale_belastbare_grondslag)}</div>
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

# Extra kaart voor uitkering (in rij eronder voor consistentie)
colu1, colu2, colu3 = st.columns(3)
with colu1:
    st.markdown(
        f"""
<div class="card">
  <strong>Uitkering (WW)</strong>
  <div>Belastbaar: {euro(max(inkomens.get('ww', 0.0), 0.0))}</div>
  <div class="muted">Telt mee voor VV AOW Anw Wlz. Telt niet mee voor arbeidskorting en niet voor ZVW via aanslag.</div>
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
zvw_grondslag = min(bel_onderneming + bel_overig, ZVW_CFG["MAX_INKOMEN"])
st.markdown(
    f"""
<div class="card">
  <div>Belastbare winst uit onderneming + overig werk: {euro(bel_onderneming + bel_overig)}</div>
  <div>Grondslag ZVW (gemaximeerd op {euro(ZVW_CFG["MAX_INKOMEN"])}): {euro(zvw_grondslag)}</div>
  <div>Bijdragepercentage: {ZVW_CFG["PCT"]*100:.2f}%</div>
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
  <div>Algemene heffingskorting (verlaagt belasting): <strong>{euro(ahk_rounded)}</strong></div>
  <div>Arbeidskorting (verlaagt belasting): <strong>{euro(ak_rounded)}</strong></div>
  <div class="muted">Arbeidsinkomen voor arbeidskorting: {euro(arbeidsinkomen_korting)} ({arbeidskorting_details(arbeidsinkomen_korting)['bracket']})</div>
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

# Verborgen tool: Zorgtoeslag (klap in, standaard dicht)
with st.expander("Zorgtoeslag – officiële berekening (optioneel)", expanded=False):
    st.caption("Officiële berekening volgens Belastingdienst-staffels o.b.v. toetsingsinkomen (hier: totaal belastbaar inkomen) en partnerstatus.")
    
    # Invoer voor toetsingsinkomen
    colzt1, colzt2 = st.columns([1,1])
    with colzt1:
        gebruik_belastbaar = st.checkbox("Gebruik totaal belastbaar inkomen als toetsingsinkomen", value=True)
        toetsingsinkomen = totale_belastbare_grondslag if gebruik_belastbaar else st.number_input("Toetsingsinkomen (per jaar)", min_value=0, value=int(totale_belastbare_grondslag))
    
    with colzt2:
        heeft_partner = st.checkbox("Ik heb een toeslagpartner", value=False)
    
    # Partner inkomen invoer (alleen zichtbaar als partner is geselecteerd)
    partner_inkomen = 0.0
    if heeft_partner:
        st.markdown("<div class=\"section-title\">Partner inkomen</div>", unsafe_allow_html=True)
        partner_inkomen = st.number_input("Inkomen toeslagpartner (per jaar)", min_value=0, value=0, help="Voer het inkomen van je toeslagpartner in voor de verzamelinkomen berekening")
        
        # Bereken verzamelinkomen (gecombineerd inkomen)
        verzamelinkomen = float(toetsingsinkomen) + float(partner_inkomen)
        st.markdown(
            f"""
<div class="card">
  <div>Jouw toetsingsinkomen: {euro(float(toetsingsinkomen))}</div>
  <div>Partner inkomen: {euro(float(partner_inkomen))}</div>
  <div class="metric">Verzamelinkomen: {euro(verzamelinkomen)}</div>
</div>
""",
            unsafe_allow_html=True,
        )
        
        # Gebruik verzamelinkomen voor zorgtoeslag berekening
        toetsingsinkomen_final = verzamelinkomen
    else:
        toetsingsinkomen_final = float(toetsingsinkomen)

    zt_jaar, meta = bereken_zorgtoeslag(toetsingsinkomen_final, bool(heeft_partner))
    zt_maand = meta["per_maand"]

    st.markdown(
        f"""
<div class="card">
  <div>Toetsingsinkomen: {euro(toetsingsinkomen_final)}</div>
  <div>Situatie: {'met partner' if heeft_partner else 'alleenstaand'}</div>
  <div>Zorgtoeslag per maand: <strong>{euro(zt_maand)}</strong></div>
  <div>Zorgtoeslag per jaar: <strong>{euro(zt_jaar)}</strong></div>
</div>
""",
        unsafe_allow_html=True,
    )

if gekozen_jaar == 2025:
    st.caption(
        "Indicatieve berekening 2025. Tarieven: 35,82% / 37,48% / 49,50%. "
        "Heffingskortingen en ZVW benaderd voor snelle inschatting."
    )
else:
    st.caption(
        "Indicatieve berekening 2024. Tarieven: 36,97% / 49,50%. "
        "Heffingskortingen en ZVW benaderd voor snelle inschatting."
    )

