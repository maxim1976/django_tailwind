from .cart import Cart

#Create context proccessors so our cart can work on all pages of our site

def cart(request):
    return {'cart': Cart(request)}