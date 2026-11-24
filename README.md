# BiZ Media — site web

Site vitrine bilingue (FR / EN) de **BiZ Media** — *Stories That Connect. Solutions That Work.*

| Page | Français | English |
|---|---|---|
| Accueil / Home | `index.html` | `en/index.html` |
| Forfaits / Packages | `forfaits/` | `en/packages/` |
| Réalisations / Our Work | `realisations/` | `en/work/` |
| À propos / About | `a-propos/` | `en/about/` |
| Billetterie / Tickets | `billetterie/` | `en/tickets/` |

- `assets/` : styles, logo, favicon, image de partage

## Modifier les textes ou les coordonnées

Tous les textes, les prix et les coordonnées (e-mail, WhatsApp, téléphone) sont dans `build.py`.
Les éléments à compléter sont marqués `[Prix]`, `[X]`, `[Nom]`, `[À compléter …]`.
Après modification :

```bash
python3 build.py
```

## Mise en ligne

Hébergé avec GitHub Pages (branche `main`, dossier racine).
Pour le domaine `bizmedia.ht` : ajouter un fichier `CNAME` contenant `bizmedia.ht`
et configurer le DNS chez le registrar.

## Billetterie

Paiement MonCash / NatCash envoyé par le client, vérifié à la main, puis billet avec QR code.

- Base de données : projet Supabase **BiZ Media** (`sljzkbcpkecpvvpzskxa`)
- `billetterie/?e=<slug>` : achat d'un billet · `billetterie/commande/?t=<jeton>` : suivi de commande · `billet/?c=<code>` : billet
- `admin/` : validation des paiements et envoi des billets sur WhatsApp · `admin/scan/` : scanner à l'entrée
- Les événements et types de billets se créent dans Supabase (tables `events`, `ticket_types`).
- Un administrateur = un compte Supabase Auth dont l'e-mail est dans la table `admins`.

## Plusieurs clients et base nationale

- `organizations` : un client (ex. Cap Talent Lab). Chaque événement appartient à un client (`events.org_id`).
- `org_members` : e-mails qui ont accès à l'espace d'un client (`owner` ou `staff`). Ils ne voient que les événements, commandes et billets de leur client.
- `admins` : équipe BiZ Media (super-admin) — voit tous les clients et la base nationale (`admin/participants/`).
- `people` : une fiche par numéro de téléphone (format +509…), partagée entre tous les clients.
  `consent_biz` = la personne a coché « BiZ Media peut me contacter ». Seules ces personnes peuvent être contactées par BiZ.
- Le formulaire impose le consentement pour l'événement ; le consentement BiZ est facultatif et décoché par défaut.
  La page de commande permet de retirer ce consentement.
