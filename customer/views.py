from django.shortcuts import render,redirect,get_object_or_404
from myadmin.models import *
from customer.models import *
from saler.models import *
from django.contrib.auth.models import User
from django.contrib import auth,messages
from datetime import date
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import razorpay
from .utils import common_category
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

#Email
from django.conf import settings
from io import BytesIO
from django.core.mail import EmailMessage

#Invoice
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.colors import HexColor
from reportlab.lib import colors
import io

#AutoComplate
from django.http import JsonResponse
from django.urls import reverse


def layout(request):
    # category = Categories.objects.all()
    # context = {'category':category}

    context = common_category()
    return render(request,'customer/layout.html',context)


def index(request):
    category = Categories.objects.all()
    category_ids = category.values_list('id', flat=True)

    product = Product.objects.filter(categories_id__in=category_ids)

    context = {'category':category,'product':product}
    context.update(common_category())

    return render(request,'customer/index.html',context)

def autocomplete(request):
    if 'term' in request.GET:
        qs = Product.objects.filter(product_name__icontains=request.GET.get('term'))
        results = []
        for product in qs:
            product_dict = {
                'name': product.product_name,
                'url': reverse('product_detail', args=[product.id])
            }
            results.append(product_dict)
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)


# Login Crud
def login(request):
    context = common_category()
    return render(request,'customer/login.html',context)

def login_check(request):
    if request.method == 'POST':
        myusername = request.POST.get('username')
        mypassword = request.POST.get('password')

        if not myusername or not mypassword:
            messages.error(request, "Username and password are required.")
            return redirect('/customer/login')

        result = auth.authenticate(username=myusername, password=mypassword)
        if result is None:
            messages.error(request, "Invalid Username or Password 🤭")
            return redirect('/customer/login')
        else:
            try:
                user_register = Register.objects.get(user=result)
                user_status = user_register.status 
                if user_status == 'Pending':
                    messages.error(request, "Your account is still pending approval.")
                    return redirect('/customer/login')
                else:
                    auth.login(request, result)
                    return redirect('/customer/index')
            except Register.DoesNotExist:
                messages.error(request, "User profile does not exist.")
                return redirect('/customer/login')
    else:
        return render(request, 'customer/login.html') 
     
# Logout
def logout(request):
	auth.logout(request)
	return redirect('/customer/login')

def register(request):
    state = State.objects.all()
    city = City.objects.all()
    area = Area.objects.all()

    context = {'state':state,'city':city,'area':area}
    context.update(common_category())
    return render(request,'customer/register.html',context)

def check_username(request,uname):
    if User.objects.filter(username=uname).exists():
        return False 
    else:
        return True    

def check_email(request,email):
    if User.objects.filter(email=email).exists():
        return False
    else:
        return True

def check_contact(request,contact):
    if Register.objects.filter(contact=contact).exists():
        return False
    else:
        return True

def store_register(request):
    myfirst_name = request.POST['first_name']
    mylast_name = request.POST['last_name']
    myemail = request.POST['email']
    myusername = request.POST['username']
    mypassword = request.POST['password']
    mycpassword = request.POST['cpassword']

    mycontact = request.POST['contact']
    mydob = request.POST['dob']
    mygender = request.POST['gender']
    myaddress = request.POST['address']
    mystate= request.POST['state']
    mycity= request.POST['city']
    myarea= request.POST['area']
    mydate = date.today()


    if mypassword == mycpassword and check_username(request,myusername) and check_email(request,myemail) and check_contact(request,mycontact):
        user = User.objects.create_user(first_name=myfirst_name,last_name=mylast_name,email=myemail,username=myusername,password=mypassword)
        Register.objects.create(contact=mycontact,dob=mydob,gender=mygender,address=myaddress,state_id=mystate,city_id=mycity,area_id=myarea,user_id=user.id,date=mydate)

        return redirect('/customer/login')
    else:
        if check_username(request,myusername) is False:
            messages.error(request,'UserName Already Exists...') 
            return redirect('/customer/register')
        elif check_email(request,myemail) is False:
            messages.error(request,'Email Already Exists...') 
            return redirect('/customer/register')
        elif check_contact(request,mycontact) is False:
            messages.error(request,'Contact Already Exists...') 
            return redirect('/customer/register')
        
# Conatct Crud
def contact(request):
    context = {}
    context.update(common_category())
    return render(request,'customer/contact.html',context)

def insert_contact(request):
    myname = request.POST['name']
    myemail = request.POST['email']
    mycontact = request.POST['contact']
    mymessage = request.POST['message']
    mydate = date.today()

    Contact.objects.create(name=myname,email=myemail,contact=mycontact,message=mymessage,date=mydate)
    return redirect('/customer/contact')

#saler Registration
def saler_reg(request):
    state = State.objects.all()
    city = City.objects.all()
    area = Area.objects.all()
    user = User.objects.all()

    context = {'state':state,'city':city,'area':area,'user':user}
    context.update(common_category())
    return render(request,'customer/saler_reg.html',context)

def store_reg(request):
    myfirst_name = request.POST['first_name']
    mylast_name = request.POST['last_name']
    myemail = request.POST['email']
    myusername = request.POST['username']
    mypassword = request.POST['password']
    mycpassword = request.POST['cpassword']
    
    myshop_name= request.POST['shop_name']
    myshop_address= request.POST['shop_address']
    myshop_contact= request.POST['shop_contact']
    mysid= request.POST['state']
    mycid= request.POST['city']
    myaid= request.POST['area']
    myshop_image = request.FILES['shop_image']
    mydate = date.today()

    mylocation = os.path.join(settings.MEDIA_ROOT, 'upload')
    obj = FileSystemStorage(location=mylocation)
    obj.save(myshop_image.name, myshop_image)
    if mypassword == mycpassword and check_username(request,myusername) and check_email(request,myemail):
        user = User.objects.create_user(first_name=myfirst_name,last_name=mylast_name,email=myemail,username=myusername,password=mypassword)
        Saler_reg.objects.create(shop_name=myshop_name,shop_address=myshop_address,shop_contact=myshop_contact,user_id=user.id,state_id=mysid,city_id=mycid,area_id=myaid,image=myshop_image,date=mydate)

        return redirect('/saler/login')
    else:
        if check_username(request,myusername) is False:
            messages.error(request,'UserName Already Exists...') 
            return redirect('/customer/saler_reg')
        elif check_email(request,myemail) is False:
            messages.error(request,'Email Already Exists...') 
            return redirect('/customer/saler_reg') 

def delete_reg(request,id):
    result = Saler_reg.objects.get(pk=id)
    result.delete()
    return redirect('/myadmin/all_salers')

def edit_reg(request,id):
    result = Saler_reg.objects.get(pk=id)
    state = State.objects.all()
    city = City.objects.all()
    area = Area.objects.all()

    context={'result':result,'state':state,'city':city,'area':area}
    return render(request,'salers/edit_reg.html',context)


def update_reg(request,id):
    myfirst_name = request.POST['fname']
    mylast_name = request.POST['lname']
    myemail = request.POST['email']
    myusername = request.POST['username']
   
    
    mysaler_contact= request.POST['saler_contact']
    myshop_name= request.POST['shop_name']
    myshop_address= request.POST['shop_address']
    myshop_contact= request.POST['shop_contact']
    mysid= request.POST['sid']
    mycid= request.POST['cid']
    myaid= request.POST['aid']
    myshop_image = request.FILES['shop_image']

    mylocation = os.path.join(settings.MEDIA_ROOT, 'upload')
    obj = FileSystemStorage(location=mylocation)
    obj.save(myshop_image.name, myshop_image)

    data = {
            'first_name':myfirst_name,
            'last_name':mylast_name,
            'email':myemail,
            'username':myusername
    }

    data1 = {
            'saler_contact':mysaler_contact,
            'shop_name':myshop_name,
            'shop_address':myshop_address,
            'shop_contact':myshop_contact,
            'state_id':mysid,
            'city_id':mycid,
            'area_id':myaid,
            'image':myshop_image
    }
     
    user_id = request.user.id
    saler = Saler_reg.objects.get(user_id=user_id)

    User.objects.update_or_create(pk=user_id,defaults=data)
    Saler_reg.objects.update_or_create(pk=saler.id,defaults=data1)
    return redirect('/myadmin/all_salers')

#Get Product
def product_list(request,id):
    categories = Categories.objects.all()
    product = Product.objects.filter(categories_id=id)
    context = {'categories':categories,'product':product}
    context.update(common_category())
    return render(request,'customer/product_list.html',context)

def product_detail(request,id):
    product = Product.objects.get(pk=id)
    available_sizes = set(product.size.split(','))  

    context = {'product':product,'available_sizes':available_sizes}
    context.update(common_category())
    return render(request,'customer/product_detail.html',context)

#Cart 
@login_required
def cart(request):
    if request.method == 'POST':
        cart_id = request.POST.get('cart_id')
        quantity = int(request.POST.get('quantity'))
        cart_item = Cart.objects.get(id=cart_id)
        cart_item.quantity = quantity
        cart_item.save()
        return redirect('/customer/cart')
    
    user_id = request.user.id
    cart_items = Cart.objects.filter(user_id=user_id)
    count = cart_items.count()

    subtotal = 0

    for item in cart_items:
        item.total_price = int(item.product.price) * int(item.quantity)
        subtotal += item.total_price

    context = {'cart': cart_items,'subtotal':subtotal,'count':count}
    context.update(common_category())
    return render(request, 'customer/cart.html', context)

@login_required
def insert_cart(request):
    user_id = request.user.id
    seller = request.POST['sel_id']
    product = request.POST['product_id']
    quantity = request.POST.get('quantity', 1)
    # size = request.POST['size']

    Cart.objects.create(user_id=user_id, saler_id=seller, product_id=product, quantity=quantity)
    return redirect('/customer/cart')

def delete_cart(request,id):
    result = Cart.objects.get(pk=id)
    result.delete()
    return redirect('/customer/cart')

#CheckOut
@login_required
def checkout(request):
    user_id = request.user.id
    cart_items = Cart.objects.filter(user_id=user_id)
    subtotal = 0

    for item in cart_items:
        item.total_price = int(item.product.price) * int(item.quantity)
        subtotal += item.total_price

    state = State.objects.all()
    city = City.objects.all()
    area = Area.objects.all()

    context = {'cart': cart_items,'subtotal':subtotal,'state':state,'city':city,'area':area}
    context.update(common_category())
    return render(request,'customer/checkout.html',context)

@login_required
def store_checkout(request):
    mydate = date.today()
    myuser_id = request.user.id
    myamount = request.POST['amount']
    mysaler_id = request.POST['saler_id']
    mypay_method = request.POST['payment']

    order = Order.objects.create(date=mydate,user_id=myuser_id,amount=myamount,saler_id=mysaler_id,pay_method=mypay_method)
    
    if order.id:
        
        myaddress = request.POST['address']
        mystate = request.POST['state']
        mycity = request.POST['city']
        myarea = request.POST['area']
        mypincode = request.POST['pincode']
        myfirstname = request.POST['firstname']
        mylastname = request.POST['lastname']
        myemail = request.POST['email']
        mycontact = request.POST['contact']
        myamount = request.POST['amount']

        Shipping.objects.create(order_id=order.id,address=myaddress,state_id=mystate,city_id=mycity,area_id=myarea,pincode=mypincode,firstname=myfirstname,lastname=mylastname,email=myemail,contact=mycontact,amount=myamount)
        Billing.objects.create(order_id=order.id,address=myaddress,state_id=mystate,city_id=mycity,area_id=myarea,pincode=mypincode,firstname=myfirstname,lastname=mylastname,email=myemail,contact=mycontact,amount=myamount)
        
        product_ids = request.POST.getlist('product_id')
        quantities = request.POST.getlist('quantity')
        sizes = request.POST.getlist('size')
        product_amounts = request.POST.getlist('total_price')
        print(f"Lengths - product_ids: {len(product_ids)}, quantities: {len(quantities)}, sizes: {len(sizes)}, product_amounts: {len(product_amounts)}")

    
        for i in range(len(product_ids)):
            product_id = product_ids[i]
            quantity = quantities[i]
            size = sizes[i]
            amount = product_amounts[i]

            Order_details.objects.create(order_id=order.id,product_id=product_id,quantity=quantity,size=size,amount=amount)

    if mypay_method.lower() == 'cod':
        return redirect('/customer/success')
    else:
        request.session['price'] = order.amount
        request.session['id'] = order.id
        return redirect('/customer/payment')
    
@login_required
def payment(request):
    user_id = request.user.id
    cart_items = Cart.objects.filter(user_id=user_id)
    subtotal = 0
    for item in cart_items:
        item.total_price = int(item.product.price) * int(item.quantity)
        subtotal += item.total_price

    key_id = 'rzp_test_PvM4GxK9MYlCUc'
    key_secret = 'WzsOTRAU4l3oAA1CS7jlVS5E'

    amount = int(request.session['price'])*100

    client = razorpay.Client(auth=(key_id, key_secret))

    data = {
        'amount': amount,
        'currency': 'INR',
        "receipt":"order",
        "notes":{
            'name' : request.user.first_name,
            'payment_for':'order Test'
        }
    }
    
    payment = client.order.create(data=data)

    request.session['payment'] = True

    context = {'payment' : payment,'cart': cart_items,'subtotal':subtotal}
    return render(request, 'customer/payment.html',context)


@csrf_exempt
def success(request):
    order = Order.objects.last()
    billing_info = order.billing_set.first()
    products = [
        {
            'product_name': item.product.product_name,
            'quantity': item.quantity,
            'amount': item.amount
        }
        for item in order.order_details_set.all()
    ]
    
    # Generate the invoice PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.fontName = 'Helvetica-Bold'
    title_style.fontSize = 24
    normal_style = styles['Normal']
    normal_style.fontSize = 12

    elements.append(Paragraph("INVOICE", title_style))
    elements.append(Spacer(1, 24))

    elements.append(Paragraph(f"Invoice Number: {order.id}", normal_style))
    elements.append(Paragraph(f"Date of Issue: {order.date.strftime('%Y-%m-%d')}", normal_style))
    elements.append(Spacer(1, 12))

    data = [
        ["PRODUCT NAME", "QUANTITY", "PRICE", "TOTAL"],
    ]
    total_price = 0
    for detail in order.order_details_set.all():
        price = float(detail.product.price)
        quantity = int(detail.quantity)
        total_item_price = price * quantity
        total_price += total_item_price
        data.append([
            detail.product.product_name,
            str(quantity),
            f"{price:.2f}",
            f"{total_item_price:.2f}"
        ])

    table = Table(data, colWidths=[3.5*inch, 1*inch, 1*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4B0D61')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONT', (0, 1), (-1, -1), 'Helvetica'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f2f2f2')),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))

    subtotal_data = [
        ["", "SUBTOTAL", f"{total_price:.2f}"]
    ]
    subtotal_table = Table(subtotal_data, colWidths=[5.5*inch, 1*inch, 1*inch])
    subtotal_table.setStyle(TableStyle([
        ('BACKGROUND', (1, 0), (2, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold'),
    ]))
    elements.append(subtotal_table)

    total_due = total_price
    total_data = [
        ["", "TOTAL", f"{total_due:.2f}"]
    ]
    total_table = Table(total_data, colWidths=[5.5*inch, 1*inch, 1*inch])
    total_table.setStyle(TableStyle([
        ('BACKGROUND', (1, 0), (2, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (1, 0), (2, 0), colors.HexColor('#2E74B5')),
    ]))
    elements.append(total_table)

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    # Send email with invoice attachment
    email = EmailMessage(
        subject="Order Confirmation and Invoice",
        body=f"Dear {billing_info.firstname} {billing_info.lastname},\n\nThank you for your order. Please find your invoice attached.",
        from_email="your-email@example.com",
        to=[billing_info.email],
    )
    email.attach(f"invoice_{order.id}.pdf", pdf, "application/pdf")
    email.send()

    # Update order status if payment is PayPal
    if order.pay_method.lower() == 'paypal':
        id = order.id
        data = {'status': 'completed'}
        Order.objects.update_or_create(pk=id, defaults=data)

    return render(request, 'customer/success.html')
    

#Order Crud
def myorder(request):
    user_id = request.user.id
    subtotal = 0
    orders = Order.objects.filter(user_id=user_id)  # Use filter to get all orders for the user

    if orders.exists():
        order_details_list = []
        for order in orders:
            order_details = Order_details.objects.filter(order=order)
            order_total = 0
            for item in order_details:
                item.total_price = int(item.product.price) * int(item.quantity)
                order_total += item.total_price
            order_details_list.append({'order': order, 'order_details': order_details, 'order_total': order_total})
            subtotal += order_total
        
        context = {'orders': orders, 'order_details_list': order_details_list, 'subtotal': subtotal}
        context.update(common_category())
    else:
        context = {'error_message': 'No orders found for this user'}
        context.update(common_category())

    return render(request, 'customer/myorder.html', context)

#Invoice
def generate_invoice(request, order_id):
    order = Order.objects.get(id=order_id)
    
    order_details = Order_details.objects.filter(order=order)

    # Create the HttpResponse object with the appropriate PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'

    # Create the PDF object, using the response object as its "file."
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.fontName = 'Helvetica-Bold'
    title_style.fontSize = 24
    normal_style = styles['Normal']
    normal_style.fontSize = 12

    # Add the title
    elements.append(Paragraph("INVOICE", title_style))
    elements.append(Spacer(1, 24))

    # Add the invoice number, date of issue
    elements.append(Paragraph(f"Invoice Number: {order.id}", normal_style))
    elements.append(Paragraph(f"Date of Issue: {order.date.strftime('%Y-%m-%d')}", normal_style))
    elements.append(Spacer(1, 12))

    # Prepare table data
    data = [
        ["PRODUCT NAME", "QUANTITY", "PRICE", "TOTAL"],
    ]
    total_price = 0
    for idx, detail in enumerate(order_details, start=1):
        price = float(detail.product.price)
        quantity = int(detail.quantity)
        total_item_price = price * quantity
        total_price += total_item_price
        data.append([
            detail.product.product_name,
            str(quantity),
            f"{price:.2f}",
            f"{total_item_price:.2f}"
        ])

    # Create the table
    table = Table(data, colWidths=[3.5*inch, 1*inch, 1*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4B0D61')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONT', (0, 1), (-1, -1), 'Helvetica'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f2f2f2')),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))

    # Add Subtotal and Total
    subtotal_data = [
        ["", "SUBTOTAL", f"{total_price:.2f}"]
    ]
    subtotal_table = Table(subtotal_data, colWidths=[5.5*inch, 1*inch, 1*inch])
    subtotal_table.setStyle(TableStyle([
        ('BACKGROUND', (1, 0), (2, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold'),
    ]))
    elements.append(subtotal_table)

    total_due = total_price  # Adjust for any discount if necessary
    total_data = [
        ["", "TOTAL", f"{total_due:.2f}"]
    ]
    total_table = Table(total_data, colWidths=[5.5*inch, 1*inch, 1*inch])
    total_table.setStyle(TableStyle([
        ('BACKGROUND', (1, 0), (2, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (1, 0), (2, 0), colors.HexColor('#2E74B5')),
    ]))
    elements.append(total_table)

    # Build the PDF
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    # Save PDF to a temporary file
    with open(f"static/images/upload{order.id}.pdf", "wb") as f:
        f.write(pdf)

    billing = Billing.objects.get(order_id=order)
    # Send email with PDF attached
    subject = f"Invoice #{order.id}"
    message = "Please find attached your invoice."
    from_email = {order.user.email}
    recipient_list = {billing.email}  # Assuming Order model has a customer with an email field
    email = EmailMessage(subject, message, from_email, recipient_list)
    email.attach(f"invoice_{order.id}.pdf", pdf, "order/pdf")
    email.send()

    # Write PDF to response for immediate download
    response.write(pdf)

    redirect('/customer/myorder')
    return response