#!/usr/bin/env python3
"""Génère toutes les pages du site (FR + EN) à partir des textes ci-dessous.
Modifier les textes, les prix ou les coordonnées ici, puis lancer :  python3 build.py
"""
from html import escape
from pathlib import Path

SITE_URL = "https://bizmedia.ht"
CONTACT = {
    "email": "",                       # TODO : adresse e-mail (vide = non affichée)
    "whatsapp": "50949012257",         # numéro WhatsApp au format international, sans +
    "phone_display": "+509 4901-2257",
}

# Chemin de chaque page, par langue
PAGES = {
    "home":     {"fr": "",              "en": "en/"},
    "packages": {"fr": "forfaits/",     "en": "en/packages/"},
    "work":     {"fr": "realisations/", "en": "en/work/"},
    "about":    {"fr": "a-propos/",     "en": "en/about/"},
    "tickets":  {"fr": "billetterie/",  "en": "en/tickets/"},
    "order":    {"fr": "billetterie/commande/", "en": "en/tickets/order/"},
    "ticket":   {"fr": "billet/",       "en": "en/ticket/"},
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
    nav=dict(services="Services", packages="Forfaits", work="Réalisations", about="À propos", tickets="Billetterie", quote="Demander un devis"),
    footerLinks="Pages", illus="Photos et vidéo : images d’illustration.",
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
        dict(name="Pack Événement Essentiel", price=None, per="Devis gratuit", popular=False,
             desc="Le système digital, sans la couverture média.",
             items=["Page & formulaire d’inscription", "Confirmations et relances automatiques", "Liste d’attente et gestion des places", "Billetterie MonCash / NatCash avec QR code", "Pointage à l’entrée", "Rapport de participation"]),
        dict(name="Pack Événement Complet", price=None, per="Devis gratuit", popular=True,
             desc="Le système digital + la couverture photo & vidéo.",
             items=["Tout le Pack Essentiel", "Photographe & vidéaste le jour J", "Vidéo highlights pour réseaux sociaux", "Certificats de participation", "Suivi CRM après l’événement"]),
        dict(name="Couverture Média", price=None, per="Devis gratuit", popular=False,
             desc="Photo et vidéo professionnelles pour un événement.",
             items=["Photographe professionnel", "Captation vidéo", "Photos retouchées et livrées rapidement", "Vidéo récapitulative", "Livraison en ligne"]),
        dict(name="Contenu mensuel", price=None, per="Devis gratuit", popular=False,
             desc="Pour les entreprises qui communiquent chaque mois.",
             items=["Séances photo / vidéo chaque mois", "Contenus pour réseaux sociaux", "Interviews & portraits d’équipe", "Calendrier de publication", "Bilan mensuel"]),
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
    nav=dict(services="Services", packages="Packages", work="Our Work", about="About", tickets="Tickets", quote="Get a quote"),
    footerLinks="Pages", illus="Photos and video: illustrative images.",
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
        dict(name="Essential Event Package", price=None, per="Free quote", popular=False,
             desc="The digital system, without media coverage.",
             items=["Registration page & form", "Automatic confirmations and reminders", "Waitlist and seat management", "MonCash / NatCash ticketing with QR codes", "Check-in at the door", "Attendance report"]),
        dict(name="Complete Event Package", price=None, per="Free quote", popular=True,
             desc="The digital system + photo & video coverage.",
             items=["Everything in Essential", "Photographer & videographer on the day", "Highlight video for social media", "Attendance certificates", "Post-event CRM follow-up"]),
        dict(name="Media Coverage", price=None, per="Free quote", popular=False,
             desc="Professional photo and video for an event.",
             items=["Professional photographer", "Video capture", "Edited photos, delivered fast", "Recap video", "Online delivery"]),
        dict(name="Monthly Content", price=None, per="Free quote", popular=False,
             desc="For businesses that communicate every month.",
             items=["Monthly photo / video sessions", "Social media content", "Interviews & team portraits", "Publishing calendar", "Monthly report"]),
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

# Photos réelles — Bwat Sekrèm Talks
PHOTOS = {
    "fr": [("bst-certificats", "Remise des certificats aux intervenants, avec l’équipe Bwat Sekrèm sur scène"),
           ("bst-intervenants", "Les intervenants reçoivent un panier de produits locaux"),
           ("bst-scene", "Échanges chaleureux sur scène entre les intervenants et l’équipe"),
           ("bst-echange", "Le présentateur échange avec un intervenant au micro"),
           ("bst-remise", "Remise des cadeaux aux intervenants sur scène")],
    "en": [("bst-certificats", "Speakers receive their certificates, with the Bwat Sekrèm team on stage"),
           ("bst-intervenants", "Speakers receive a basket of local products"),
           ("bst-scene", "Warm moments on stage between speakers and the team"),
           ("bst-echange", "The host talks with a speaker at the microphone"),
           ("bst-remise", "Gifts handed to the speakers on stage")],
}

def root_of(path):
    return "../" * path.count("/")

def rel(frm, to, anchor=""):
    """Lien relatif de la page `frm` vers la page `to` (chemins de PAGES)."""
    up = "../" * frm.count("/")
    target = up + to
    return (target or "./") + anchor

def svg(name, color="#F5B841", size=26):
    return f'<svg aria-hidden="true" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>'

def layout(lang, key, title, desc, body, page=None, scripts=(), noindex=False):
    t = T[lang]; me = PAGES[key][lang]; root = "../" * me.count("/")
    other = "en" if lang == "fr" else "fr"
    n = t["nav"]
    def nl(k, label, anchor=""):
        cur = ' aria-current="page"' if k == key and not anchor else ''
        return f'<a class="l" href="{rel(me, PAGES[k][lang], anchor)}"{cur}>{e(label)}</a>'
    fr_href = rel(me, PAGES[key]["fr"]); en_href = rel(me, PAGES[key]["en"])
    footer_links = " · ".join(f'<a href="{rel(me, PAGES[k][lang])}">{e(n[k])}</a>' for k in ("packages", "work", "about", "tickets"))
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
<link rel="stylesheet" href="{root}assets/style.css">{'<meta name="robots" content="noindex">' if noindex else ""}
</head>
<body{f' data-page="{page}" data-root="{root}"' if page else ""}>
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
{nl("tickets", n["tickets"])}
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
{"".join(f'<script src="{src if src.startswith("http") else root + src}"></script>' for src in scripts)}
<footer><div class="wrap"><span class="t">BiZ Media · Stories That Connect. Solutions That Work.</span><span class="c fl">{footer_links}</span><span class="c">© <span id="y">2026</span> BiZ Media — bizmedia.ht</span></div></footer>
<script>
document.getElementById('y').textContent=new Date().getFullYear();
if(matchMedia('(prefers-reduced-motion: reduce)').matches)document.querySelectorAll('video[autoplay]').forEach(function(v){{v.pause();v.removeAttribute('autoplay')}});
(function(){{var it=document.querySelectorAll('.rot-i');if(it.length<2||matchMedia('(prefers-reduced-motion: reduce)').matches)return;var i=0;setInterval(function(){{it[i].classList.remove('on');i=(i+1)%it.length;it[i].classList.add('on');}},3200);}})();
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
# Textes de la page d'accueil (structure orientée client)
HOME = {
"fr": dict(
    eyebrow="Stories That Connect. Solutions That Work.",
    h1a="Votre événement :",
    rot=["une salle pleine, avec le bon public.", "des billets vendus par MonCash, sans stress.", "zéro désordre à l’entrée.",
         "chaque participant suivi, de l’inscription au certificat.", "des images dont vous serez fiers."],
    lead="Inscriptions en ligne, billetterie MonCash / NatCash, confirmations WhatsApp, pointage à l’entrée, couverture photo & vidéo et rapport final. Une seule équipe s’occupe de tout, avant, pendant et après.",
    ctaWa="Écrivez-nous sur WhatsApp", ctaForm="Demander un devis", ctaHow="Voir comment ça marche",
    reel="[ Showreel vidéo 30–60 s ]", reelLabel="Showreel BiZ Media",
    trust="Système déjà utilisé pour Bwat Sekrèm Talks",
    trustStats=[("374", "inscrits"), ("188", "présents pointés"), ("675", "messages envoyés")],
    howEyebrow="Comment ça marche", howTitle="Vous organisez. Nous gérons le reste.",
    howLead="Trois étapes, un seul interlocuteur. Voici ce que vivent vos participants, et ce que vous voyez de votre côté.",
    how=[
        dict(tag="Avant l’événement", title="Les inscriptions se gèrent toutes seules",
             text="Une page d’inscription à vos couleurs. Chaque inscrit reçoit sa confirmation sur WhatsApp. Quand c’est complet, la liste d’attente prend le relais.",
             points=["Formulaire en ligne", "Confirmation WhatsApp automatique", "Relances & liste d’attente"]),
        dict(tag="Le jour J", title="Un accueil rapide, une équipe qui filme",
             text="À l’entrée, on pointe chaque participant en quelques secondes. Pendant ce temps, nos photographes et vidéastes capturent les moments forts.",
             points=["Pointage à l’entrée", "Présences en temps réel", "Photo & vidéo professionnelles"]),
        dict(tag="Après", title="Des résultats concrets, des images à partager",
             text="Les participants reçoivent leur certificat. Vous recevez les photos, la vidéo highlights et un rapport complet de votre événement.",
             points=["Certificats envoyés", "Photos & vidéo livrées", "Rapport de participation"]),
    ],
    mForm=dict(title="Inscription — Forum Business 2026", name="Nom complet", phone="WhatsApp", btn="Je m’inscris"),
    mWa=dict(head="BiZ Événements", msg="Bonjour Nadia Votre inscription au Forum Business 2026 est confirmée. Rendez-vous samedi à 9 h. Présentez ce message à l’entrée.", time="09:41", reply="Merci !"),
    mDash=dict(title="Tableau de bord", live="En direct", reg="Inscrits", here="Présents", rate="Taux de présence", recent="Derniers arrivés"),
    proofEyebrow="La preuve", proofTitle="Bwat Sekrèm Talks : un système, des centaines de participants.",
    proofText="Inscriptions, confirmations, liste d’attente, pointage, certificats et suivi de chaque participant : tout a été conçu et opéré par notre équipe.",
    proofCta="Voir l’étude de cas →",
    quote="[ Témoignage du responsable de Bwat Sekrèm : une ou deux phrases sur le résultat obtenu. ]", quoteWho="[Nom]", quoteRole="[Fonction], Bwat Sekrèm",
    photosPh="[ Photo ]",
    pkEyebrow="Nos forfaits", pkTitle="Choisissez votre point de départ.", pkLead="Chaque forfait s’adapte à votre événement. Le premier appel est gratuit.",
    pkAll="Voir tous les forfaits et la FAQ →",
    svcEyebrow="Et aussi", svcTitle="Pour les entreprises, toute l’année.",
    svc=[("media", "Photo & vidéo", "Reportages, portraits et couverture d’événements."),
         ("prod", "Productions", "Interviews, mini-documentaires et spots publicitaires."),
         ("digital", "CRM & automatisation", "Suivi clients, relances WhatsApp et tableaux de bord."),
         ("corp", "Communication", "Image de marque, contenu institutionnel et interne.")],
    faqTitle="Vos questions",
    faq=[("Mes participants doivent-ils installer une application ?", "Non. Ils s’inscrivent depuis un simple lien et reçoivent leurs messages sur WhatsApp."),
         ("Puis-je prendre seulement le système, sans photo ni vidéo ?", "Oui, c’est le Pack Événement Essentiel. Vous pouvez aussi réserver uniquement la couverture média."),
         ("Combien de temps faut-il pour tout mettre en place ?", "[À compléter : délai de mise en place recommandé.]"),
         ("Comment se passe le paiement ?", "[À compléter : acompte, solde, modes de paiement.]")],
    finalTitle="Parlons de votre prochain événement.", finalText="Dites-nous la date, le lieu et le nombre de participants attendus. Nous revenons vers vous avec une proposition.",
    floatWa="WhatsApp", floatContact="Nous écrire",
),
"en": dict(
    eyebrow="Stories That Connect. Solutions That Work.",
    h1a="Your event:",
    rot=["a full room, with the right audience.", "tickets sold via MonCash, stress-free.", "zero chaos at the door.",
         "every attendee followed, from sign-up to certificate.", "images you’ll be proud of."],
    lead="Online registration, MonCash / NatCash ticketing, WhatsApp confirmations, check-in at the door, photo & video coverage and a final report. One team handles it all, before, during and after.",
    ctaWa="Message us on WhatsApp", ctaForm="Get a quote", ctaHow="See how it works",
    reel="[ Video showreel 30–60 s ]", reelLabel="BiZ Media showreel",
    trust="System already used for Bwat Sekrèm Talks",
    trustStats=[("374", "registered"), ("188", "checked in"), ("675", "messages sent")],
    howEyebrow="How it works", howTitle="You host. We handle the rest.",
    howLead="Three steps, one point of contact. Here is what your attendees experience, and what you see on your side.",
    how=[
        dict(tag="Before the event", title="Registrations run themselves",
             text="A branded registration page. Every attendee gets a WhatsApp confirmation. When seats run out, the waitlist takes over.",
             points=["Online form", "Automatic WhatsApp confirmation", "Reminders & waitlist"]),
        dict(tag="On the day", title="A fast welcome, a team that films",
             text="At the door, each attendee is checked in within seconds. Meanwhile, our photographers and videographers capture the key moments.",
             points=["Door check-in", "Live attendance", "Professional photo & video"]),
        dict(tag="After", title="Real results, images to share",
             text="Attendees receive their certificate. You receive the photos, the highlight video and a full report of your event.",
             points=["Certificates sent", "Photos & video delivered", "Attendance report"]),
    ],
    mForm=dict(title="Registration — Business Forum 2026", name="Full name", phone="WhatsApp", btn="Register"),
    mWa=dict(head="BiZ Events", msg="Hi Nadia Your registration for Business Forum 2026 is confirmed. See you Saturday at 9 am. Show this message at the door.", time="09:41", reply="Thanks!"),
    mDash=dict(title="Dashboard", live="Live", reg="Registered", here="Checked in", rate="Attendance rate", recent="Latest arrivals"),
    proofEyebrow="The proof", proofTitle="Bwat Sekrèm Talks: one system, hundreds of attendees.",
    proofText="Registrations, confirmations, waitlist, check-in, certificates and follow-up for every attendee: all designed and run by our team.",
    proofCta="Read the case study →",
    quote="[ Testimonial from the Bwat Sekrèm lead: one or two sentences about the result. ]", quoteWho="[Name]", quoteRole="[Role], Bwat Sekrèm",
    photosPh="[ Photo ]",
    pkEyebrow="Our packages", pkTitle="Pick your starting point.", pkLead="Every package adapts to your event. The first call is free.",
    pkAll="See all packages and FAQ →",
    svcEyebrow="Also", svcTitle="For businesses, all year round.",
    svc=[("media", "Photo & video", "Reports, portraits and event coverage."),
         ("prod", "Productions", "Interviews, mini-documentaries and commercials."),
         ("digital", "CRM & automation", "Customer follow-up, WhatsApp reminders and dashboards."),
         ("corp", "Communications", "Brand image, institutional and internal content.")],
    faqTitle="Your questions",
    faq=[("Do attendees need to install an app?", "No. They register from a simple link and receive their messages on WhatsApp."),
         ("Can I get only the system, without photo or video?", "Yes, that’s the Essential Event Package. You can also book media coverage only."),
         ("How long does setup take?", "[To complete: recommended setup lead time.]"),
         ("How does payment work?", "[To complete: deposit, balance, payment methods.]")],
    finalTitle="Let’s talk about your next event.", finalText="Tell us the date, the venue and how many attendees you expect. We’ll get back to you with a proposal.",
    floatWa="WhatsApp", floatContact="Contact us",
),
}

WA_ICON = '<svg aria-hidden="true" width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.3-.4.8-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/></svg>'

def price_html(t, p):
    if p["price"]:
        return f'<span class="from">{e(t["pkFrom"])}</span><b>{e(p["price"])}</b><span class="per">{e(p["per"])}</span>'
    return f'<b>{e(t["pkQuote"])}</b><span class="per">{e(p["per"])}</span>'

def wa_link(lang):
    if not CONTACT["whatsapp"]:
        return None
    from urllib.parse import quote
    return f'https://wa.me/{CONTACT["whatsapp"]}?text={quote(T[lang]["msgIntro"])}'

def quote_html(h):
    q = h.get("quote") or ""
    if not q or q.startswith("["):
        return ""
    return f'<figure class="quote"><blockquote>{e(q)}</blockquote><figcaption><b>{e(h["quoteWho"])}</b> · {e(h["quoteRole"])}</figcaption></figure>'

def home(lang):
    t = T[lang]; h = HOME[lang]; me = PAGES["home"][lang]
    wa = wa_link(lang)
    cta_main = (f'<a class="btn btn-gold" href="{e(wa)}" target="_blank" rel="noopener">{WA_ICON}<span>{e(h["ctaWa"])}</span></a>' if wa
                else f'<a class="btn btn-gold" href="#contact">{e(h["ctaForm"])}</a>')
    trust = "".join(f'<li><b>{n}</b> {e(l)}</li>' for n, l in h["trustStats"])
    f, w, d = h["mForm"], h["mWa"], h["mDash"]
    mocks = [
        f'''<div class="mock mock-form" aria-hidden="true">
<div class="mf-top"><span class="biz sm"><span>B</span><span class="i"><span class="dot"></span><span class="stem"></span></span><span>Z</span></span></div>
<b class="mf-title">{e(f["title"])}</b>
<span class="mf-l">{e(f["name"])}</span><span class="mf-in">Nadia J.</span>
<span class="mf-l">{e(f["phone"])}</span><span class="mf-in">+509 •••• ••••</span>
<span class="mf-btn">{e(f["btn"])}</span>
</div>''',
        f'''<div class="mock mock-wa" aria-hidden="true">
<div class="wa-head"><span class="wa-av">B</span><b>{e(w["head"])}</b></div>
<div class="wa-body"><p class="bub in">{e(w["msg"])}<span class="tm">{w["time"]}</span></p><p class="bub out">{e(w["reply"])}<span class="tm">{w["time"]} ✓✓</span></p></div>
</div>''',
        f'''<div class="mock mock-dash" aria-hidden="true">
<div class="md-h"><b>{e(d["title"])}</b><span class="live">{e(d["live"])}</span></div>
<div class="md-k"><div><b>374</b><span>{e(d["reg"])}</span></div><div><b>188</b><span>{e(d["here"])}</span></div></div>
<div class="md-bar"><span>{e(d["rate"])}</span><div><i style="width:50%"></i></div></div>
<span class="md-r">{e(d["recent"])}</span>
<ul class="md-list"><li><i></i>Participant #188</li><li><i></i>Participant #187</li><li><i></i>Participant #186</li></ul>
</div>''',
    ]
    how = "\n".join(f'''<li class="how-step">
<div class="how-txt"><span class="how-tag">0{i+1} · {e(s["tag"])}</span><h3>{e(s["title"])}</h3><p>{e(s["text"])}</p>
<ul class="checks">{"".join(f'<li>{svg("check", "#B45309", 18)}<span>{e(p)}</span></li>' for p in s["points"])}</ul></div>
<div class="how-vis">{mocks[i]}</div>
</li>''' for i, s in enumerate(h["how"]))
    photos = "".join(f'<img src="{root_of(me)}assets/img/{n}-sm.jpg" srcset="{root_of(me)}assets/img/{n}-sm.jpg 700w, {root_of(me)}assets/img/{n}.jpg 1600w" sizes="(max-width:720px) 100vw, 33vw" alt="{e(alt)}" loading="lazy" width="700" height="467">' for n, alt in PHOTOS[lang][:3])
    plans = []
    for i, p in enumerate(t["packages"][:3]):
        opt = {0: 1, 1: 0, 2: 2}[i]
        badge = f'<span class="badge">{e(t["pkPopular"])}</span>' if p["popular"] else ""
        items = "".join(f'<li>{svg("check", "#B45309", 18)}<span>{e(x)}</span></li>' for x in p["items"][:4])
        plans.append(f'''<article class="plan{' plan-pop' if p["popular"] else ''}">
{badge}<h3 class="plan-h">{e(p["name"])}</h3><p class="pdesc">{e(p["desc"])}</p>
<div class="price">{price_html(t, p)}</div>
<ul class="checks">{items}</ul>
<a class="btn {'btn-gold' if p["popular"] else 'btn-navy'}" href="#contact-{opt}">{e(t["pkCta"])}</a>
</article>''')
    svc = "".join(f'<div class="mini"><div class="ico sm">{svg(k, size=22)}</div><div><h3>{e(a)}</h3><p>{e(b)}</p></div></div>' for k, a, b in h["svc"])
    faq = "\n".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in h["faq"] if not a.startswith("["))
    options = "".join(f"<option>{e(o)}</option>" for o in t["options"])
    phone = e(CONTACT["phone_display"] or t["phoneFallback"])
    email_html = f'<a href="mailto:{e(CONTACT["email"])}">{e(CONTACT["email"])}</a>' if CONTACT["email"] else ""
    float_btn = (f'<a class="float-wa" href="{e(wa)}" target="_blank" rel="noopener" aria-label="{e(h["ctaWa"])}">{WA_ICON}<span>{e(h["floatWa"])}</span></a>' if wa
                 else f'<a class="float-wa" href="#contact">{WA_ICON}<span>{e(h["floatContact"])}</span></a>')
    body = f'''<section class="hero" id="top">
<div class="wrap">
<div class="col">
<div class="eyebrow" lang="en">{e(h["eyebrow"])}</div>
<h1>{e(h["h1a"])} <span class="sr-only">{e(" ".join(h["rot"]))}</span><span class="rot" aria-hidden="true">{"".join(f'<span class="rot-i{" on" if i == 0 else ""}">{e(x)}</span>' for i, x in enumerate(h["rot"]))}</span></h1>
<p class="lead">{e(h["lead"])}</p>
<div class="actions">{cta_main}<a class="btn btn-ghost" href="#comment">{e(h["ctaHow"])}</a></div>
</div>
<div class="col reel-col">
<div class="reel"><video autoplay muted loop playsinline preload="metadata" poster="{root_of(me)}assets/img/bst-certificats.jpg" aria-label="{e(h["reelLabel"])}"><source src="{root_of(me)}assets/showreel.mp4" type="video/mp4"></video></div>
</div>
</div>
<div class="wrap trust"><span>{e(h["trust"])}</span><ul>{trust}</ul></div>
</section>
<section id="comment">
<div class="wrap">
<div class="head center"><span class="eyebrow">{e(h["howEyebrow"])}</span><h2>{e(h["howTitle"])}</h2><p class="lead">{e(h["howLead"])}</p></div>
<ol class="how">
{how}
</ol>
</div>
</section>
<section class="case" id="preuve">
<div class="wrap proof">
<div class="col"><span class="eyebrow">{e(h["proofEyebrow"])}</span><h2>{e(h["proofTitle"])}</h2><p class="lead">{e(h["proofText"])}</p>
{quote_html(h)}
<a class="more" href="{rel(me, PAGES["work"][lang])}">{e(h["proofCta"])}</a></div>
<div class="stats">
{stats_html(t)}
</div>
</div>
<div class="wrap photos">{photos}</div>
</section>
<section class="services" id="forfaits">
<div class="wrap">
<div class="head center"><span class="eyebrow">{e(h["pkEyebrow"])}</span><h2>{e(h["pkTitle"])}</h2><p class="lead">{e(h["pkLead"])}</p></div>
<div class="plans plans-3">
{"".join(plans)}
</div>
<p class="center-link"><a class="dark-link" href="{rel(me, PAGES["packages"][lang])}">{e(h["pkAll"])}</a></p>
</div>
</section>
<section id="services">
<div class="wrap">
<div class="head"><span class="eyebrow">{e(h["svcEyebrow"])}</span><h2>{e(h["svcTitle"])}</h2></div>
<div class="minis">{svc}</div>
</div>
</section>
<section class="services">
<div class="wrap narrow">
<h2>{e(h["faqTitle"])}</h2>
<div class="faq">
{faq}
</div>
</div>
</section>
<section class="contact" id="contact">
<div class="wrap">
<div class="col" style="flex-basis:380px"><span class="eyebrow">Contact</span><h2>{e(h["finalTitle"])}</h2><p class="lead">{e(h["finalText"])}</p>
{cta_main if wa else ""}
<div class="info"><a href="tel:+{e(CONTACT["whatsapp"])}">{phone}</a>{email_html}<span>{e(t["city"])}</span></div></div>
<form id="quote" data-email="{e(CONTACT["email"])}" data-wa="{e(CONTACT["whatsapp"])}" data-intro="{e(t["msgIntro"])}" data-subject="{e(t["msgSubject"])}">
<div class="row"><label>{e(t["fName"])}<input name="name" type="text" autocomplete="name" required></label><label>{e(t["fCompany"])}<input name="company" type="text" autocomplete="organization"></label></div>
<div class="row"><label>{e(t["fPhone"])}<input name="phone" type="tel" autocomplete="tel"></label><label>{e(t["fService"])}<select name="service">{options}</select></label></div>
<label>{e(t["fProject"])}<textarea name="project" rows="4"></textarea></label>
<button class="btn btn-navy" type="submit">{e(t["fSend"])}</button>
</form>
</div>
</section>
{float_btn}'''
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
<div class="price">{price_html(t, p)}</div>
<ul class="checks">{items}</ul>
<a class="btn {'btn-gold' if p["popular"] else 'btn-navy'}" href="{rel(me, home_, f"#contact-{opt}")}">{e(t["pkCta"])}</a>
</article>''')
    faq = "\n".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in t["faq"] if not a.startswith("["))
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
    gallery = "".join(f'<img src="{root_of(me)}assets/img/{n}-sm.jpg" srcset="{root_of(me)}assets/img/{n}-sm.jpg 700w, {root_of(me)}assets/img/{n}.jpg 1600w" sizes="(max-width:720px) 100vw, 33vw" alt="{e(alt)}" loading="lazy" width="700" height="467">' for n, alt in PHOTOS[lang])
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
<section class="case cta-band"><div class="wrap"><h2>{e(t["moreTitle"])}</h2><a class="btn btn-gold" href="{rel(me, home_, "#contact")}">{e(t["moreCta"])}</a></div></section>'''
    return layout(lang, "about", t["abTitle"], t["abDesc"], body)


SB_JS = "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.45.4/dist/umd/supabase.min.js"
QR_JS = "https://cdn.jsdelivr.net/npm/qrcode-generator@1.4.4/qrcode.min.js"
SCAN_JS = "https://cdn.jsdelivr.net/npm/html5-qrcode@2.3.8/html5-qrcode.min.js"

TK = {
    "fr": dict(shopT="Billetterie — BiZ Media", shopD="Achetez vos billets d’événements avec MonCash ou NatCash. Billet avec QR code envoyé sur WhatsApp.",
               shopEy="Billetterie", shopH1="Vos billets, payés par MonCash ou NatCash.",
               shopLead="Choisissez votre billet, envoyez le paiement, recevez votre QR code sur WhatsApp.",
               orderT="Ma commande — BiZ Media", ticketT="Mon billet — BiZ Media", noscript="Activez JavaScript pour utiliser la billetterie."),
    "en": dict(shopT="Tickets — BiZ Media", shopD="Buy event tickets with MonCash or NatCash. QR-code ticket sent on WhatsApp.",
               shopEy="Tickets", shopH1="Your tickets, paid with MonCash or NatCash.",
               shopLead="Pick your ticket, send the payment, get your QR code on WhatsApp.",
               orderT="My order — BiZ Media", ticketT="My ticket — BiZ Media", noscript="Enable JavaScript to use ticketing."),
}

def app_shell(lang, key, title, desc, page, hero=None, scripts=(SB_JS, QR_JS, "assets/billetterie.js"), noindex=False):
    k = TK[lang]
    top = page_hero(*hero) if hero else ""
    body = f'''{top}
<section class="services app-sec"><div class="wrap"><div id="app"><noscript><p class="note">{e(k["noscript"])}</p></noscript></div></div></section>'''
    return layout(lang, key, title, desc, body, page=page, scripts=scripts, noindex=noindex)

def tickets(lang):
    k = TK[lang]
    return app_shell(lang, "tickets", k["shopT"], k["shopD"], "shop", hero=(k["shopEy"], k["shopH1"], k["shopLead"]))

def order(lang):
    k = TK[lang]
    return app_shell(lang, "order", k["orderT"], k["shopD"], "order", noindex=True)

def ticket(lang):
    k = TK[lang]
    return app_shell(lang, "ticket", k["ticketT"], k["shopD"], "ticket", noindex=True)

def admin_page(depth, page, title):
    root = "../" * depth
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{e(title)} — BiZ Media</title>
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="{root}assets/style.css">
</head>
<body data-page="{page}" data-root="{root}" class="adm">
<header><div class="wrap nav">
<a class="brand" href="{root}admin/" aria-label="BiZ Media — administration">
<span class="biz" aria-hidden="true"><span>B</span><span class="i"><span class="dot"></span><span class="stem"></span></span><span>Z</span></span>
<span class="sep" aria-hidden="true"></span><span class="media" aria-hidden="true">BILLETTERIE</span></a>
<span id="who" class="who"></span>
</div></header>
<main id="main"><section class="services app-sec"><div class="wrap"><div id="app"><p class="note">Chargement…</p></div></div></section></main>
<script src="{SB_JS}"></script>
{f'<script src="{SCAN_JS}"></script>' if page == "scan" else ""}
<script src="{root}assets/admin.js"></script>
</body>
</html>
'''

BUILDERS = {"home": home, "packages": packages, "work": work, "about": about, "tickets": tickets, "order": order, "ticket": ticket}

here = Path(__file__).parent
for key, paths in PAGES.items():
    for lang, p in paths.items():
        out = here / p / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(BUILDERS[key](lang), encoding="utf-8")
        print("OK:", out.relative_to(here))
for depth, path, page, title in ((1, "admin/", "admin", "Administration"), (2, "admin/scan/", "scan", "Scanner")):
    out = here / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(admin_page(depth, page, title), encoding="utf-8")
    print("OK:", out.relative_to(here))
