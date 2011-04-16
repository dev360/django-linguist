#coding=utf-8

from django.db.models import Q

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from testapp.models import Product, ProductTranslation

def list(request):
    products = ProductTranslation.objects.filter(locale='en')
    return render_to_response('testapp/list.html', {
        'products': products,
    }, RequestContext(request))

def search(request):
    qs = ProductTranslation.objects.filter(locale='en').order_by('model_number')
    
    if request.method == 'POST':
        arg = request.POST['search']
        
        #
        # Notice that we are just using `model_number` as 
        # if its part of ProductTranslation, when it actually
        # is part of the parent object, i.e. Product.
        #
        
        qs = qs.filter( Q(model_number__icontains=arg)|
                        Q(title__icontains=arg)|
                        Q(description__icontains=arg))
    
    products = qs
    
    return render_to_response('testapp/list.html', {
        'products': products,
    }, RequestContext(request))


def view(request, slug):
    if request.method == 'POST':
        return add_product(request)
    product = get_object_or_404(Product, slug=slug)
    random_products = Product.available\
            .exclude(pk=product.pk)\
            .filter(is_additional=False)\
            .order_by("?")[:3]
    return render_to_response('testapp/view.html', {
        'product': product,
    }, RequestContext(request))
