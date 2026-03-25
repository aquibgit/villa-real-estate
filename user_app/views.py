from django.shortcuts import render,redirect, get_object_or_404
from builder_app.models import property_details
from villa.models import user_details
from user_app.models import booking,wishlistss
from villa.views import home,dashboardindex
from admin_app.views import scheduledvisit
import json
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

# Create your views here.
def userhome(request):
    bdata=property_details.objects.all()
    return render(request,'userindex.html',{'builder_properties':bdata})

def viewprop(request):
    pdata = property_details.objects.all()
    wishlist_items = []
    if 'uid' in request.session:
        user_id = request.session['uid']
        wishlist_items = list(
            wishlistss.objects.filter(user_id=user_id).values_list('property_name', flat=True)
        )
    return render(request, 'myprop.html', {
        'builder_properties': pdata,
        'wishlist_items': wishlist_items
    })

def wishlist(request, id):
    user_id = request.session['uid']
    pdata = property_details.objects.get(pk=id)
    existing = wishlistss.objects.filter(user_id=user_id, property_name=pdata.property_name).first()

    if existing:
        existing.delete()
    else:
        wishlistss.objects.create(
            user_id=user_id,
            property_photo=pdata.property_photo,
            property_category=pdata.property_category,
            property_name=pdata.property_name,
            property_location=pdata.property_location,
            property_budget=pdata.property_budget,
            property_bedroom=pdata.property_bedroom,
            property_bathroom=pdata.property_bathroom,
            property_area=pdata.property_area,
            property_floor=pdata.property_floor,
            property_parking=pdata.property_parking
        )
    return redirect('viewprop')




def schedulevisit(request,id):
    user_id=request.session['uid']
    udata=user_details.objects.get(pk=user_id)
    pdata=property_details.objects.get(pk=id)
    bdata=booking(
        user_id=user_id,
        name=udata.name,
        email=udata.email,
        phone=udata.phone,
        property_name=pdata.property_name,
        property_location=pdata.property_location,
        property_budget=pdata.property_budget
    )
    bdata.save()
    return redirect(userhome)

def Delete_booking(request,id):
    builder_data = booking.objects.get(pk=id)
    builder_data.delete()
    return redirect(scheduledvisit)

def edit_booking(request,id):
    editb=booking.objects.get(pk=id)
    return render(request,'editbook.html',{'prop':editb})

def edit_bookings(request,id):
    user_id=request.session['uid']
    pdata=booking.objects.get(pk=id)
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        property_name=request.POST.get('property_name')
        property_location=request.POST.get('property_location')
        property_budget=request.POST.get('property_budget')
        #store in database
        book_det=booking(id=id,user_id=user_id,name=name,email=email,phone=phone,property_name=property_name,property_location=property_location,property_budget=property_budget)
        #save data to database
        book_det.save()
    return redirect(scheduledvisit)

