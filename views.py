# from django.views.generic import ListView
from django.shortcuts import render,redirect,get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from plush.settings import EMAIL_HOST_USER
from django.views.generic import View
from django.contrib.auth.models import User
from plush_app.models import Category,Contact,Order,OrderItem, ShopProduct, FontawesomeDesc,Login, FontawesomeDesc2, FontawesomeDesc3, FlashSale, MeetUs, Testimonials, Media,Carosue
from plush_app.forms import ContactForm, Register, EditProfileForm, LoginForm, CartAddProductForm, OrderCreateForm
from django.contrib import messages
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth import login, authenticate,logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes,force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from plush_app.tokens import account_activation_token
from django.core.mail import EmailMessage
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from .filters import UserFilter
from django.db.models import Q
from django.views.decorators.http import require_POST
from plush_app.cart import Cart
from django.contrib.admin.views.decorators import staff_member_required
# import weasyprint

# @staff_member_required
# def admin_order_pdf(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     html = render_to_string('plush_app/pdf.html',{'order': order})
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'filename=\
#         "order_{}.pdf"'.format(order.id)
#     weasyprint.HTML(string=html).write_pdf(response,stylesheets=[weasyprint.CSS(
#         settings.STATIC_ROOT + 'css/pdf.css')])
#     return response

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,'admin/detail.html',{'order': order})

@login_required
def payteuiosth(request):
    cart = Cart(request)
    return render(request,'plush_app/order.html',{'cart':cart})


@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    product_price1=item['product_price1'],
                    quantity=item['quantity']
                )
            cart.clear()
            paid=True
        return render(request, 'plush_app/thankyou.html', {'order': order,'cart':cart})
    else:
        form = OrderCreateForm()
    return render(request, 'plush_app/checkout.html', {'form': form,'cart':cart})

def shop(request, category_slug=None):
    car = Carosue.objects.all()
    cart = Cart(request)
    category = None
    categories = Category.objects.all()
    products = ShopProduct.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = ShopProduct.objects.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'car': car,
        'cart':cart
    }
    return render(request, 'plush_app/shop.html', context)


def shop_single(request, id, slug, category_slug=None):
    cart = Cart(request)
    product = get_object_or_404(ShopProduct, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    products = ShopProduct.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = ShopProduct.objects.filter(category=category)

    context = {
        'product': product,
        'products': products,
        'cart_product_form': cart_product_form,
        'cart': cart
    }
    return render(request, 'plush_app/shop-single.html', context)


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(ShopProduct, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('plush_app:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(ShopProduct, id=product_id)
    cart.remove(product)
    return redirect('plush_app:cart_detail')


@login_required
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'plush_app/cart.html', {'cart': cart})


def index(request, category_slug=None):
    car = Carosue.objects.all()
    cart = Cart(request)
    fornt = FontawesomeDesc.objects.all()
    fornt2 = FontawesomeDesc2.objects.all()
    fornt3 = FontawesomeDesc3.objects.all()
    flash = FlashSale.objects.all()
    category = None
    categories = Category.objects.all()
    products = ShopProduct.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = ShopProduct.objects.filter(category=category)

    return render(request, 'plush_app/index.html', {'car': car, 'cart': cart, 'category': category, 'categories': categories, 'products': products, 'fornt': fornt, 'fornt2': fornt2, 'fornt3': fornt3, 'flash': flash})


def about(request):
    media = Media.objects.all()
    cart = Cart(request)
    flash = FlashSale.objects.all()
    meet = MeetUs.objects.all()
    test = Testimonials.objects.all()
    fornt = FontawesomeDesc.objects.all()
    fornt2 = FontawesomeDesc2.objects.all()
    fornt3 = FontawesomeDesc3.objects.all()
    return render(request, 'plush_app/about.html',{'media':media,'cart':cart,'flash':flash,'meet':meet,'test':test,'fornt':fornt,'fornt2':fornt2,'fornt3':fornt3})

def contact(request):
    cart = Cart(request)
    flash = FlashSale.objects.all()
    contact = Contact.objects.all()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            sender_name = form.cleaned_data['name']
            sender_email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            try:
                send_mail(sender_name, message, sender_email,
                          ['plushconceptfashionstore@gmail.com'])
                return HttpResponse('success')
            except BadHeaderError:
                # form.save(commit=True)
                return HttpResponse('Invalid header found.')
    else:
        form = ContactForm()
    return render(request, 'plush_app/contact.html', {'cart':cart,'contact': contact, 'form': form, 'flash':flash})

# def contact(request):
#     cart = Cart(request)
#     flash = FlashSale.objects.all()
#     contact = Contact.objects.all()
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             if form.is_valid():
#                 sender_name = form.cleaned_data['name']
#                 sender_email = form.cleaned_data['email']
#                 message = form.cleaned_data['message']
#                 email_msg = EmailMessage(subject=f"{sender_name}" 'reply from plush fashion store contact page', body=message, from_email='helpdesk@plushfashionstore.com',
#                                      to=['helpdesk@plushfashionstore.com'], headers={'Reply-To': sender_email})
#                 email_msg.send()
#                 form = ContactForm()
#     else:
#         form = ContactForm()
#     return render(request, 'plush_app/contact.html', {'cart':cart,'contact': contact, 'form': form, 'flash':flash})
   


@login_required
def success(request):
    return HttpResponse('Message sent! Thank you for your message.')

@login_required    
def checkout(request):
    user = request.user
    carts = OrderItem.objects.filter(user=user)
    orders = Order.objects.filter(user=user, ordered=False)
    ship = ShippingDelivery.objects.all()
    if carts.exists():
        order = orders[0]
        return render(request, 'plush_app/checkout.html', {'carts': carts, 'order': order, 'ship': ship})
    else:
        return render(request, "plush_app/checkout.html")

@login_required
def thankyou(request):
    cart = Cart(request)
    return render(request, 'plush_app/thankyou.html',{'cart':cart})

@login_required
def activation_sent(request):
    return render(request,'plush_app/activation_sent.html')


def register(request):
    flash = FlashSale.objects.all()
    if request.method == 'POST':
        form = Register(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('plush_app/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = Register()
    return render(request,'registration/register.html',{'form':form, 'flash':flash})
    
@login_required
def activate1(request,token,uidb64):
    return render(request,'plush_app/activation.html')

@login_required
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
        

@login_required  
def addtocart(request, slug):
    item = get_object_or_404(ShopProduct, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        purchased=False
        )

    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity +=1 
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        # ordered_date = timezone.now()
        order = Order.objects.create(user=request.user)
        order.items.add(order_item)
    return render(request,'plush_app/cart_message.html')

@login_required
def removefromcart(request,slug):
    item = get_object_or_404(ShopProduct, slug=slug)
    orderitem_qs = OrderItem.objects.filter(user=request.user, item=item)
    if orderitem_qs.exists():
        item = orderitem_qs[0]
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            orderitem_qs.delete()
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False
        )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
            )[0]
            order.items.remove(order_item)
            messages.info(request,"This item was removed from your cart")
            return render(request,'plush_app/cart_message2.html')
        else:
            messages.info(request,"This item was not in your cart")
            return render(request,'plush_app/cart_message2.html')
    else:
        messages.info(request,"You do not have an active order")
        return render(request,'plush_app/shop.html')

@login_required
def logoutpage(request):
    # if request.method =="POST":
        logout(request)
        return render(request,'plush_app/logout.html')
    
def searchposts(request):
    if request.method == 'GET':
        query = request.GET.get('q')

        submitbutton = request.GET.get('submit')

        if query is not None:
            lookups = Q(product_name1__icontains=query)

            results = ShopProduct.objects.filter(lookups).distinct()

            context = {'results': results,
                       'submitbutton': submitbutton}

            return render(request, 'plush_app/search.html', context)

        else:
            return render(request, 'plush_app/index.html')

    else:
        return render(request, 'plush_app/index.html')


def searchfilter(request):
    if request.method == 'GET':
        query = request.GET.get('q')

        submitbutton = request.GET.get('submit')

        if query is not None:
            lookups = Q(product_price1__icontains=query)

            results = ShopProduct.objects.filter(lookups).distinct()

            context = {'results': results,
                       'submitbutton': submitbutton}

            return render(request, 'plush_app/filterlist.html', context)

        else:
            return render(request, 'plush_app/shop.html')

    else:
        return render(request, 'plush_app/shop.html')

def gallery(request):
    media = Media.objects.all()
    return render(request, 'plush_app/gallery.html', {'media': media})