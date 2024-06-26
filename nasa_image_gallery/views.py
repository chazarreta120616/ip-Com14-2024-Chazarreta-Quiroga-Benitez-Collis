# capa de vista/presentación
# si se necesita algún dato (lista, valor, etc), esta capa SIEMPRE se comunica con services_nasa_image_gallery.py

from django.shortcuts import redirect, render
from .layers.services import services_nasa_image_gallery
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse
from .layers.services import services_nasa_image_gallery
from django.contrib.auth import authenticate, login, logout
from .google_translate import translate_text

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('Usuario o contraseña incorrectos.')
    return render(request, 'login.html')

# función que invoca al template del índice de la aplicación.
def index_page(request):
    return render(request, 'index.html')

# auxiliar: retorna 2 listados -> uno de las imágenes de la API y otro de los favoritos del usuario.
def getAllImagesAndFavouriteList(request):
    images = services_nasa_image_gallery.getAllImages()
    favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request) if request.user.is_authenticated else []
    return images, favourite_list


# función principal de la galería.
def home(request):
    images, favourite_list = getAllImagesAndFavouriteList(request)
    return render(request, "home.html", {"images": images, "favourite_list": favourite_list})



# función utilizada en el buscador.
def search(request):
    images, favourite_list = getAllImagesAndFavouriteList(request)
    search_msg = request.POST.get("query", "")

    if search_msg != "":
        # Traduce la palabra al inglés si es necesario
        translated_search_msg = translate_text(search_msg, 'en')
        # Busca imágenes usando la palabra traducida
        images_filtered = services_nasa_image_gallery.getImagesBySearchInputLike(translated_search_msg)
        return render(request, "home.html", {"images": images_filtered, "favourite_list": favourite_list})
    else:
        return redirect("home")


# las siguientes funciones se utilizan para implementar la sección de favoritos: traer los favoritos de un usuario, guardarlos, eliminarlos y desloguearse de la app.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = []
    return render(request, 'favourites.html', {'favourite_list': favourite_list})


@login_required
def saveFavourite(request):
    pass


@login_required
def deleteFavourite(request):
    pass


@login_required 
def exit(request):     
    logout(request)     
    return redirect('index-page')