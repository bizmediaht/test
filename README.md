# BiZ Media — site web

Site vitrine bilingue (FR / EN) de **BiZ Media** — *Stories That Connect. Solutions That Work.*

| Page | Français | English |
|---|---|---|
| Accueil / Home | `index.html` | `en/index.html` |
| Forfaits / Packages | `forfaits/` | `en/packages/` |
| Réalisations / Our Work | `realisations/` | `en/work/` |
| À propos / About | `a-propos/` | `en/about/` |

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
