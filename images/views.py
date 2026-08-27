from django.shortcuts import render
from PIL import Image as PILImage
from tensorflow.keras.applications import VGG16
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .models import Image
from sklearn.neighbors import NearestNeighbors

from django.db.models import Q

def search_by_keywords(request):
    results = None
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        
        # Search for distinct images corresponding to the entered keyword
        results = Image.objects.filter(keywords__name__icontains=search_query).distinct()
        print(results)

        if results.exists():  # If there are results, display them
            return render(request, 'images/results.html', {'results': results})
    
    return render(request, 'images/search.html', {'results': results})


def extract_vgg_features(image_file):
    model = VGG16(weights='imagenet', include_top=False)
    
    img = PILImage.open(image_file)
    img = img.resize((224, 224))
    img_array = keras_image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    features = model.predict(img_array)
    flattened_features = features.flatten()

    return flattened_features

def search_similar_images(request):
    if request.method == 'POST' and request.FILES.get('image_file'):
        uploaded_image = request.FILES['image_file']
        
        model = VGG16(weights='imagenet', include_top=False)
        
        img = PILImage.open(uploaded_image)
        img = img.resize((224, 224))
        img_array = keras_image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        features = model.predict(img_array)
        uploaded_image_features = features.flatten()  # Get features as a 1D array

        similar_images = []
        all_image_features = []
        all_images = Image.objects.all()
        for img_obj in all_images:
            db_image_features = np.frombuffer(img_obj.image_features, dtype=np.float32)
            all_image_features.append(db_image_features)

        # Convertir en une liste pour le KNN
        all_image_features = np.array(all_image_features)
        
        # Créer un objet NearestNeighbors
        nn = NearestNeighbors(n_neighbors=3, metric='cosine')
        nn.fit(all_image_features)

        # Rechercher les plus proches voisins pour l'image téléchargée
        distances, indices = nn.kneighbors([uploaded_image_features])

        # Récupérer les images similaires
        for index in indices.flatten():
            img_obj = all_images[int(index)]  # Convertir l'index en un entier
            similar_images.append({'image': img_obj.image_file.url})

        return render(request, 'images/similar_images.html', {'similar_images': similar_images})
    
    return render(request, 'images/upload_images.html')
