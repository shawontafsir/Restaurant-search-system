from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

import restaurant
from register.models import Register
from restaurant.models import Restaurant, Menu, Review

def restaurants(request):
    try:
        restaurants = Restaurant.objects.all()
    except:
        Http404("Error")

    if request.POST.get('form_type')=='range_form':
        price_max = request.POST.get('price-max')
        price_min = request.POST.get('price-min')
        matched_restaurants = []
        for r in restaurants:
            price = r.costperfood
            price1, price2 = price.split("-")
            if int(price1)>=int(price_min) and int(price1)<=int(price_max) and r not in matched_restaurants:
                matched_restaurants.append(r)
            if int(price2)>=int(price_min) and int(price2)<=int(price_max) and r not in matched_restaurants:
                matched_restaurants.append(r)

        if request.session.get('username'):
            user = Register.objects.get(name=request.session.get('username'))
            return render(request, 'restaurant/search.html',
                          {'restaurants': matched_restaurants, 'is_valid': True, 'user': user})
        else:
            return render(request, 'restaurant/search.html',
                          {'restaurants': matched_restaurants, 'is_valid': False, 'user': None})

    if request.session.get('username'):
        user = Register.objects.get(name=request.session.get('username'))
        return render(request, 'restaurant/restaurants.html',{'restaurants': restaurants, 'is_valid': True, 'user': user})
    else:
        return render(request, 'restaurant/restaurants.html',{'restaurants': restaurants, 'is_valid': False, 'user': None})

def detail(request,res_name):
    try:
        restaurant = Restaurant.objects.get(name=res_name)
    except:
        Http404("Restaurant does not exist")

    if request.POST.get('form_type')=='rating_form':
        if request.session.get('username'):
            try:
                review = Review.objects.all()
            except:
                Http404("ERROR")
            f = 0
            t_comment = ""
            t_review = Review()
            for r in review:
                if r.username == request.session.get('username') and restaurant == r.restaurant:
                    f = 1
                    t_comment = r.review
                    t_review = r
                    break
            if f:
                t_review.delete()
                r = Review()
                r.restaurant = restaurant
                r.username = request.session.get('username')
                r.review = t_comment
                r.rating = request.POST.get('rating')
                r.save()
            else:
                re = Review()
                re.username = request.session.get('username')
                re.restaurant = restaurant
                re.review = ""
                r.rating = request.POST.get('rating')
                re.save()
        else:
            return HttpResponseRedirect("/register/login")
    if request.POST.get('form_type')=='comment_form':
        if request.session.get('username'):
            try:
                review = Review.objects.all()
            except:
                Http404("ERROR")
            f=0
            t_rate = "0"
            t_review = Review()
            for r in review:
                if r.username==request.session.get('username') and restaurant==r.restaurant:
                    f=1
                    t_rate = r.rating
                    t_review = r
                    break
            if f:
                t_review.delete()
                r = Review()
                r.restaurant = restaurant
                r.username = request.session.get('username')
                r.review = request.POST.get('comment')
                r.rating = t_rate
                r.save()
            else:
                r = Review()
                r.username = request.session.get('username')
                r.restaurant = restaurant
                r.review = request.POST.get('comment')
                r.rating = "0"
                r.save()
        else:
            return HttpResponseRedirect("/register/login")

    if request.session.get('username'):
        user = Register.objects.get(name=request.session.get('username'))
        review = Review.objects.all()
        t_rate = 0
        for r in review:
            if r.username == request.session.get('username') and restaurant == r.restaurant:
                t_rate = int(float(r.rating))
                break

        return render(request, 'restaurant/detail.html',{'restaurant': restaurant, 'is_valid': True, 'user': user, 'rate':t_rate})
    else:
        return render(request, 'restaurant/detail.html',{'restaurant': restaurant, 'is_valid': False, 'user': None, 'rate':None})

def search(request):
    query = request.GET.get("q")
    if query==None:
        return HttpResponseRedirect("/restaurant/")
    try:
        restaurants = Restaurant.objects.all()
    except:
        Http404("Restaurants or does not exist")

    matched_restaurants=[]
    for restaurant in restaurants:
        if query.lower() in restaurant.name.lower():
            matched_restaurants.append(restaurant)
        elif query.lower() in restaurant.cuisine.lower():
            matched_restaurants.append(restaurant)
        else:
            for m in restaurant.menu_set.all():
                if query.lower() in m.foodname.lower():
                    matched_restaurants.append(restaurant)
                    break

    if request.session.get('username'):
        user = Register.objects.get(name=request.session.get('username'))
        return render(request, 'restaurant/search.html',{'restaurants':matched_restaurants, 'is_valid': True, 'user': user})
    else:
        return render(request, 'restaurant/search.html', {'restaurants': matched_restaurants, 'is_valid': False, 'user': None})

def order(request):
    if request.session.get('username'):
        try:
            restaurants = Restaurant.objects.all()
            user = Register.objects.get(name=request.session.get('username'))
        except:
            Http404("Restaurant does not exist")

        if request.POST.get('form_type')=="select_form":
            s = request.POST.get('selected')
            if s:
                selected_restaurant = Restaurant.objects.get(name=s)
                request.session['selected_restaurant'] = s
                return render(request, 'restaurant/order.html',{'restaurants':restaurants,'ordered':request.session.get('ordered2'), 'selected_restaurant': selected_restaurant, 'is_valid': True, 'user': user})
            else:
                return render(request, 'restaurant/order.html',{'restaurants':restaurants,'ordered':request.session.get('ordered2'), 'is_valid': True, 'user': user})



        elif request.POST.get('form_type')=="order_form":
            s = request.POST.getlist('selected')
            if not 'ordered2' in request.session:
                request.session['ordered2'] = s
            else:
                saved_list = request.session['ordered2']
                for element in s:
                    if element not in saved_list:
                        saved_list.append(element)
                request.session['ordered2'] = saved_list
            selected_restaurant = Restaurant.objects.get(name=request.session.get('selected_restaurant'))
            return render(request, 'restaurant/order.html',{'restaurants':restaurants, 'selected_restaurant': selected_restaurant, 'ordered':request.session.get('ordered2'), 'is_valid': True, 'user': user})

        elif request.POST.get('form_type')=="confirm_form":
            confirmed = {}
            total = {}
            sum = 0
            for element in request.session['ordered2']:
                quantity = request.POST.get(element)
                if quantity and float(quantity)>0:
                    confirmed.update({element:quantity})
                    m = Menu.objects.get(id=element)
                    sum += float(m.price)*float(quantity)
                    total.update({m.foodname : (float(m.price)*float(quantity))})
            print(confirmed)
            print(total)
            request.session['confirmed'] = confirmed
            request.session['total'] = total
            request.session['sum'] = sum
            selected_restaurant = Restaurant.objects.get(name=request.session.get('selected_restaurant'))
            return render(request,'restaurant/order.html',{'restaurants':restaurants, 'selected_restaurant':selected_restaurant, 'confirmed':confirmed,'total':total,'sum':sum, 'is_valid':True, 'user':user})

        elif request.POST.get('form_type')=="confirm_again_form":
            if 'selected_restaurant' not in request.session:
                return HttpResponseRedirect("/restaurant/")

            confirmed = request.session.get('confirmed')
            total = request.session.get('total')
            sum = request.session.get('sum')

            file = open("order.txt","w")

            file.write("Your Ordered List:\n")
            file.write("Item              total Price\n")
            file.write("--------------------------------\n")
            for key,value in total.items():
                file.write(str(key)+"      "+str(value)+"\n")
            file.write("--------------------------------\n")
            file.write("Total Price:   "+str(sum)+"\n")

            file.close()

            try:
                del request.session['selected_restaurant']
                del request.session['confirmed']
                del request.session['total']
                del request.session['sum']
                del request.session['ordered2']
                del request.session['ordered']
                del request.session['ordered1']
            except:
                pass
            return HttpResponseRedirect("/restaurant/")

        else:
            return render(request, 'restaurant/order.html', {'restaurants':restaurants, 'ordered':request.session.get('ordered2'), 'is_valid': True, 'user': user})

    else:
        return HttpResponseRedirect("/register/login")
