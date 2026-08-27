from django.db import models
from PIL import Image as PILImage
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image
import numpy as np

class Keyword(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Image(models.Model):
    title = models.CharField(max_length=100)
    image_file = models.ImageField(upload_to='images/')
    image_features = models.BinaryField(blank=True, null=True)
    keywords = models.ManyToManyField(Keyword, related_name='images')

    def extract_vgg_features(self):
        model = VGG16(weights='imagenet', include_top=False)
        
        img = PILImage.open(self.image_file)
        img = img.resize((224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        features = model.predict(img_array)
        flattened_features = features.flatten()

        return flattened_features.tobytes()

    def save_vgg_features(self):
        vgg_features = self.extract_vgg_features()
        self.image_features = vgg_features
        super(Image, self).save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.keywords.exists():
            self.keywords.clear()
        for keyword in self.keywords.all():
            self.keywords.add(keyword)
