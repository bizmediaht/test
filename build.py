#!/usr/bin/env python3
"""Génère index.html (FR) et en/index.html (EN) à partir des textes ci-dessous.
Modifier les textes ou les coordonnées ici, puis lancer :  python3 build.py
"""
from html import escape
from pathlib import Path

SITE_URL = "https://bizmedia.ht"
CONTACT = {
    "email": "contact@bizmedia.ht",   # TODO : adresse réelle
    "whatsapp": "",                    # TODO : numéro au format 509XXXXXXXX (vide = formulaire par e-mail)
    "phone_display": "",               # TODO : ex. +509 XX XX XXXX
}

ICONS = {
    "media": '<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/>',
    "prod": '<polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2"/>',
    "digital": '<rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/><polyline points="7 10 10 12 14 8 17 10"/>',
    "corp": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
}
NUMS = ["374", "188", "675", "2 684"]

T = {
"fr": dict(
    htmllang="fr", path="/", title="BiZ Media — Photo, vidéo, production & solutions digitales en Haïti",
    desc="BiZ Media : photographie, vidéo, production, CRM et automatisation pour les entreprises et les événements en Haïti.",
    skip="Aller au contenu", navLabel="Navigation principale", navServices="Services", navPack="Pack Événement",
    navWork="Réalisations", navQuote="Demander un devis", langLabel="Langue",
    heroText="Photo, vidéo, production et systèmes digitaux — CRM, inscriptions, automatisation — réunis sous un même toit pour les entreprises et les événements en Haïti.",
    heroCta1="Parlons de votre projet", heroCta2="Voir le Pack Événement",
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
    packText="De la première inscription jusqu’au rapport final : on gère le système et on raconte l’histoire.", packCta="Réserver une date",
    steps=[
        ("Inscriptions en ligne", "Page et formulaire à vos couleurs, avec gestion des places."),
        ("Confirmations auto", "Messages de confirmation, relances et liste d’attente."),
        ("Pointage le jour J", "Accueil rapide et liste des présents en temps réel."),
        ("Couverture photo & vidéo", "Notre équipe capture les moments forts."),
        ("Certificats & rapport", "Certificats envoyés et bilan complet de l’événement."),
    ],
    caseEyebrow="Étude de cas",
    caseText="Formulaire d’inscription, confirmations et relances automatiques, liste d’attente, pointage à l’entrée, certificats et suivi CRM de chaque participant — un seul système, conçu et opéré par notre équipe.",
    caseCta="Obtenir le même système pour votre événement →",
    stats=["inscriptions", "présences pointées", "messages envoyés", "visites du site"],
    contactTitle="Racontons votre prochaine histoire.",
    contactText="Dites-nous ce que vous préparez. Nous revenons vers vous avec une proposition.",
    phoneFallback="[Téléphone / WhatsApp]", city="Haïti",
    fName="Nom complet", fCompany="Entreprise", fPhone="Téléphone", fService="Service souhaité", fProject="Votre projet", fSend="Envoyer la demande",
    options=["Pack Événement Complet", "BiZ Media — Photo / Vidéo", "BiZ Productions", "BiZ Digital — CRM / Automatisation", "BiZ Corporate"],
    msgIntro="Bonjour BiZ Media, je souhaite un devis.", msgSubject="Demande de devis — site web",
),
"en": dict(
    htmllang="en", path="/en/", title="BiZ Media — Photo, video, production & digital solutions in Haiti",
    desc="BiZ Media: photography, video, production, CRM and automation for businesses and events in Haiti.",
    skip="Skip to content", navLabel="Main navigation", navServices="Services", navPack="Event Package",
    navWork="Our Work", navQuote="Get a quote", langLabel="Language",
    heroText="Photo, video, production and digital systems — CRM, registrations, automation — all under one roof for businesses and events in Haiti.",
    heroCta1="Let’s talk about your project", heroCta2="See the Event Package",
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
    packText="From the first registration to the final report: we run the system and tell the story.", packCta="Book a date",
    steps=[
        ("Online registration", "A branded page and form, with seat management."),
        ("Automatic confirmations", "Confirmation messages, reminders and waitlist."),
        ("Event-day check-in", "Fast welcome desk and a live attendance list."),
        ("Photo & video coverage", "Our team captures the key moments."),
        ("Certificates & report", "Certificates sent and a full event report."),
    ],
    caseEyebrow="Case study",
    caseText="Registration form, automatic confirmations and reminders, waitlist, check-in at the door, certificates and CRM follow-up for every attendee — one system, built and run by our team.",
    caseCta="Get the same system for your event →",
    stats=["registrations", "check-ins recorded", "messages sent", "website visits"],
    contactTitle="Let’s tell your next story.",
    contactText="Tell us what you’re planning. We’ll get back to you with a proposal.",
    phoneFallback="[Phone / WhatsApp]", city="Haiti",
    fName="Full name", fCompany="Company", fPhone="Phone", fService="Service needed", fProject="Your project", fSend="Send request",
    options=["Complete Event Package", "BiZ Media — Photo / Video", "BiZ Productions", "BiZ Digital — CRM / Automation", "BiZ Corporate"],
    msgIntro="Hello BiZ Media, I would like a quote.", msgSubject="Quote request — website",
),
}

def e(s): return escape(s, quote=True)

def page(lang):
    t = T[lang]; root = "" if lang == "fr" else "../"
    other = "en" if lang == "fr" else "fr"
    services = "\n".join(f'''<article class="card">
<div class="ico"><svg aria-hidden="true" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#F5B841" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[k]}</svg></div>
<div><h3>{e(n)}</h3><p>{e(d)}</p></div>
<ul>{"".join(f"<li>{e(i)}</li>" for i in items)}</ul>
</article>''' for k, n, d, items in t["services"])
    steps = "\n".join(f'<li><span class="n">0{i+1}</span><h3>{e(a)}</h3><p>{e(b)}</p></li>' for i, (a, b) in enumerate(t["steps"]))
    stats = "\n".join(f'<div><b>{n}</b><span>{e(l)}</span></div>' for n, l in zip(NUMS, t["stats"]))
    options = "".join(f"<option>{e(o)}</option>" for o in t["options"])
    phone = e(CONTACT["phone_display"] or t["phoneFallback"])
    return f'''<!doctype html>
<html lang="{t["htmllang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t["title"])}</title>
<meta name="description" content="{e(t["desc"])}">
<link rel="canonical" href="{SITE_URL}{t["path"]}">
<link rel="alternate" hreflang="fr" href="{SITE_URL}/">
<link rel="alternate" hreflang="en" href="{SITE_URL}/en/">
<link rel="alternate" hreflang="x-default" href="{SITE_URL}/">
<meta property="og:title" content="{e(t["title"])}">
<meta property="og:description" content="{e(t["desc"])}">
<meta property="og:image" content="{SITE_URL}/assets/og-image.png">
<meta property="og:url" content="{SITE_URL}{t["path"]}">
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
<a class="brand" href="{root or './'}" aria-label="BiZ Media">
<span class="biz" aria-hidden="true"><span>B</span><span class="i"><span class="dot"></span><span class="stem"></span></span><span>Z</span></span>
<span class="sep" aria-hidden="true"></span><span class="media" aria-hidden="true">MEDIA</span>
</a>
<nav aria-label="{e(t["navLabel"])}">
<a class="l" href="#services">{e(t["navServices"])}</a>
<a class="l" href="#evenement">{e(t["navPack"])}</a>
<a class="l" href="#realisations">{e(t["navWork"])}</a>
<div class="lang" role="group" aria-label="{e(t["langLabel"])}">
<a href="{root or './'}" lang="fr" hreflang="fr"{' aria-current="page"' if lang == "fr" else ''}>FR</a>
<a href="{'en/' if lang == 'fr' else './'}" lang="en" hreflang="en"{' aria-current="page"' if lang == "en" else ''}>EN</a>
</div>
<a class="btn btn-gold" href="#contact">{e(t["navQuote"])}</a>
</nav>
</div>
</header>
<main id="main">
<section class="hero" id="top">
<div class="wrap">
<div class="col">
<div class="eyebrow">Media · Technology · Business</div>
<h1 lang="en">Stories That Connect.<br><span>Solutions That Work.</span></h1>
<p class="lead">{e(t["heroText"])}</p>
<div class="actions"><a class="btn btn-gold" href="#contact">{e(t["heroCta1"])}</a><a class="btn btn-ghost" href="#evenement">{e(t["heroCta2"])}</a></div>
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
<a class="btn btn-navy" href="#contact">{e(t["packCta"])}</a>
</div>
<ol class="steps">
{steps}
</ol>
</div>
</section>
<section class="case" id="realisations">
<div class="wrap">
<div class="col"><span class="eyebrow">{e(t["caseEyebrow"])}</span><h2>Bwat Sekrèm Talks</h2><p class="lead">{e(t["caseText"])}</p><a class="more" href="#contact">{e(t["caseCta"])}</a></div>
<div class="stats">
{stats}
</div>
</div>
</section>
<section class="contact" id="contact">
<div class="wrap">
<div class="col" style="flex-basis:380px"><span class="eyebrow">Contact</span><h2>{e(t["contactTitle"])}</h2><p class="lead">{e(t["contactText"])}</p>
<div class="info"><span>{phone}</span><a href="mailto:{e(CONTACT["email"])}" style="color:#334155">{e(CONTACT["email"])}</a><span>{e(t["city"])}</span></div></div>
<form id="quote" data-email="{e(CONTACT["email"])}" data-wa="{e(CONTACT["whatsapp"])}" data-intro="{e(t["msgIntro"])}" data-subject="{e(t["msgSubject"])}">
<div class="row"><label>{e(t["fName"])}<input name="name" type="text" autocomplete="name" required></label><label>{e(t["fCompany"])}<input name="company" type="text" autocomplete="organization"></label></div>
<div class="row"><label>{e(t["fPhone"])}<input name="phone" type="tel" autocomplete="tel"></label><label>{e(t["fService"])}<select name="service">{options}</select></label></div>
<label>{e(t["fProject"])}<textarea name="project" rows="4"></textarea></label>
<button class="btn btn-navy" type="submit">{e(t["fSend"])}</button>
</form>
</div>
</section>
</main>
<footer><div class="wrap"><span class="t">BiZ Media · Stories That Connect. Solutions That Work.</span><span class="c">© <span id="y">2026</span> BiZ Media — bizmedia.ht</span></div></footer>
<script>
document.getElementById('y').textContent=new Date().getFullYear();
document.getElementById('quote').addEventListener('submit',function(ev){{
  ev.preventDefault();var f=ev.target,d=f.dataset,v=function(n){{return f.elements[n].value.trim()}};
  var lines=[d.intro,'',v('name')+(v('company')?' — '+v('company'):''),v('phone'),v('service'),'',v('project')].filter(function(x,i){{return x||i===1||i===5}});
  var msg=lines.join('\\n');
  if(d.wa){{window.open('https://wa.me/'+d.wa+'?text='+encodeURIComponent(msg),'_blank','noopener');}}
  else{{location.href='mailto:'+d.email+'?subject='+encodeURIComponent(d.subject)+'&body='+encodeURIComponent(msg);}}
}});
</script>
</body>
</html>
'''

here = Path(__file__).parent
(here / "index.html").write_text(page("fr"), encoding="utf-8")
(here / "en").mkdir(exist_ok=True)
(here / "en" / "index.html").write_text(page("en"), encoding="utf-8")
print("OK: index.html, en/index.html")
