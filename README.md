# 🖼️ SRI — Système de Recherche d'Images (Content-Based Image Retrieval)

Application web Django permettant de rechercher des images de deux façons :
- **par mots-clés** (recherche classique dans une base annotée)
- **par similarité visuelle** : on uploade une image, le système renvoie les images les plus visuellement proches, en s'appuyant sur des caractéristiques extraites par le réseau de neurones **VGG16** (pré-entraîné sur ImageNet) et une recherche des plus proches voisins (**KNN**, similarité cosinus).

## 🎯 Objectif

Explorer la recherche d'images par le contenu (*Content-Based Image Retrieval*, CBIR) : au lieu de dépendre uniquement de tags/mots-clés saisis manuellement, le système compare directement l'apparence visuelle des images entre elles.

## 🛠️ Stack technique

| Composant | Rôle |
|---|---|
| **Django** | Backend web (modèles, vues, formulaires, templates) |
| **TensorFlow / Keras (VGG16)** | Extraction de caractéristiques visuelles (feature embeddings) |
| **scikit-learn** | Recherche des plus proches voisins (`NearestNeighbors`, cosine) |
| **Pillow** | Chargement / redimensionnement des images |
| **SQLite** | Base de données (mots-clés, métadonnées images, features stockées en binaire) |

## 🧠 Fonctionnement

### Recherche par mots-clés
```
Formulaire (mot-clé) → filtre Image.objects.filter(keywords__name__icontains=...) → résultats
```

### Recherche par similarité d'image
```
Image uploadée
      │
      ▼
VGG16 (poids ImageNet, sans la tête de classification)
      │
      ▼
Vecteur de caractéristiques (feature embedding)
      │
      ▼
Comparaison avec les embeddings de toutes les images en base (similarité cosinus, KNN)
      │
      ▼
3 images les plus proches renvoyées
```

Chaque image en base a ses caractéristiques VGG16 pré-calculées et stockées (`image_features`, `BinaryField`) au moment de son ajout, pour éviter de recalculer les features de toute la base à chaque recherche.

## 📁 Structure du projet

```
sri/
├── manage.py
├── requirements.txt
├── sri/                          # Configuration Django (settings, urls, wsgi)
└── images/                       # Application principale
    ├── models.py                 # Modèles Image / Keyword + extraction VGG16
    ├── views.py                  # Recherche par mots-clés + recherche par similarité
    ├── urls.py
    ├── templates/images/         # search.html, results.html, upload_images.html, similar_images.html
    └── media/images/             # Images de démonstration (tigre, ours, cheval, oiseau, parapluie)
```

## 🚀 Installation et lancement

```bash
# 1. Cloner le repo
git clone https://github.com/<ton-user>/sri-image-retrieval.git
cd sri-image-retrieval

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate      # Windows : venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Appliquer les migrations
python manage.py migrate

# 5. (Optionnel) Créer un compte admin pour ajouter des images via /admin/
python manage.py createsuperuser

# 6. Lancer le serveur
python manage.py runserver
```

Rends-toi sur `http://127.0.0.1:8000/` pour la recherche par mots-clés, ou `http://127.0.0.1:8000/upload/` pour la recherche par image.

## 📊 Utilisation

- **Recherche par mots-clés** : tape un mot-clé associé à une ou plusieurs images (ex. "tigre") → la page affiche les images correspondantes.
- **Recherche par image** : uploade une photo → le système renvoie les 3 images les plus visuellement similaires dans la base.

## 📄 Licence

Ce projet est distribué sous licence MIT — voir le fichier [LICENSE](LICENSE).
