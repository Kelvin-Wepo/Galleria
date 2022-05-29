from django.db import models

# Create your models here.

class Location(models.Model):
    name = models.CharField(max_length=100)

    def save_location(self):
        self.save()

    def delete_location(self):
        self.delete()

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)

    def save_category(self):
        self.save()

    def delete_category(self):
        self.delete()

    def __str__(self):
        return self.name

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=100)
    photographer = models.CharField(max_length=50)
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()

    @classmethod
    def update_image(cls, id, value):
        image = cls.objects.filter(id=id).update(image=value)

    @classmethod
    def get_image_by_id(cls, id):
        image = cls.objects.filter(id=id).all()
        return image

    @classmethod
    def search_by_category(cls, category):
        images = cls.objects.filter(category__name__icontains=category)
        return images

    @classmethod
    def filter_by_location(cls, location):
        images = Image.objects.filter(name=location).all()
        return images


    def __str__(self):
        return self.name
        
    """
    Meta subclass to order images from latest
    """
    class Meta:
        ordering = ['-date_posted'] 
# Create your models here.
