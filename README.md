#  GOOD-DEAL-CHAT

> Une interface conversationnelle ancrée dans la connaissance, conçue pour les alumni de la formation GOOD-DEAL.  
> Posez une question sur Excel, la gestion de stocks, les calculs financiers ou l’ingénierie de prompt, et obtenez instantanément une réponse experte, appuyée par une base de savoir structurée.

![Stars](https://img.shields.io/badge/theme-cosmic-6ee7ff) ![Python](https://img.shields.io/badge/python-3.8+-blue) ![Flask](https://img.shields.io/badge/flask-2.x-lightgrey) ![Mistral AI](https://img.shields.io/badge/AI-Mistral-ffd580) ![License](https://img.shields.io/badge/license-MIT-green)

---

##  Table des matières

- [Aperçu](#aperçu)
- [Architecture](#architecture)
- [Fonctionnement](#fonctionnement)
- [Technologies utilisées](#technologies-utilisées)
- [Structure du projet](#structure-du-projet)
- [Prise en main rapide](#prise-en-main-rapide)
  - [Prérequis](#prérequis)
  - [Installation locale](#installation-locale)
  - [Lancement en local](#lancement-en-local)
- [Déploiement](#déploiement)
  - [Render (recommandé)](#render-recommandé)
  - [Heroku (alternative)](#heroku-alternative)
- [Gestion de la base de connaissances](#gestion-de-la-base-de-connaissances)
- [Configuration](#configuration)
- [Sécurité](#sécurité)
- [Développement](#développement)
- [Licence](#licence)
- [Support](#support)

---

## Aperçu

**GOOD-DEAL-CHAT** met à disposition des apprenants un assistant intelligent capable de répondre à leurs questions métier en s’appuyant exclusivement sur une base de connaissances dédiée. L’outil combine un backend Flask faisant office de proxy vers l’API Mistral AI, une interface web immersive (thème cosmique), et un module de transformation CSV → prompt système qui garantit des réponses précises et contextualisées.

Cas d’usage typiques :
- “Comment construire un diagramme de Pareto sous Excel ?”
- “Explique-moi la différence entre le Few‑Shot et le Chained Prompting.”
- “Quelle formule utiliser pour alerter en cas de rupture de stock ?”

---

## Architecture

```
┌─────────────┐      HTTP POST /chat      ┌──────────────┐      API Mistral      ┌───────────────┐
│  Navigateur  │ ──────────────────────────│  Flask Proxy │ ─────────────────────│  Mistral AI    │
│ (HTML/CSS/JS)│ ◀─────────────────────────│  (server.py) │ ◀────────────────────│  (chat compl.) │
└─────────────┘      JSON {message}        └──────────────┘      messages +       └───────────────┘
                                                              contexte système
                                                              (knowledge.txt)
```

Le flux d’une requête :
1. L’utilisateur saisit une question dans l’interface web.
2. Le frontend envoie l’historique de la session au backend (`/chat`).
3. Le serveur insère le contenu de `knowledge.txt` en tant que message `system` et appelle l’API Mistral.
4. La réponse de l’IA est renvoyée au frontend, où le Markdown est interprété avant affichage.

---

## Fonctionnement

### Backend (`server.py`)
- Charge la base de connaissances (`knowledge.txt`) au démarrage.
- Expose un point de terminaison `/chat` qui reçoit `{ "messages": [...] }`.
- Construit le tableau complet des messages en ajoutant le contexte système en première position.
- Appelle l’API Mistral avec :
  - Modèle : `mistral-small` (modifiable)
  - Température : `0.3` (réponses précises)
  - `max_tokens` : `1024`
- Retourne la réponse de l’assistant sous la forme `{ "message": { "role": "assistant", "content": "..." } }`.

### Frontend (`static/`)
- **HTML** : structure sémantique et accessible (attributs ARIA).
- **CSS** : thème cosmique avec toile étoilée animée (canvas), bulles de conversation translucides et animations fluides.
- **JavaScript** :
  - Maintient un historique de messages en mémoire (aucune persistance).
  - Envoie les requêtes au backend via `fetch`.
  - Interprète le Markdown des réponses avec [marked.js](https://marked.js.org) pour un affichage structuré (titres, listes, code, etc.).

### Base de connaissances
- **`knowledge_base.csv`** : base structurée avec les colonnes `Catégorie`, `Sous_Catégorie`, `Question_Apprenant`, `Réponse_Détaillée_Chatbot`, `Exemple_Pratique_Ou_Formule`.
- **`convert_csv_to_txt.py`** : script Python qui lit le CSV et produit un bloc texte formaté injecté comme prompt système.
- **`knowledge.txt`** : fichier texte chargé par le serveur. Il contient l’intégralité du savoir métier dans un format lisible par le modèle.

---

## Technologies utilisées

| Couche        | Technologies |
|---------------|--------------|
| **Frontend**  | HTML5, CSS3, JavaScript (vanilla), Canvas API, [marked.js](https://marked.js.org) |
| **Backend**   | Python 3, Flask, Gunicorn (production), requests, python-dotenv |
| **IA**        | API Mistral AI (`mistral-small` ou `mistral-medium`) |
| **Déploiement** | Render, Heroku, tout service supportant un Procfile/Gunicorn |

---

## Structure du projet

```
GOOD-DEAL-CHAT/
├── server.py                    Application Flask – endpoint /chat
├── static/
│   ├── index.html               Interface utilisateur avec toile étoilée
│   ├── app.js                   Logique de messagerie et rendu Markdown
│   └── style.css                Thème cosmique
├── convert_csv_to_txt.py        Conversion CSV → prompt système
├── knowledge_base.csv           Questions/réponses métier (séparateur « ; »)
├── knowledge.txt                Contexte système (généré)
├── requirements.txt             Dépendances Python
├── Procfile                     Commande de démarrage pour Gunicorn
└── README.md                    Documentation
```

---

## Prise en main rapide

### Prérequis
- Python 3.8 ou supérieur
- Une clé API Mistral AI ([console.mistral.ai](https://console.mistral.ai))

### Installation locale
```bash
git clone https://github.com/monsieurMechant200/GOOD-DEAL-CHAT.git
cd GOOD-DEAL-CHAT
python -m venv venv
source venv/bin/activate      # Windows : venv\Scripts\activate
pip install -r requirements.txt
```

Créez un fichier `.env` à la racine :
```
MISTRAL_API_KEY=votre_clé_api
```

### Lancement en local
```bash
python server.py
```
Ouvrez [http://localhost:5000](http://localhost:5000) dans votre navigateur.

---

## Déploiement

### Render (recommandé)
1. Poussez votre projet sur GitHub.
2. Sur [Render](https://render.com), créez un **Web Service** connecté à votre dépôt.
3. Paramétrez :
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `gunicorn server:app --bind 0.0.0.0:$PORT`
4. Ajoutez la variable d’environnement `MISTRAL_API_KEY` avec votre clé.
5. Déployez. Votre service sera accessible sur `https://<nom>.onrender.com`.

> 💡 Le plan gratuit de Render met le service en veille après 15 min d’inactivité ; la première requête peut prendre 30–60 s.

### Heroku (alternative)
```bash
heroku create votre-app
heroku config:set MISTRAL_API_KEY=votre_clé
git push heroku main
```

---

## Gestion de la base de connaissances

1. **Modifiez** `knowledge_base.csv` avec vos nouvelles entrées (séparateur `;`).  
2. **Régénérez** le contexte système :
   ```bash
   python convert_csv_to_txt.py
   ```
3. **Redémarrez** le serveur (ou redéployez) pour que le nouveau `knowledge.txt` soit pris en compte.

Il est conseillé de versionner `knowledge_base.csv` **et** `knowledge.txt` afin de conserver un historique des connaissances déployées.

---

## Configuration

Tous les paramètres centraux sont dans `server.py` :

| Paramètre | Valeur par défaut | Description |
|-----------|-------------------|-------------|
| `MODEL` | `"mistral-small"` | Modèle IA (peut être remplacé par `mistral-medium`) |
| `temperature` | `0.3` | Contrôle la créativité (plus bas = plus déterministe) |
| `max_tokens` | `1024` | Longueur maximale de la réponse |
| `MISTRAL_URL` | `"https://api.mistral.ai/v1/chat/completions"` | Endpoint de l’API |

---

## Sécurité

- **Clé API** : stockée exclusivement dans des variables d’environnement, jamais dans le code source ni dans le dépôt.
- **Contenu utilisateur** : les messages sont échappés côté frontend avant affichage (pas de HTML brut).
- **Réponses de l’IA** : le Markdown est converti en HTML par `marked.js`, qui nettoie les scripts par défaut.
- **Timeout** : un délai de 30 secondes empêche les connexions pendantes vers l’API Mistral.
- **CORS** : le frontend appelle le même domaine (pas de requête cross-origin exposée).

---

## Développement

### Tests manuels
```bash
# Lancez le serveur en local, puis exécutez :
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Comment utiliser SOMME.SI ?"}]}'
```

### Personnalisation
- **Styles** : modifiez `static/style.css` (palette cosmique, animations).
- **Logique frontend** : éditez `static/app.js`.
- **Comportement backend** : ajoutez des middlewares, de nouvelles routes, ou modifiez les paramètres d’appel dans `server.py`.
- **Connaissance** : enrichissez `knowledge_base.csv` et régénérez le prompt.

---

## Licence

Ce projet est distribué sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## Support

Pour toute question, suggestion ou anomalie :
1. Consultez les [issues existantes](https://github.com/monsieurMechant200/GOOD-DEAL-CHAT/issues).
2. Ouvrez une nouvelle issue en décrivant clairement le contexte, le comportement attendu et les éventuels messages d’erreur.

---

*Propulsé par DATAIKOS pour les alumni GOOD-DEAL - parce que chaque question mérite une réponse stellaire.*

Ce README reflète la maturité technique du projet tout en restant accueillant pour les nouveaux utilisateurs. Vous pouvez l’adapter encore selon vos préférences (badges supplémentaires, captures d’écran de l’interface cosmique, etc.).
