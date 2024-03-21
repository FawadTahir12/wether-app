from django.shortcuts import render


def search(request):
    return render(request,'app/search.html',{})

def favoriteCities(request):
    return render(request,'app/favourites.html',{})
    
