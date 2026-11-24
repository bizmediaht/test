# BiZ Media — site web

Site vitrine bilingue (FR / EN) de **BiZ Media** — *Stories That Connect. Solutions That Work.*

- `index.html` : version française (page par défaut)
- `en/index.html` : version anglaise
- `assets/` : styles, logo, favicon, image de partage

## Modifier les textes ou les coordonnées

Tous les textes et les coordonnées (e-mail, WhatsApp, téléphone) sont dans `build.py`.
Après modification :

```bash
python3 build.py
```

## Mise en ligne

Hébergé avec GitHub Pages (branche `main`, dossier racine).
Pour le domaine `bizmedia.ht` : ajouter un fichier `CNAME` contenant `bizmedia.ht`
et configurer le DNS chez le registrar.
