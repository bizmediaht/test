"""Résultats mesurés — Bwat Sekrèm Talks (Cap-Haïtien, 22 novembre 2026).

Données extraites de la base du système d'inscription le 24/11/2026.
Places demandées = places réservées sur le formulaire (participant + accompagnants), annulations comprises.
"""
from html import escape

CAPACITY = 300
LAUNCH = "2026-11-06"
# Places demandées par jour (06/11 → 22/11 ; le 22 = inscriptions sur place)
DAILY_PLACES = [("06/11", 49), ("07/11", 25), ("08/11", 14), ("09/11", 17), ("10/11", 45), ("11/11", 34), ("12/11", 23),
                ("13/11", 9), ("14/11", 16), ("15/11", 10), ("16/11", 30), ("17/11", 43), ("18/11", 24), ("19/11", 33),
                ("20/11", 32), ("21/11", 0), ("22/11", 11)]
# Jour J : entrées pointées par tranche de 15 minutes (heure d'Haïti)
CHECKIN = [("13:45", 2), ("14:00", 1), ("14:15", 32), ("14:30", 29), ("14:45", 32), ("15:00", 33), ("15:15", 23),
           ("15:30", 17), ("15:45", 5), ("16:00", 2), ("16:15", 6), ("16:30", 4), ("16:45", 2)]
# Taux de présence : inscriptions pointées / inscriptions actives
CONFIRMED = (137, 247)      # confirmées par WhatsApp
NOT_CONFIRMED = (32, 79)    # non confirmées
REACHED = (348, 374)        # inscrits ayant reçu au moins un message
RATING = (4.89, 9)

# Public : 326 inscriptions actives (hors annulations). Profils à choix multiples (53 personnes en ont coché plusieurs).
AUD_N = 326
PROFILES = [("etudiant", 203, 93), ("employe", 76, 41), ("proprietaire", 51, 29), ("cadre", 16, 7), ("autre", 44, 22)]  # (clé, inscrits, présents)
GENDER = [("femme", 201), ("homme", 124)]          # 1 non renseigné
CITY = [("cap", 283), ("nord", 18), ("pap", 11), ("autre", 14)]
SOURCES = [("ami", 140), ("whatsapp", 131), ("instagram", 14), ("affiche", 13), ("surplace", 11), ("facebook", 6), ("autre", 11)]
AUD_TXT = {
    "fr": dict(title="Qui était dans la salle ?", sub="326 inscriptions actives · profils déclarés à l’inscription",
               prof="Profil professionnel", profs="Plusieurs choix possibles : le total dépasse 100 %",
               gen="Répartition femmes / hommes", city="Ville de provenance", src="Comment ils ont connu l’événement",
               tip="{l} : {n} inscrits ({p} %)", tipP="{l} : {n} inscrits ({p} %) · {r} % présents le jour J",
               lab=dict(etudiant="Étudiants", employe="Employés", proprietaire="Entrepreneurs", cadre="Cadres", autre="Autres",
                        femme="Femmes", homme="Hommes", cap="Cap-Haïtien", nord="Autres communes du Nord", pap="Port-au-Prince",
                        ami="Un ami / un collègue", whatsapp="WhatsApp", instagram="Instagram", affiche="Affiche",
                        surplace="Sur place (jour J)", facebook="Facebook"),
               insight="Les entrepreneurs ont le meilleur taux de présence ({a} %), devant les étudiants ({b} %).",
               insight2="83 % des inscriptions viennent du bouche-à-oreille et de WhatsApp.",
               cols=("Groupe", "Inscrits", "Part", "Présents")),
    "en": dict(title="Who was in the room?", sub="326 active registrations · profiles declared at sign-up",
               prof="Professional profile", profs="Multiple choices allowed: totals exceed 100%",
               gen="Women / men split", city="Home city", src="How they heard about the event",
               tip="{l}: {n} registrants ({p}%)", tipP="{l}: {n} registrants ({p}%) · {r}% attended",
               lab=dict(etudiant="Students", employe="Employees", proprietaire="Business owners", cadre="Managers", autre="Other",
                        femme="Women", homme="Men", cap="Cap-Haïtien", nord="Other towns in the North", pap="Port-au-Prince",
                        ami="A friend / colleague", whatsapp="WhatsApp", instagram="Instagram", affiche="Poster",
                        surplace="On site (event day)", facebook="Facebook"),
               insight="Business owners had the best attendance rate ({a}%), ahead of students ({b}%).",
               insight2="83% of registrations came from word of mouth and WhatsApp.",
               cols=("Group", "Registrants", "Share", "Attended")),
}

GOLD, GRID, AXIS, MUTED, SURF = "#F5B841", "#334155", "#94A3B8", "#64748B", "#1E293B"

TXT = {
    "fr": dict(
        eyebrow="Résultats mesurés", title="Bwat Sekrèm Talks : les chiffres, pas des promesses.",
        lead="Conférence à Cap-Haïtien, 22 novembre 2026. Inscriptions, confirmations WhatsApp et pointage gérés par notre système.",
        k1="de la salle réservée en 5 jours", k2="de demande par rapport à la capacité", k3="des inscrits joints sur WhatsApp",
        k4="note moyenne des participants", k4s="9 avis",
        c1="Places demandées, cumul jour par jour", c1s="Capacité : 300 places · lancement le 6 novembre",
        cap="Capacité 300", a5="J+5 : 150 places", afull="Salle pleine le 17/11", aend="415 demandées",
        c2="Jour J : entrées pointées par tranche de 15 min", c2s="188 personnes accueillies · pic à 15 h 00",
        apeak="126 entrées en 1 h", c3="Taux de présence le jour J", c3s="Part des inscrits venus à l’événement",
        conf="Confirmés sur WhatsApp", nconf="Non confirmés", gain="+{p} points de présence chez les inscrits confirmés",
        data="Voir les données", day="Jour", places="Places (cumul)", slot="Heure", entries="Entrées",
        group="Groupe", rate="Présence", source="Source : système d’inscription BiZ, données du 6 au 22 novembre 2026. Présence = inscriptions pointées à l’entrée.",
        tipDay="{d} : {n} places ({c} au total)", tipSlot="{t} : {n} entrées", nb=lambda n: f"{n:,}".replace(",", " ")),
    "en": dict(
        eyebrow="Measured results", title="Bwat Sekrèm Talks: numbers, not promises.",
        lead="Conference in Cap-Haïtien, November 22, 2026. Registrations, WhatsApp confirmations and check-in run on our system.",
        k1="of the room booked in 5 days", k2="demand vs. capacity", k3="of registrants reached on WhatsApp",
        k4="average attendee rating", k4s="9 reviews",
        c1="Seats requested, cumulative by day", c1s="Capacity: 300 seats · launched November 6",
        cap="Capacity 300", a5="Day 5: 150 seats", afull="Full on Nov 17", aend="415 requested",
        c2="Event day: check-ins per 15 minutes", c2s="188 people welcomed · peak at 3:00 pm",
        apeak="126 check-ins in 1 hour", c3="Event-day attendance rate", c3s="Share of registrants who showed up",
        conf="Confirmed on WhatsApp", nconf="Not confirmed", gain="+{p} points of attendance among confirmed registrants",
        data="See the data", day="Day", places="Seats (cumulative)", slot="Time", entries="Check-ins",
        group="Group", rate="Attendance", source="Source: BiZ registration system, data from November 6 to 22, 2026. Attendance = registrations checked in at the door.",
        tipDay="{d}: {n} seats ({c} total)", tipSlot="{t}: {n} check-ins", nb=lambda n: f"{n:,}"),
}


def e(s):
    return escape(str(s), quote=True)


def pct(a, b):
    return round(100 * a / b)


def chart_cumulative(t):
    W, H, L, R, T, B = 640, 280, 44, 16, 20, 34
    cum, c = [], 0
    for d, n in DAILY_PLACES:
        c += n
        cum.append((d, n, c))
    ymax = 450
    x = lambda i: L + i * (W - L - R) / (len(cum) - 1)
    y = lambda v: T + (H - T - B) * (1 - v / ymax)
    grid = "".join(f'<line x1="{L}" x2="{W-R}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="{GRID}" stroke-width="1"/>'
                   f'<text x="{L-8}" y="{y(v)+4:.1f}" text-anchor="end" class="ax">{v}</text>' for v in (0, 100, 200, 300, 400))
    xt = "".join(f'<text x="{x(i):.1f}" y="{H-12}" text-anchor="{"start" if i == 0 else "end" if i == len(cum) - 1 else "middle"}" class="ax">{d}</text>'
                 for i, (d, _, _) in enumerate(cum) if i % 4 == 0 or i == len(cum) - 1)
    pts = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, (_, _, v) in enumerate(cum))
    area = f'M{x(0):.1f},{y(0):.1f} L' + " L".join(f"{x(i):.1f},{y(v):.1f}" for i, (_, _, v) in enumerate(cum)) + f' L{x(len(cum)-1):.1f},{y(0):.1f} Z'
    full_i = next(i for i, (_, _, v) in enumerate(cum) if v >= CAPACITY)
    ann = [(4, cum[4][2], t["a5"], "start", 22), (full_i, cum[full_i][2], t["afull"], "end", -12), (len(cum) - 1, cum[-1][2], t["aend"], "end", -12)]
    marks = "".join(f'<circle cx="{x(i):.1f}" cy="{y(v):.1f}" r="5" fill="{GOLD}" stroke="{SURF}" stroke-width="2"/>'
                    f'<text x="{x(i) + (8 if a == "start" else -8):.1f}" y="{y(v)+dy:.1f}" text-anchor="{a}" class="lbl">{e(s)}</text>'
                    for i, v, s, a, dy in ann)
    step = (W - L - R) / (len(cum) - 1)
    hits = "".join(f'<rect x="{x(i)-step/2:.1f}" y="{T}" width="{step:.1f}" height="{H-T-B}" fill="transparent" tabindex="0" '
                   f'data-tip="{e(t["tipDay"].format(d=d, n=n, c=c))}" aria-label="{e(t["tipDay"].format(d=d, n=n, c=c))}"/>'
                   for i, (d, n, c) in enumerate(cum))
    cap = (f'<line x1="{L}" x2="{W-R}" y1="{y(CAPACITY):.1f}" y2="{y(CAPACITY):.1f}" stroke="{AXIS}" stroke-width="1.5"/>'
           f'<text x="{L+6}" y="{y(CAPACITY)-6:.1f}" class="lbl muted">{e(t["cap"])}</text>')
    svg = (f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{e(t["c1"])}">{grid}{xt}{cap}'
           f'<path d="{area}" fill="{GOLD}" fill-opacity=".1"/>'
           f'<polyline points="{pts}" fill="none" stroke="{GOLD}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>'
           f'{marks}{hits}</svg>')
    rows = "".join(f"<tr><td>{d}</td><td>{n}</td><td>{c}</td></tr>" for d, n, c in cum)
    table = f'<table><thead><tr><th>{e(t["day"])}</th><th>+</th><th>{e(t["places"])}</th></tr></thead><tbody>{rows}</tbody></table>'
    return svg, table


def chart_checkin(t):
    W, H, L, R, T, B = 420, 250, 30, 6, 34, 30
    ymax = 40
    n = len(CHECKIN)
    slot = (W - L - R) / n
    bw = min(24, slot - 6)
    y = lambda v: T + (H - T - B) * (1 - v / ymax)
    grid = "".join(f'<line x1="{L}" x2="{W-R}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="{GRID}" stroke-width="1"/>'
                   f'<text x="{L-8}" y="{y(v)+4:.1f}" text-anchor="end" class="ax">{v}</text>' for v in (0, 10, 20, 30, 40))
    bars, labels, hits = "", "", ""
    peak = max(v for _, v in CHECKIN)
    for i, (tm, v) in enumerate(CHECKIN):
        cx = L + slot * i + slot / 2
        top, base = y(v), y(0)
        r = min(4, (base - top) / 2)
        x0, x1 = cx - bw / 2, cx + bw / 2
        path = (f"M{x0:.1f},{base:.1f} L{x0:.1f},{top+r:.1f} Q{x0:.1f},{top:.1f} {x0+r:.1f},{top:.1f} "
                f"L{x1-r:.1f},{top:.1f} Q{x1:.1f},{top:.1f} {x1:.1f},{top+r:.1f} L{x1:.1f},{base:.1f} Z")
        bars += f'<path d="{path}" fill="{GOLD if 2 <= i <= 5 else MUTED}"/>'
        if v == peak:
            labels += f'<text x="{cx:.1f}" y="{top-8:.1f}" text-anchor="middle" class="lbl">{v}</text>'
        if i % 2 == 0:
            labels += f'<text x="{cx:.1f}" y="{H-12}" text-anchor="middle" class="ax">{tm}</text>'
        tip = e(t["tipSlot"].format(t=tm, n=v))
        hits += f'<rect x="{cx-slot/2:.1f}" y="{T}" width="{slot:.1f}" height="{H-T-B}" fill="transparent" tabindex="0" data-tip="{tip}" aria-label="{tip}"/>'
    bx0, bx1 = L + slot * 2 + 4, L + slot * 6 - 4
    brace = (f'<line x1="{bx0:.1f}" x2="{bx1:.1f}" y1="{T-8}" y2="{T-8}" stroke="{AXIS}" stroke-width="1"/>'
             f'<text x="{(bx0+bx1)/2:.1f}" y="{T-14}" text-anchor="middle" class="lbl">{e(t["apeak"])}</text>')
    svg = f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{e(t["c2"])}" style="overflow:visible">{grid}{bars}{brace}{labels}{hits}</svg>'
    rows = "".join(f"<tr><td>{tm}</td><td>{v}</td></tr>" for tm, v in CHECKIN)
    table = f'<table><thead><tr><th>{e(t["slot"])}</th><th>{e(t["entries"])}</th></tr></thead><tbody>{rows}</tbody></table>'
    return svg, table


def chart_attendance(t):
    rows = [(t["conf"], *CONFIRMED, GOLD), (t["nconf"], *NOT_CONFIRMED, MUTED)]
    bars = "".join(f'''<div class="hb" tabindex="0" data-tip="{e(f"{lab} : {a} / {b}")}">
<span class="hb-l">{e(lab)}</span>
<span class="hb-track"><span class="hb-fill" style="width:{pct(a, b)}%;background:{col}"></span></span>
<b class="hb-v">{pct(a, b)} %</b></div>''' for lab, a, b, col in rows)
    trs = "".join(f"<tr><td>{e(lab)}</td><td>{a} / {b}</td><td>{pct(a, b)} %</td></tr>" for lab, a, b, _ in rows)
    table = f'<table><thead><tr><th>{e(t["group"])}</th><th>n</th><th>{e(t["rate"])}</th></tr></thead><tbody>{trs}</tbody></table>'
    gain = pct(*CONFIRMED) - pct(*NOT_CONFIRMED)
    return f'<div class="hbars">{bars}</div><p class="gain">{e(t["gain"].format(p=gain))}</p>', table


def audience_html(lang):
    a = AUD_TXT[lang]; L = a["lab"]; sp = " %" if lang == "fr" else "%"
    lab = lambda k: L.get(k, a["lab"]["autre"])

    def bars(rows, with_rate=False):
        out, trs = "", ""
        for r in rows:
            k, n = r[0], r[1]
            p = pct(n, AUD_N)
            tip = (a["tipP"].format(l=lab(k), n=n, p=p, r=pct(r[2], n)) if with_rate else a["tip"].format(l=lab(k), n=n, p=p))
            out += (f'<div class="hb sm" tabindex="0" data-tip="{e(tip)}"><span class="hb-l">{e(lab(k))}</span>'
                    f'<span class="hb-track"><span class="hb-fill" style="width:{p}%;background:{GOLD}"></span></span>'
                    f'<b class="hb-v">{p}{sp}</b></div>')
            trs += f"<tr><td>{e(lab(k))}</td><td>{n}</td><td>{p}{sp}</td>" + (f"<td>{pct(r[2], n)}{sp}</td>" if with_rate else "") + "</tr>"
        cols = a["cols"] if with_rate else a["cols"][:3]
        table = "<table><thead><tr>" + "".join(f"<th>{e(c)}</th>" for c in cols) + f"</tr></thead><tbody>{trs}</tbody></table>"
        return f'<div class="hbars">{out}</div>', table

    def card(title, sub, rows, with_rate=False, note=""):
        body, table = bars(rows, with_rate)
        return (f'<figure class="chart"><figcaption><b>{e(title)}</b>{f"<span>{e(sub)}</span>" if sub else ""}</figcaption>{body}'
                f'{f"<p class=gain>{e(note)}</p>" if note else ""}'
                f'<details class="data"><summary>{e(TXT[lang]["data"])}</summary>{table}</details></figure>')
    rate = {k: pct(p, n) for k, n, p in PROFILES}
    return f'''<div class="aud-head"><h3>{e(a["title"])}</h3><p>{e(a["sub"])}</p></div>
<div class="charts">
{card(a["prof"], a["profs"], PROFILES, True, a["insight"].format(a=rate["proprietaire"], b=rate["etudiant"]))}
{card(a["src"], "", SOURCES, note=a["insight2"])}
{card(a["gen"], "", GENDER)}
{card(a["city"], "", CITY)}
</div>'''


def proof_html(lang, more_link=""):
    t = TXT[lang]
    booked5 = sum(n for _, n in DAILY_PLACES[:5])
    demand = sum(n for _, n in DAILY_PLACES)
    rating = f"{RATING[0]:.1f}".replace(".", "," if lang == "fr" else ".")
    kpis = [(f"{pct(booked5, CAPACITY)} %", t["k1"], ""), (f"{pct(demand, CAPACITY)} %", t["k2"], ""),
            (f"{pct(*REACHED)} %", t["k3"], ""), (f"{rating} / 5", t["k4"], t["k4s"])]
    if lang == "en":
        kpis = [(k.replace(" %", "%"), l, s) for k, l, s in kpis]
    kp = "".join(f'<div class="kpi"><b>{e(k)}</b><span>{e(l)}</span>{f"<small>{e(s)}</small>" if s else ""}</div>' for k, l, s in kpis)

    def card(title, sub, body, table, cls=""):
        return (f'<figure class="chart {cls}"><figcaption><b>{e(title)}</b><span>{e(sub)}</span></figcaption>{body}'
                f'<details class="data"><summary>{e(t["data"])}</summary>{table}</details></figure>')
    s1, t1 = chart_cumulative(t)
    s2, t2 = chart_checkin(t)
    s3, t3 = chart_attendance(t)
    return f'''<div class="wrap proof-data">
<div class="head"><span class="eyebrow">{e(t["eyebrow"])}</span><h2>{e(t["title"])}</h2><p class="lead">{e(t["lead"])}</p></div>
<div class="kpis-row">{kp}</div>
<div class="charts">
{card(t["c1"], t["c1s"], s1, t1, "wide")}
{card(t["c2"], t["c2s"], s2, t2)}
{card(t["c3"], t["c3s"], s3, t3)}
</div>
{audience_html(lang)}
<p class="src">{e(t["source"])}{more_link}</p>
<div class="chart-tip" role="tooltip" hidden></div>
</div>'''
