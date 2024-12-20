from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from cart.forms import QuantityForm
from shop.models import Product, Category
from .models import Product
from .forms import AddToCartForm
from .forms import CommentForm
from cart.utils.cart import Cart
from django.contrib import messages

@login_required
def add_to_cart(request, product_id):
    # Buscar el producto por ID
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    form = AddToCartForm(request.POST)

    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        cart.add(product=product, quantity=quantity)
        messages.success(request, f'{quantity} {product.title} añadido(s) al carrito.')
    else:
        messages.error(request, 'Por favor, ingresa una cantidad válida.')

    # Redirige a la página de detalles del producto
    return redirect('shop:product_detail', slug=product.slug)

def paginat(request, list_objects):
	p = Paginator(list_objects, 15)
	page_number = request.GET.get('page')
	try:
		page_obj = p.get_page(page_number)
	except PageNotAnInteger:
		page_obj = p.page(1)
	except EmptyPage:
		page_obj = p.page(p.num_pages)
	return page_obj


def home_page(request):
	products = Product.objects.all()
	context = {'products': paginat(request ,products)}
	return render(request, 'home_page.html', context)

@login_required
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).all()[:5]
    form = AddToCartForm(request.POST or None)
    comments = product.comments.all()
    comment_form = CommentForm(request.POST or None)

    if request.method == 'POST':
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comentario añadido correctamente.')
            return redirect('shop:product_detail', slug=slug)

        if form.is_valid():
            cart = Cart(request)
            quantity = form.cleaned_data['quantity']
            cart.add(product=product, quantity=quantity)
            messages.success(request, f'{quantity} {product.title} añadido(s) al carrito.')
            return redirect('shop:product_detail', slug=slug)

    context = {
        'product': product,
        'comments': comments,
        'comment_form': comment_form,
        'form': form,
        'related_products': related_products,
    }
    return render(request, 'product_detail.html', context)


@login_required
def add_to_favorites(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	request.user.likes.add(product)
	return redirect('shop:product_detail', slug=product.slug)


@login_required
def remove_from_favorites(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	request.user.likes.remove(product)
	return redirect('shop:favorites')


@login_required
def favorites(request):
	products = request.user.likes.all()
	context = {'title':'Favorites', 'products':products}
	return render(request, 'favorites.html', context)

def search(request):
	query = request.GET.get('q')
	products = Product.objects.filter(title__icontains=query).all()
	context = {'products': paginat(request ,products)}
	return render(request, 'home_page.html', context)


def filter_by_category(request, slug):
	#El usuario da clic en las categorias y se desplegan las categorias con subcategorias
	result = []
	category = Category.objects.filter(slug=slug).first()
	[result.append(product) \
		for product in Product.objects.filter(category=category.id).all()]
	# se comprueba si la categoria es padre de las subcategorias
	if not category.is_sub:
		sub_categories = category.sub_categories.all()
		# se obtienen las subcategorias de todas las categorias
		for category in sub_categories:
			[result.append(product) \
				for product in Product.objects.filter(category=category).all()]
	context = {'products': paginat(request ,result)}
	return render(request, 'home_page.html', context)



