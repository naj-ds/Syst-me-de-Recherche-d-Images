from django.urls import path
from images import views

urlpatterns = [
    path('search/', views.search_by_keywords, name='search'),  # URL pour la recherche par mots-clés
    path('upload/', views.search_similar_images, name='upload_image'),  # URL pour la recherche d'images similaires

    # Ajoutez d'autres URL pour vos vues si nécessaire
]
