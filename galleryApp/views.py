from django.shortcuts import render
from .models import Location, Category, Image


# Create your views here.
def home(request):
    images = Image.objects.all()
    category = Category.objects.all()
    
    return render(request, 'home.html', {'images':images})

def search_images(request):

    if 'images' in request.GET and request.GET["images"]:
        category = request.GET.get("images")
        searched_images = Image.search_by_category(category)
        message = f"{category}"

        return render(request, 'search.html',{"message":message,"images": searched_images})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})



# Create your views here.
