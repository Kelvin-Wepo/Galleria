from django.test import TestCase
from .models import Location, Category, Image

# Create your tests here.
"""
Test methods for location
"""
class LocationTestClass(TestCase):
    def setUp(self):
        self.location = Location(name='Kenya')
        self.location.save_location()

    def test_instance(self):
        self.assertTrue(isinstance(self.location, Location))

    """ 
    Testing save method 
    """
    def test_save(self):
        self.location.save_location()
        locations=Location.objects.all()
        self.assertTrue(len(locations)>0)

    # Testing delete method
    def test_delete(self):
        self.location.delete_location()
        locations=Location.objects.all()
        self.assertTrue(len(locations)==0)

"""
Test methods for category
"""
class CategoryTestClass(TestCase):
    def setUp(self):
        self.category = Category(name='nature')
        self.category.save_category()

    def test_instance(self):
        self.assertTrue(isinstance(self.category, Category))

    # Testing save method
    def test_save(self):
        self.category.save_category()
        categories=Category.objects.all()
        self.assertTrue(len(categories)>0)

    # Testing delete method
    def test_delete(self):
        self.category.delete_category()
        categories=Category.objects.all()
        self.assertTrue(len(categories)==0)
"""
Test methods for the Image class
"""
class ImageTestClass(TestCase):

    # set up method
    def setUp(self):
        self.location = Location(name='Kenya')
        self.location.save_location()

        self.category = Category(name='nature')
        self.category.save_category()
        
        self.image= Image(image='hallow', name='ugly', photographer='kwepo', description='not what I expected', location=self.location, category=self.category)
        self.image.save_image()

    # Testing instance
    def test_instance(self):
        self.assertTrue(isinstance(self.image,Image))

    # Testing save method
    def test_save(self):
        self.image.save_image()
        images=Image.objects.all()
        self.assertTrue(len(images)>0)

    # Testing delete method
    def test_delete(self):
        self.image.delete_image()
        images=Image.objects.all()
        self.assertTrue(len(images)==0)

    def test_update_image(self):
        self.image.save_image()
        self.image.update_image(self.image.id, 'images/image1.jpeg')
        updated_image = Image.objects.filter(image='images/image2.jpeg')
        self.assertFalse(len(updated_image) > 0)

    def test_get_image_by_id(self):
        image_found = self.image.get_image_by_id(self.image.id)
        images = Image.objects.filter(id=self.image.id)
        self.assertTrue(image_found, images)

    def test_search_image_by_category(self):
        category = 'nature'
        image_found = self.image.search_by_category(category)
        self.assertFalse(len(image_found) > 1) 

    def test_filter_by_location(self):
        self.image.save()
        images_found = self.image.filter_by_location(location='Kenya')
        self.assertFalse(len(images_found) > 0)  

    def tearDown(self):
        Image.objects.all().delete()
        Location.objects.all().delete()
        Category.objects.all().delete()
