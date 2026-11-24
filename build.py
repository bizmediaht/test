#!/usr/bin/env python3
"""Génère toutes les pages du site (FR + EN) à partir des textes ci-dessous.
Modifier les textes, les prix ou les coordonnées ici, puis lancer :  python3 build.py
"""
from html import escape
from pathlib import Path

SITE_URL = "https://bizmedia.ht"
CONTACT = {
    "email": "contact@bizmedia.ht",   # TODO : adresse réelle
    "whatsapp": "",                    # TODO : numéro au format 509XXXXXXXX (vide = formulaire par e-mail)
    "phone_display": "",               # TODO : ex. +509 XX XX XXXX
}

# Chemin de chaque page, par langue
PAGES = {
    "home":     {"fr": "",              "en": "en/"},
    "packages": {"fr": "forfaits/",     "en": "en/packages/"},
    "work":     {"fr": "realisations/", "en": "en/work/"},
    "about":    {"fr": "a-propos/",     "en": "en/about/"},
}

ICONS = {
    "media": '<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/>',
    "prod": '<polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2"/>',
    "digital": '<rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/><polyline points="7 10 10 12 14 8 17 10"/>',
    "corp": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    "check": '<polyline points="20 6 9 17 4 12"/>',
}
NUMS = ["374", "188", "675", "2 684"]

T = {
"fr": dict(
    htmllang="fr", skip="Aller au contenu", navLabel="Navigation principale", langLabel="Langue",
    nav=dict(services="Services", packages="Forfaits", work="Réalisations", about="À propos", quote="Demander un devis"),
    footerLinks="Pages",
    # ---------- Accueil ----------
    homeTitle="BiZ Media — Photo, vidéo, production & solutions digitales en Haïti",
    homeDesc="BiZ Media : photographie, vidéo, production, CRM et automatisation pour les entreprises et les événements en Haïti.",
    heroText="Photo, vidéo, production et systèmes digitaux — CRM, inscriptions, automatisation — réunis sous un même toit pour les entreprises et les événements en Haïti.",
    heroCta1="Parlons de votre projet", heroCta2="Voir les forfaits",
    heroPhoto="[ Photo ou vidéo d’un événement couvert par BiZ ]",
    dashTitle="Tableau de bord — Événement", dashLive="En direct", dashReg="Inscrits", dashPresent="Présents",
    svcEyebrow="Nos services", svcTitle="Quatre expertises, une seule équipe.",
    svcText="Vous n’avez plus besoin de coordonner un photographe, une agence vidéo et un développeur. BiZ s’occupe de tout.",
    services=[
        ("media", "BiZ Media", "Photographie, vidéographie et couverture d’événements.", ["Reportage photo", "Captation vidéo", "Highlights pour réseaux sociaux"]),
        ("prod", "BiZ Productions", "Interviews, documentaires et publicités.", ["Interviews & portraits", "Mini-documentaires", "Spots publicitaires"]),
        ("digital", "BiZ Digital", "CRM, automatisation et solutions digitales.", ["Inscriptions en ligne", "CRM & relances WhatsApp", "Tableaux de bord"]),
        ("corp", "BiZ Corporate", "Communication d’entreprise et services aux entreprises.", ["Identité & image de marque", "Communication interne", "Contenu institutionnel"]),
    ],
    packEyebrow="Offre phare", packTitle="Le Pack Événement Complet",
    packText="De la première inscription jusqu’au rapport final : on gère le système et on raconte l’histoire.", packCta="Voir les forfaits",
    steps=[
        ("Inscriptions en ligne", "Page et formulaire à vos couleurs, avec gestion des places."),
        ("Confirmations auto", "Messages de confirmation, relances et liste d’attente."),
        ("Pointage le jour J", "Accueil rapide et liste des présents en temps réel."),
        ("Couverture photo & vidéo", "Notre équipe capture les moments forts."),
        ("Certificats & rapport", "Certificats envoyés et bilan complet de l’événement."),
    ],
    caseEyebrow="Étude de cas",
    caseText="Formulaire d’inscription, confirmations et relances automatiques, liste d’attente, pointage à l’entrée, certificats et suivi CRM de chaque participant — un seul système, conçu et opéré par notre équipe.",
    caseCta="Voir l’étude de cas complète →",
    stats=["inscriptions", "présences pointées", "messages envoyés", "visites du site"],
    contactTitle="Racontons votre prochaine histoire.",
    contactText="Dites-nous ce que vous préparez. Nous revenons vers vous avec une proposition.",
    phoneFallback="[Téléphone / WhatsApp]", city="Haïti",
    fName="Nom complet", fCompany="Entreprise", fPhone="Téléphone", fService="Service souhaité", fProject="Votre projet", fSend="Envoyer la demande",
    options=["Pack Événement Complet", "Pack Événement Essentiel", "Couverture Média", "Contenu mensuel", "BiZ Digital — CRM / Automatisation", "Autre / sur mesure"],
    msgIntro="Bonjour BiZ Media, je souhaite un devis.", msgSubject="Demande de devis — site web",
    # ---------- Forfaits ----------
    pkTitle="Forfaits — BiZ Media", pkDesc="Les forfaits BiZ Media : événements, couverture photo & vidéo, contenu mensuel et solutions digitales.",
    pkEyebrow="Forfaits", pkH1="Des offres claires pour chaque projet.",
    pkLead="Choisissez une base, nous l’adaptons à votre événement ou à votre entreprise. Chaque projet commence par un appel gratuit.",
    pkPopular="Le plus demandé", pkFrom="À partir de", pkQuote="Sur devis", pkCta="Choisir ce forfait",
    packages=[
        dict(name="Pack Événement Essentiel", price="[Prix] HTG", per="par événement", popular=False,
             desc="Le système digital, sans la couverture média.",
             items=["Page & formulaire d’inscription", "Confirmations et relances automatiques", "Liste d’attente et gestion des places", "Pointage à l’entrée", "Rapport de participation"]),
        dict(name="Pack Événement Complet", price="[Prix] HTG", per="par événement", popular=True,
             desc="Le système digital + la couverture photo & vidéo.",
             items=["Tout le Pack Essentiel", "Photographe & vidéaste le jour J", "Vidéo highlights pour réseaux sociaux", "Certificats de participation", "Suivi CRM après l’événement"]),
        dict(name="Couverture Média", price="[Prix] HTG", per="par demi-journée", popular=False,
             desc="Photo et vidéo professionnelles pour un événement.",
             items=["Photographe professionnel", "Captation vidéo", "Photos retouchées sous [X] jours", "Vidéo récapitulative", "Livraison en ligne"]),
        dict(name="Contenu mensuel", price="[Prix] HTG", per="par mois", popular=False,
             desc="Pour les entreprises qui communiquent chaque mois.",
             items=["[X] séances photo / vidéo", "Contenus pour réseaux sociaux", "Interviews & portraits d’équipe", "Calendrier de publication", "Bilan mensuel"]),
    ],
    customTitle="Besoin d’autre chose ?",
    customText="Documentaire, spot publicitaire, CRM pour votre entreprise, automatisation WhatsApp… Nous construisons une offre sur mesure.",
    customCta="Demander un devis sur mesure",
    faqTitle="Questions fréquentes",
    faq=[
        ("Comment se passe le paiement ?", "[À compléter : acompte à la réservation, solde à la livraison, modes de paiement acceptés.]"),
        ("Combien de temps à l’avance faut-il réserver ?", "[À compléter : délai recommandé avant l’événement.]"),
        ("Travaillez-vous en dehors de Port-au-Prince ?", "[À compléter : zones couvertes et frais de déplacement.]"),
        ("Le système d’inscription fonctionne-t-il avec WhatsApp ?", "Oui. Les confirmations et les relances peuvent être envoyées par WhatsApp, et chaque participant est suivi dans le CRM."),
    ],
    # ---------- Réalisations ----------
    wkTitle="Réalisations — BiZ Media", wkDesc="Projets réalisés par BiZ Media : étude de cas Bwat Sekrèm Talks et galerie.",
    wkEyebrow="Réalisations", wkH1="Des projets qui parlent pour nous.",
    wkLead="Chaque projet combine ce que nous faisons de mieux : raconter l’histoire et faire fonctionner le système.",
    csEyebrow="Étude de cas", csClient="Client", csClientV="Bwat Sekrèm", csType="Type", csTypeV="Conférence / événement public",
    csServices="Services", csServicesV="BiZ Digital · BiZ Media",
    csChallengeT="Le défi", csChallenge="Gérer des centaines d’inscriptions, confirmer chaque participant, gérer une liste d’attente et savoir exactement qui est venu le jour de l’événement.",
    csSolutionT="La solution",
    csSolution=["Formulaire d’inscription public", "Confirmations, relances et messages d’attente automatiques", "CRM avec un responsable et des notes pour chaque personne", "Pointage des présences à l’entrée", "Envoi des certificats après l’événement"],
    csResultsT="Les résultats",
    galleryTitle="Galerie", galleryPh="[ Photo ]",
    moreTitle="Votre projet pourrait être le prochain.", moreCta="Parlons-en",
    # ---------- À propos ----------
    abTitle="À propos — BiZ Media", abDesc="BiZ Media réunit média, technologie et business pour les entreprises et les événements en Haïti.",
    abEyebrow="À propos", abH1="Média, technologie et business, sous un même toit.",
    abLead="BiZ Media est né d’un constat simple : un événement réussi a besoin d’une belle histoire et d’un système qui fonctionne. Rarement les deux chez le même prestataire.",
    storyTitle="Notre histoire",
    story=["Avant BiZ Media, nous avons conçu et opéré le système complet de Bwat Sekrèm Talks : inscriptions, confirmations automatiques, CRM, pointage et certificats.",
           "Après cet événement, plusieurs entreprises nous ont demandé la même chose. BiZ Media est la réponse : une équipe qui couvre votre événement en photo et en vidéo, et qui construit les outils digitaux qui vont avec."],
    valuesTitle="Ce qui nous guide",
    values=[("Fiabilité", "Un système qui marche le jour J, sans surprise."), ("Clarté", "Des offres et des prix compréhensibles."),
            ("Qualité", "Des images et des outils dont vous serez fiers."), ("Proximité", "Une équipe locale qui connaît le terrain.")],
    howTitle="Comment nous travaillons",
    how=[("Appel découverte", "On écoute votre projet et vos objectifs."), ("Proposition", "Un devis clair, avec le forfait adapté."),
         ("Réalisation", "Mise en place du système et couverture média."), ("Bilan", "Livraison des contenus et rapport final.")],
    teamTitle="L’équipe", teamPh="[Nom]", teamRole="[Rôle]",
),
"en": dict(
    htmllang="en", skip="Skip to content", navLabel="Main navigation", langLabel="Language",
    nav=dict(services="Services", packages="Packages", work="Our Work", about="About", quote="Get a quote"),
    footerLinks="Pages",
    homeTitle="BiZ Media — Photo, video, production & digital solutions in Haiti",
    homeDesc="BiZ Media: photography, video, production, CRM and automation for businesses and events in Haiti.",
    heroText="Photo, video, production and digital systems — CRM, registrations, automation — all under one roof for businesses and events in Haiti.",
    heroCta1="Let’s talk about your project", heroCta2="See our packages",
    heroPhoto="[ Photo or video of an event covered by BiZ ]",
    dashTitle="Event dashboard", dashLive="Live", dashReg="Registered", dashPresent="Checked in",
    svcEyebrow="Our services", svcTitle="Four areas of expertise, one team.",
    svcText="No more juggling a photographer, a video agency and a developer. BiZ handles it all.",
    services=[
        ("media", "BiZ Media", "Photography, videography and event coverage.", ["Photo reporting", "Video capture", "Social media highlights"]),
        ("prod", "BiZ Productions", "Interviews, documentaries and commercials.", ["Interviews & portraits", "Mini-documentaries", "Commercials"]),
        ("digital", "BiZ Digital", "CRM, automation and digital solutions.", ["Online registrations", "CRM & WhatsApp follow-ups", "Dashboards"]),
        ("corp", "BiZ Corporate", "Corporate communications and business services.", ["Brand identity", "Internal communications", "Institutional content"]),
    ],
    packEyebrow="Signature offer", packTitle="The Complete Event Package",
    packText="From the first registration to the final report: we run the system and tell the story.", packCta="See our packages",
    steps=[
        ("Online registration", "A branded page and form, with seat management."),
        ("Automatic confirmations", "Confirmation messages, reminders and waitlist."),
        ("Event-day check-in", "Fast welcome desk and a live attendance list."),
        ("Photo & video coverage", "Our team captures the key moments."),
        ("Certificates & report", "Certificates sent and a full event report."),
    ],
    caseEyebrow="Case study",
    caseText="Registration form, automatic confirmations and reminders, waitlist, check-in at the door, certificates and CRM follow-up for every attendee — one system, built and run by our team.",
    caseCta="Read the full case study →",
    stats=["registrations", "check-ins recorded", "messages sent", "website visits"],
    contactTitle="Let’s tell your next story.",
    contactText="Tell us what you’re planning. We’ll get back to you with a proposal.",
    phoneFallback="[Phone / WhatsApp]", city="Haiti",
    fName="Full name", fCompany="Company", fPhone="Phone", fService="Service needed", fProject="Your project", fSend="Send request",
    options=["Complete Event Package", "Essential Event Package", "Media Coverage", "Monthly Content", "BiZ Digital — CRM / Automation", "Other / custom"],
    msgIntro="Hello BiZ Media, I would like a quote.", msgSubject="Quote request — website",
    pkTitle="Packages — BiZ Media", pkDesc="BiZ Media packages: events, photo & video coverage, monthly content and digital solutions.",
    pkEyebrow="Packages", pkH1="Clear offers for every project.",
    pkLead="Pick a starting point and we tailor it to your event or business. Every project starts with a free call.",
    pkPopular="Most requested", pkFrom="From", pkQuote="On request", pkCta="Choose this package",
    packages=[
        dict(name="Essential Event Package", price="[Price] HTG", per="per event", popular=False,
             desc="The digital system, without media coverage.",
             items=["Registration page & form", "Automatic confirmations and reminders", "Waitlist and seat management", "Check-in at the door", "Attendance report"]),
        dict(name="Complete Event Package", price="[Price] HTG", per="per event", popular=True,
             desc="The digital system + photo & video coverage.",
             items=["Everything in Essential", "Photographer & videographer on the day", "Highlight video for social media", "Attendance certificates", "Post-event CRM follow-up"]),
        dict(name="Media Coverage", price="[Price] HTG", per="per half-day", popular=False,
             desc="Professional photo and video for an event.",
             items=["Professional photographer", "Video capture", "Edited photos within [X] days", "Recap video", "Online delivery"]),
        dict(name="Monthly Content", price="[Price] HTG", per="per month", popular=False,
             desc="For businesses that communicate every month.",
             items=["[X] photo / video sessions", "Social media content", "Interviews & team portraits", "Publishing calendar", "Monthly report"]),
    ],
    customTitle="Need something else?",
    customText="Documentary, commercial, a CRM for your business, WhatsApp automation… We build a custom offer.",
    customCta="Request a custom quote",
    faqTitle="Frequently asked questions",
    faq=[
        ("How does payment work?", "[To complete: deposit at booking, balance on delivery, accepted payment methods.]"),
        ("How far in advance should we book?", "[To complete: recommended lead time before the event.]"),
        ("Do you work outside Port-au-Prince?", "[To complete: areas covered and travel fees.]"),
        ("Does the registration system work with WhatsApp?", "Yes. Confirmations and reminders can be sent via WhatsApp, and every attendee is tracked in the CRM."),
    ],
    wkTitle="Our Work — BiZ Media", wkDesc="Projects by BiZ Media: Bwat Sekrèm Talks case study and gallery.",
    wkEyebrow="Our work", wkH1="Projects that speak for us.",
    wkLead="Every project combines what we do best: telling the story and making the system work.",
    csEyebrow="Case study", csClient="Client", csClientV="Bwat Sekrèm", csType="Type", csTypeV="Conference / public event",
    csServices="Services", csServicesV="BiZ Digital · BiZ Media",
    csChallengeT="The challenge", csChallenge="Handle hundreds of registrations, confirm every attendee, manage a waitlist and know exactly who showed up on the day.",
    csSolutionT="The solution",
    csSolution=["Public registration form", "Automatic confirmations, reminders and waitlist messages", "CRM with an owner and notes for every person", "Attendance check-in at the door", "Certificates sent after the event"],
    csResultsT="The results",
    galleryTitle="Gallery", galleryPh="[ Photo ]",
    moreTitle="Your project could be next.", moreCta="Let’s talk",
    abTitle="About — BiZ Media", abDesc="BiZ Media brings media, technology and business together for companies and events in Haiti.",
    abEyebrow="About", abH1="Media, technology and business, under one roof.",
    abLead="BiZ Media started from a simple observation: a successful event needs a great story and a system that works. Rarely from the same provider.",
    storyTitle="Our story",
    story=["Before BiZ Media, we designed and ran the full system behind Bwat Sekrèm Talks: registrations, automatic confirmations, CRM, check-in and certificates.",
           "After that event, several companies asked us for the same thing. BiZ Media is the answer: one team that covers your event in photo and video, and builds the digital tools that go with it."],
    valuesTitle="What guides us",
    values=[("Reliability", "A system that works on the day, no surprises."), ("Clarity", "Offers and prices that are easy to understand."),
            ("Quality", "Images and tools you’ll be proud of."), ("Proximity", "A local team that knows the ground.")],
    howTitle="How we work",
    how=[("Discovery call", "We listen to your project and goals."), ("Proposal", "A clear quote with the right package."),
         ("Delivery", "System setup and media coverage."), ("Wrap-up", "Content delivery and final report.")],
    teamTitle="The team", teamPh="[Name]", teamRole="[Role]",
),
}

def e(s): return escape(s, quote=True)

def rel(frm, to, anchor=""):
    """Lien relatif de la page `frm` vers la page `to` (chemins de PAGES)."""
    up = "../" * frm.count("/")
    target = up + to
    return (target or "./") + anchor

def svg(name, color="#F5B841", size=26):
    return f'<svg aria-hidden="true" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>'

def layout(lang, key, title, desc, body):
    t = T[lang]; me = PAGES[key][lang]; root = "../" * me.count("/")
    other = "en" if lang == "fr" else "fr"
    n = t["nav"]
    def nl(k, label, anchor=""):
        cur = ' aria-current="page"' if k == key and not anchor else ''
        return f'<a class="l" href="{rel(me, PAGES[k][lang], anchor)}"{cur}>{e(label)}</a>'
    fr_href = rel(me, PAGES[key]["fr"]); en_href = rel(me, PAGES[key]["en"])
    footer_links = " · ".join(f'<a href="{rel(me, PAGES[k][lang])}">{e(n[k])}</a>' for k in ("packages", "work", "about"))
    return f'''<!doctype html>
<html lang="{t["htmllang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE_URL}/{me}">
<link rel="alternate" hreflang="fr" href="{SITE_URL}/{PAGES[key]["fr"]}">
<link rel="alternate" hreflang="en" href="{SITE_URL}/{PAGES[key]["en"]}">
<link rel="alternate" hreflang="x-default" href="{SITE_URL}/{PAGES[key]["fr"]}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{SITE_URL}/assets/og-image.png">
<meta property="og:url" content="{SITE_URL}/{me}">
<meta name="theme-color" content="#0F172A">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{root}assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="{root}assets/style.css">
</head>
<body>
<a class="skip" href="#main">{e(t["skip"])}</a>
<header>
<div class="wrap nav">
<a class="brand" href="{rel(me, PAGES["home"][lang])}" aria-label="BiZ Media">
<span class="biz" aria-hidden="true"><span>B</span><span class="i"><span class="dot"></span><span class="stem"></span></span><span>Z</span></span>
<span class="sep" aria-hidden="true"></span><span class="media" aria-hidden="true">MEDIA</span>
</a>
<nav aria-label="{e(t["navLabel"])}">
{nl("home", n["services"], "#services")}
{nl("packages", n["packages"])}
{nl("work", n["work"])}
{nl("about", n["about"])}
<div class="lang" role="group" aria-label="{e(t["langLabel"])}">
<a href="{fr_href}" lang="fr" hreflang="fr"{' aria-current="true"' if lang == "fr" else ''}>FR</a>
<a href="{en_href}" lang="en" hreflang="en"{' aria-current="true"' if lang == "en" else ''}>EN</a>
</div>
<a class="btn btn-gold" href="{rel(me, PAGES["home"][lang], "#contact")}">{e(n["quote"])}</a>
</nav>
</div>
</header>
<main id="main">
{body}
</main>
<footer><div class="wrap"><span class="t">BiZ Media · Stories That Connect. Solutions That Work.</span><span class="c fl">{footer_links}</span><span class="c">© <span id="y">2026</span> BiZ Media — bizmedia.ht</span></div></footer>
<script>
document.getElementById('y').textContent=new Date().getFullYear();
var q=document.getElementById('quote');
if(q)q.addEventListener('submit',function(ev){{
  ev.preventDefault();var f=ev.target,d=f.dataset,v=function(n){{return f.elements[n].value.trim()}};
  var lines=[d.intro,'',v('name')+(v('company')?' — '+v('company'):''),v('phone'),v('service'),'',v('project')].filter(function(x,i){{return x||i===1||i===5}});
  var msg=lines.join('\\n');
  if(d.wa){{window.open('https://wa.me/'+d.wa+'?text='+encodeURIComponent(msg),'_blank','noopener');}}
  else{{location.href='mailto:'+d.email+'?subject='+encodeURIComponent(d.subject)+'&body='+encodeURIComponent(msg);}}
}});
var sel=document.querySelector('#quote select');var m=location.hash.match(/^#contact-(\\d+)$/);
if(sel&&m){{if(sel.options[+m[1]])sel.selectedIndex=+m[1];document.getElementById('contact').scrollIntoView();}}
</script>
</body>
</html>
'''

def page_hero(eyebrow, h1, lead):
    return f'''<section class="hero page-hero"><div class="wrap"><div class="col">
<div class="eyebrow">{e(eyebrow)}</div><h1>{e(h1)}</h1><p class="lead">{e(lead)}</p>
</div></div></section>'''

def stats_html(t):
    return "\n".join(f'<div><b>{n}</b><span>{e(l)}</span></div>' for n, l in zip(NUMS, t["stats"]))

# ---------------- Pages ----------------
def home(lang):
    t = T[lang]; me = PAGES["home"][lang]
    services = "\n".join(f'''<article class="card">
<div class="ico">{svg(k)}</div>
<div><h3>{e(n)}</h3><p>{e(d)}</p></div>
<ul class="dots">{"".join(f"<li>{e(i)}</li>" for i in items)}</ul>
</article>''' for k, n, d, items in t["services"])
    steps = "\n".join(f'<li><span class="n">0{i+1}</span><h3>{e(a)}</h3><p>{e(b)}</p></li>' for i, (a, b) in enumerate(t["steps"]))
    options = "".join(f"<option>{e(o)}</option>" for o in t["options"])
    phone = e(CONTACT["phone_display"] or t["phoneFallback"])
    body = f'''<section class="hero" id="top">
<div class="wrap">
<div class="col">
<div class="eyebrow">Media · Technology · Business</div>
<h1 lang="en">Stories That Connect.<br><span>Solutions That Work.</span></h1>
<p class="lead">{e(t["heroText"])}</p>
<div class="actions"><a class="btn btn-gold" href="#contact">{e(t["heroCta1"])}</a><a class="btn btn-ghost" href="{rel(me, PAGES["packages"][lang])}">{e(t["heroCta2"])}</a></div>
</div>
<div class="col" style="gap:16px">
<div class="photo">{e(t["heroPhoto"])}</div>
<div class="dash">
<div class="dash-h"><span>{e(t["dashTitle"])}</span><span class="live">{e(t["dashLive"])}</span></div>
<div class="kpis"><div><b>374</b><span>{e(t["dashReg"])}</span></div><div><b>188</b><span>{e(t["dashPresent"])}</span></div><div><b>675</b><span>Messages</span></div></div>
</div>
</div>
</div>
</section>
<section class="services" id="services">
<div class="wrap">
<div class="head"><span class="eyebrow">{e(t["svcEyebrow"])}</span><h2>{e(t["svcTitle"])}</h2><p class="lead">{e(t["svcText"])}</p></div>
<div class="cards">
{services}
</div>
</div>
</section>
<section id="evenement">
<div class="wrap">
<div class="pack-h">
<div class="head"><span class="eyebrow">{e(t["packEyebrow"])}</span><h2>{e(t["packTitle"])}</h2><p class="lead">{e(t["packText"])}</p></div>
<a class="btn btn-navy" href="{rel(me, PAGES["packages"][lang])}">{e(t["packCta"])}</a>
</div>
<ol class="steps">
{steps}
</ol>
</div>
</section>
<section class="case" id="realisations">
<div class="wrap">
<div class="col"><span class="eyebrow">{e(t["caseEyebrow"])}</span><h2>Bwat Sekrèm Talks</h2><p class="lead">{e(t["caseText"])}</p><a class="more" href="{rel(me, PAGES["work"][lang])}">{e(t["caseCta"])}</a></div>
<div class="stats">
{stats_html(t)}
</div>
</div>
</section>
<section class="contact" id="contact">
<div class="wrap">
<div class="col" style="flex-basis:380px"><span class="eyebrow">Contact</span><h2>{e(t["contactTitle"])}</h2><p class="lead">{e(t["contactText"])}</p>
<div class="info"><span>{phone}</span><a href="mailto:{e(CONTACT["email"])}">{e(CONTACT["email"])}</a><span>{e(t["city"])}</span></div></div>
<form id="quote" data-email="{e(CONTACT["email"])}" data-wa="{e(CONTACT["whatsapp"])}" data-intro="{e(t["msgIntro"])}" data-subject="{e(t["msgSubject"])}">
<div class="row"><label>{e(t["fName"])}<input name="name" type="text" autocomplete="name" required></label><label>{e(t["fCompany"])}<input name="company" type="text" autocomplete="organization"></label></div>
<div class="row"><label>{e(t["fPhone"])}<input name="phone" type="tel" autocomplete="tel"></label><label>{e(t["fService"])}<select name="service">{options}</select></label></div>
<label>{e(t["fProject"])}<textarea name="project" rows="4"></textarea></label>
<button class="btn btn-navy" type="submit">{e(t["fSend"])}</button>
</form>
</div>
</section>'''
    return layout(lang, "home", t["homeTitle"], t["homeDesc"], body)

def packages(lang):
    t = T[lang]; me = PAGES["packages"][lang]; home_ = PAGES["home"][lang]
    cards = []
    for i, p in enumerate(t["packages"]):
        badge = f'<span class="badge">{e(t["pkPopular"])}</span>' if p["popular"] else ""
        items = "".join(f'<li>{svg("check", "#B45309", 18)}<span>{e(x)}</span></li>' for x in p["items"])
        # index de l'option correspondante dans le formulaire de contact
        opt = {0: 1, 1: 0, 2: 2, 3: 3}.get(i, 5)
        cards.append(f'''<article class="plan{' plan-pop' if p["popular"] else ''}">
{badge}<h2>{e(p["name"])}</h2><p class="pdesc">{e(p["desc"])}</p>
<div class="price"><span class="from">{e(t["pkFrom"])}</span><b>{e(p["price"])}</b><span class="per">{e(p["per"])}</span></div>
<ul class="checks">{items}</ul>
<a class="btn {'btn-gold' if p["popular"] else 'btn-navy'}" href="{rel(me, home_, f"#contact-{opt}")}">{e(t["pkCta"])}</a>
</article>''')
    faq = "\n".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in t["faq"])
    body = f'''{page_hero(t["pkEyebrow"], t["pkH1"], t["pkLead"])}
<section class="services"><div class="wrap">
<div class="plans">
{"".join(cards)}
</div>
<div class="custom"><div><h2>{e(t["customTitle"])}</h2><p class="lead">{e(t["customText"])}</p></div>
<a class="btn btn-gold" href="{rel(me, home_, "#contact-5")}">{e(t["customCta"])}</a></div>
</div></section>
<section><div class="wrap narrow">
<h2>{e(t["faqTitle"])}</h2>
<div class="faq">
{faq}
</div>
</div></section>'''
    return layout(lang, "packages", t["pkTitle"], t["pkDesc"], body)

def work(lang):
    t = T[lang]; me = PAGES["work"][lang]; home_ = PAGES["home"][lang]
    sol = "".join(f'<li>{svg("check", "#B45309", 18)}<span>{e(x)}</span></li>' for x in t["csSolution"])
    gallery = "".join(f'<div class="ph">{e(t["galleryPh"])}</div>' for _ in range(6))
    body = f'''{page_hero(t["wkEyebrow"], t["wkH1"], t["wkLead"])}
<section class="services"><div class="wrap">
<div class="cs">
<div class="cs-main">
<span class="eyebrow">{e(t["csEyebrow"])}</span><h2>Bwat Sekrèm Talks</h2>
<dl class="meta"><div><dt>{e(t["csClient"])}</dt><dd>{e(t["csClientV"])}</dd></div><div><dt>{e(t["csType"])}</dt><dd>{e(t["csTypeV"])}</dd></div><div><dt>{e(t["csServices"])}</dt><dd>{e(t["csServicesV"])}</dd></div></dl>
<h3>{e(t["csChallengeT"])}</h3><p class="lead">{e(t["csChallenge"])}</p>
<h3>{e(t["csSolutionT"])}</h3><ul class="checks">{sol}</ul>
</div>
<div class="cs-side">
<h3>{e(t["csResultsT"])}</h3>
<div class="stats stats-light">
{stats_html(t)}
</div>
</div>
</div>
</div></section>
<section><div class="wrap">
<h2>{e(t["galleryTitle"])}</h2>
<div class="gallery">{gallery}</div>
</div></section>
<section class="case cta-band"><div class="wrap"><h2>{e(t["moreTitle"])}</h2><a class="btn btn-gold" href="{rel(me, home_, "#contact")}">{e(t["moreCta"])}</a></div></section>'''
    return layout(lang, "work", t["wkTitle"], t["wkDesc"], body)

def about(lang):
    t = T[lang]; me = PAGES["about"][lang]; home_ = PAGES["home"][lang]
    story = "".join(f'<p class="lead">{e(p)}</p>' for p in t["story"])
    values = "".join(f'<div class="val"><h3>{e(a)}</h3><p>{e(b)}</p></div>' for a, b in t["values"])
    how = "\n".join(f'<li><span class="n">0{i+1}</span><h3>{e(a)}</h3><p>{e(b)}</p></li>' for i, (a, b) in enumerate(t["how"]))
    team = "".join(f'<div class="member"><div class="avatar" aria-hidden="true"></div><b>{e(t["teamPh"])}</b><span>{e(t["teamRole"])}</span></div>' for _ in range(3))
    body = f'''{page_hero(t["abEyebrow"], t["abH1"], t["abLead"])}
<section><div class="wrap narrow">
<h2>{e(t["storyTitle"])}</h2>
<div class="story">{story}</div>
</div></section>
<section class="services"><div class="wrap">
<div class="head"><h2>{e(t["valuesTitle"])}</h2></div>
<div class="values">{values}</div>
</div></section>
<section><div class="wrap">
<div class="head"><h2>{e(t["howTitle"])}</h2></div>
<ol class="steps steps-4">
{how}
</ol>
</div></section>
<section class="services"><div class="wrap">
<div class="head"><h2>{e(t["teamTitle"])}</h2></div>
<div class="team">{team}</div>
</div></section>
<section class="case cta-band"><div class="wrap"><h2>{e(t["moreTitle"])}</h2><a class="btn btn-gold" href="{rel(me, home_, "#contact")}">{e(t["moreCta"])}</a></div></section>'''
    return layout(lang, "about", t["abTitle"], t["abDesc"], body)

BUILDERS = {"home": home, "packages": packages, "work": work, "about": about}

here = Path(__file__).parent
for key, paths in PAGES.items():
    for lang, p in paths.items():
        out = here / p / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(BUILDERS[key](lang), encoding="utf-8")
        print("OK:", out.relative_to(here))
