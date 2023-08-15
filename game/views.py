from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from .forms import *
from .models import *
import random

def paymentCalc(principal,intrest,number_of_periods):
    principal = principal
    intrest = intrest
    monthly_intrest = intrest/float(12)
    number_of_periods = number_of_periods
    payment = (monthly_intrest*principal)/(float(1)-((float(1)+monthly_intrest)**-number_of_periods))
    return payment

# Create your views here.
@login_required
def home(request):
    user = request.user
    scenerios = Scenerio.objects.all()
    businesses = Business.objects.filter(user=user)
    current = True
    cc = businesses.count()

    for b in businesses:
        if b.user == user:
            current = True
        else: 
            current = False

    return render(request,'game/home.html', {
        'scenerios':scenerios,
        'businesses': businesses,
        'current': current,
        'user': user,
        'cc': cc,
    })

@login_required
def scenerio_maker(request, pk):
    user = request.user
    scenerio = get_object_or_404(Scenerio, id=pk) 
    foodtrucks = FoodTruck.objects.filter(scenerio=scenerio, master=True)
    employees = Employee.objects.filter(scenerio=scenerio, master=True)
    ingredients = Ingredient.objects.filter(scenerio=scenerio, master=True)
    market_segments = MarketSegment.objects.filter(scenerio=scenerio, master=True)
    loans = Loan.objects.filter(scenerio=scenerio, master=True)
    rounds = RoundNew.objects.filter(scenerio=scenerio)

    totalpop = 0
    for i in market_segments:
        totalpop += i.population

    return render(request,'game/scenerio_maker.html', {
        'scenerio': scenerio,
        'foodtrucks':foodtrucks,
        'employees':employees,
        'ingredients':ingredients,
        'market_segments': market_segments,
        'total_pop': totalpop,
        'rounds': rounds,
        'loans':loans,
    })

@login_required
def player_dashboard(request, pk):
    user = request.user
    business = get_object_or_404(Business, id=pk)
    scenerio = business.scenerio
    marketing_campaigns = MarketingCampaign.objects.filter(owner=business)
    online_marketing_campaigns = MarketingCampaign.objects.filter(owner=business, marketing_type = "Online")
    print_marketing_campaigns = MarketingCampaign.objects.filter(owner=business, marketing_type = "Print")
    word_of_mouth_marketing_campaigns = MarketingCampaign.objects.filter(owner=business, marketing_type = "Word of Mouth")
    ingredients = Ingredient.objects.filter(owner=business, master=False)
    trucks = FoodTruck.objects.filter(owner=business, master=False)
    loans = Loan.objects.filter(owner=business, master=False)
    employees = Employee.objects.filter(owner=business, master=False)
    rounds = RoundNew.objects.filter(business=business).order_by("number")
    demographics = MarketSegment.objects.filter(scenerio=scenerio)
    current_round = rounds.last()

    ingredient_count = ingredients.count()
    rounds_count = rounds.count()

    auth=False
    if business.user == user:
        auth = True


    #Marketing Updates
    business.onlineMarketing = online_marketing_campaigns.count()*.10
    business.printMarketing = print_marketing_campaigns.count()*.10
    business.wordOfMouthMarketing = word_of_mouth_marketing_campaigns.count()*.10

    marketing_spend = marketing_campaigns.count()*250

    #Capacity Updates
    employee_capacity = 750
    for employee in employees:
        employee_capacity = employee_capacity + employee.capacityBonus

    ft_capacity = 0 
    for ft in trucks:
        ft_capacity = ft_capacity + ft.capacityBonus

    if employee_capacity < ft_capacity:
        business.capacity = employee_capacity
    else: business.capacity = ft_capacity

    #Quality Bonuses
    i_quality = 0
    for i in ingredients:
        i_quality = i_quality + i.qualityBonus 
    
    e_quality = 0
    for e in employees:
        e_quality = e_quality + e.qualityBonus 

    t_quality = 0
    for t in trucks:
        t_quality = t_quality + t.qualityBonus

        
    business.quality = 0
    business.quality = business.quality + i_quality + e_quality + t_quality
    business.save()

    #Meal Cost
    meal_cost = 0
    meal_capacity = 0
    if ingredients.count() > 0:
        for i in ingredients:
            meal_cost = meal_cost + i.price
            meal_capacity = meal_capacity + i.capacityCost
        else: meal_capacity = 0


    gm_per_meal = business.price - meal_cost

    ft_meals = 0 
    e_meals = 0
    if trucks.count() == 0:
        ft_meals = 0 
    #else: ft_meals = ft_capacity / meal_capacity 

    #if employees.count() > 0:
       # e_meals = employee_capacity / meal_capacity
    #else: e_meals = 0 


    #Salaries
    salaries = 0
    comission = 0
    for e in employees:
        salaries = salaries + e.salary
        comission = comission + e.comission

    #MarketShare Test
    market_share = dict()
    for d in demographics:
        market_share[d.name] = (d.priceSensitivity * business.priceStrat) + (d.qualitySensitivity*business.quality) + (d.onlineMarketingSensitivity * business.onlineMarketing) + (d.printMarketingSensitivity * business.printMarketing) + (d.wordOfMouthMarketingSensitivity * business.wordOfMouthMarketing)

    food_type_turnout = dict()
    for d in demographics:
        if business.foodType == "Comfort Food":
            food_type_turnout[d.name] = (d.comfortFoodPreference * d.population)
        elif business.foodType == "Italian":
            food_type_turnout[d.name] = (d.italianFoodPreference * d.population)
        elif business.foodType == "Asian":
            food_type_turnout[d.name] = (d.asianFoodPreference * d.population)
        elif business.foodType == "Dessert":
            food_type_turnout[d.name] = (d.dessertPreference * d.population)
        elif business.foodType == "Smoothie":
            food_type_turnout[d.name] = (d.smoothieFoodPreference * d.population)

    ms_quantity_sold = dict()
    for d in demographics:
        if business.foodType == "Comfort Food":
            ms_quantity_sold[d.name] = (d.comfortFoodPreference * d.population) * ((d.priceSensitivity * business.priceStrat) + (d.qualitySensitivity*business.quality) + (d.onlineMarketingSensitivity * business.onlineMarketing) + (d.printMarketingSensitivity * business.printMarketing) + (d.wordOfMouthMarketingSensitivity * business.wordOfMouthMarketing))
        elif business.foodType == "Italian":
            ms_quantity_sold[d.name] = (d.italianFoodPreference * d.population) * ((d.priceSensitivity * business.priceStrat) + (d.qualitySensitivity*business.quality) + (d.onlineMarketingSensitivity * business.onlineMarketing) + (d.printMarketingSensitivity * business.printMarketing) + (d.wordOfMouthMarketingSensitivity * business.wordOfMouthMarketing))
        elif business.foodType == "Asian":
            ms_quantity_sold[d.name] = (d.asianFoodPreference * d.population) * ((d.priceSensitivity * business.priceStrat) + (d.qualitySensitivity*business.quality) + (d.onlineMarketingSensitivity * business.onlineMarketing) + (d.printMarketingSensitivity * business.printMarketing) + (d.wordOfMouthMarketingSensitivity * business.wordOfMouthMarketing))
        elif business.foodType == "Dessert":
            ms_quantity_sold[d.name] = (d.dessertPreference * d.population) * ((d.priceSensitivity * business.priceStrat) + (d.qualitySensitivity*business.quality) + (d.onlineMarketingSensitivity * business.onlineMarketing) + (d.printMarketingSensitivity * business.printMarketing) + (d.wordOfMouthMarketingSensitivity * business.wordOfMouthMarketing))
        elif business.foodType == "Smoothie":
            ms_quantity_sold[d.name] = (d.smoothieFoodPreference * d.population) * ((d.priceSensitivity * business.priceStrat) + (d.qualitySensitivity*business.quality) + (d.onlineMarketingSensitivity * business.onlineMarketing) + (d.printMarketingSensitivity * business.printMarketing) + (d.wordOfMouthMarketingSensitivity * business.wordOfMouthMarketing))
        
    total_sales = 0
    values = ms_quantity_sold.values()
    for v in values: 
        total_sales = total_sales + v

    total_sales = round(total_sales)





    return render(request,'game/player_dashboard.html', {
        'business':business,
        'scenerio':scenerio,
        'ingredients': ingredients,
        'marketing_campaigns':marketing_campaigns,
        'marketing_spend':marketing_spend,
        "ingredient_count": ingredient_count,
        'trucks':trucks,
        'employees':employees,
        'employee_capacity': employee_capacity,
        'ft_capacity': ft_capacity,
        'meal_cost': meal_cost,
        'gm_per_meal': gm_per_meal,
        'meal_capacity': meal_capacity,
        'ft_meals': ft_meals,
        'e_meals': e_meals,
        'salaries': salaries,
        'comission':comission,
        'rounds':rounds,
        'market_share': market_share,
        'food_type_turnout':food_type_turnout,
        'ms_quantity_sold': ms_quantity_sold,
        'total_sales': total_sales,
        'current_round':current_round,
        'rounds_count': rounds_count,
        'loans':loans,
        'auth':auth,
    })

@login_required
def shop(request, pk):
    user = request.user
    business = get_object_or_404(Business, id=pk)
    available_ingredients = Ingredient.objects.filter(scenerio=business.scenerio, master=True).order_by("price")
    current_ingredients = Ingredient.objects.filter(owner=business, master=False)

    i_count = current_ingredients.count()

    current_cost = 0
    current_qs = 0

    for i in current_ingredients:
        current_cost = current_cost + i.price
        current_qs = current_qs + i.qualityBonus

    return render(request,'game/shop.html', {
        'business':business,
        'available_ingredients':available_ingredients,
        'current_ingredients':current_ingredients,
        'i_count':i_count,
        'current_cost': current_cost,
        'current_qs': current_qs,
    })

@login_required
def market_research(request, pk):
    user = request.user
    business = get_object_or_404(Business, id=pk)
    market_segments = MarketSegment.objects.filter(scenerio=business.scenerio)

    return render(request,'game/market_research.html', {
        'business':business,
        'market_segments':market_segments,
    })

@login_required
def purchase(request, pk):
    user = request.user
    business = get_object_or_404(Business, id=pk)
    available_ingredients = Ingredient.objects.filter(scenerio=business.scenerio)

    return render(request,'game/shop.html', {
        'business':business,
        'available_ingredients':available_ingredients,
    })

@login_required
def new_business(request,pk):
    user = request.user
    scenerio = get_object_or_404(Scenerio, id=pk)
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.scenerio = scenerio
            instance.user = user
            instance.save()
            form.save()
            return HttpResponseRedirect(reverse('market_research', kwargs={'pk':instance.id}))
    else:
        form = BusinessForm()
    return render(request, 'game/business_form.html', {'form': form})

@login_required
def new_scenerio(request):
    user = request.user
    if request.method == 'POST':
        form = ScenerioForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.gm = user
            instance.save()
            form.save()
            return HttpResponseRedirect(reverse('game-home'))
    else:
        form = ScenerioForm()
    return render(request, 'game/scenerio_form.html', {'form': form})

@login_required
def new_food_truck(request,pk):
    scenerio = get_object_or_404(Scenerio, id=pk) 
    if request.method == 'POST':
        form = FoodTruckForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.scenerio = scenerio
            instance.save()
            form.save()
            return HttpResponseRedirect(reverse('scenerio_maker', kwargs={'pk':scenerio.id}))
    else:
        form = FoodTruckForm()
    return render(request, 'game/food_truck_form.html', {'form': form})

@login_required
def new_loan(request,pk):
    scenerio = get_object_or_404(Scenerio, id=pk) 
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.scenerio = scenerio
            instance.save()
            form.save()
            return HttpResponseRedirect(reverse('scenerio_maker', kwargs={'pk':scenerio.id}))
    else:
        form = LoanForm()
    return render(request, 'game/loan_form.html', {'form': form})

@login_required
def new_employee(request,pk):
    scenerio = get_object_or_404(Scenerio, id=pk) 
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.scenerio = scenerio
            instance.save()
            form.save()
            return HttpResponseRedirect(reverse('scenerio_maker', kwargs={'pk':scenerio.id}))
    else:
        form = EmployeeForm()
    return render(request, 'game/food_truck_form.html', {'form': form})

@login_required
def new_ingredient(request,pk):
    scenerio = get_object_or_404(Scenerio, id=pk) 
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.scenerio = scenerio
            instance.save()
            form.save()
            return HttpResponseRedirect(reverse('scenerio_maker', kwargs={'pk':scenerio.id}))
    else:
        form = IngredientForm()
    return render(request, 'game/ingredient_form.html', {'form': form})

@login_required
def new_market_segment(request,pk):
    scenerio = get_object_or_404(Scenerio, id=pk) 
    if request.method == 'POST':
        form = MarketSegmentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.scenerio = scenerio
            instance.save()
            form.save()
            return HttpResponseRedirect(reverse('scenerio_maker', kwargs={'pk':scenerio.id}))
    else:
        form = MarketSegmentForm()
    return render(request, 'game/market_segment_form.html', {'form': form})

@login_required
def new_round(request,pk):
    scenerio = get_object_or_404(Scenerio, id=pk) 
    if request.method == 'POST':
        form = RoundForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.scenerio = scenerio
            instance.save()
            form.save()
            return HttpResponseRedirect(reverse('scenerio_maker', kwargs={'pk':scenerio.id}))
    else:
        form = RoundForm()
    return render(request, 'game/round_form.html', {'form': form})

@login_required
def edit_identity(request,pk):
    business = get_object_or_404(Business, id=pk) 

    if request.method == 'GET':
        context = {'form': BusinessIdentityForm(instance=business), 'id': pk}
        return render(request,'game/business_form.html',context)
    else:
        form = BusinessIdentityForm(request.POST, instance=business)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('shop', kwargs={'pk':business.id}))

@login_required      
def increase_price(request,pk):
    if request.method == 'POST':
        business = get_object_or_404(Business, id=pk)
        business.price = business.price + 1
        business.priceStrat = business.priceStrat - .10
        business.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def decrease_price(request,pk):
    if request.method == 'POST':
        business = get_object_or_404(Business, id=pk)
        business.price = business.price - 1
        business.priceStrat = business.priceStrat + .10

        business.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def new_marketing_campaign(request,pk):
    business = get_object_or_404(Business, id=pk)
    scenerio = business.scenerio

    if request.method == 'POST':
        form = MarketingCampaignForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = business
            instance.save()
            form.save()
            return HttpResponseRedirect(reverse('player_dashboard', kwargs={'pk':business.id}))
    else:
        form = MarketingCampaignForm()
    return render(request, 'game/marketing_campaign_form.html', {'form': form})

@login_required
def purhcase_ingredient(request,pk):
    user = request.user
    ingredient = get_object_or_404(Ingredient, id=pk)
    scenerio = ingredient.scenerio
    business = get_object_or_404(Business, user=user)

    if request.method == 'POST':
        form = PurchaseIngredientForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = business
            instance.scenerio = scenerio
            instance.name = ingredient.name
            instance.description = ingredient.description
            instance.qualityBonus = ingredient.qualityBonus
            instance.capacityCost = ingredient.capacityCost
            instance.price = ingredient.price
            instance.master = False
            instance.save()
            form.save()

            risk = 1
            if ingredient.price > 2 or ingredient.price < 1: 
                risk = 2

            log = LogEntry(business=business, round =business.current_round, message = f"{business} chose {ingredient.name}", risk=risk )
            log.save()
            return HttpResponseRedirect(reverse('shop', kwargs={'pk':business.id}))
    else:
        form = PurchaseIngredientForm()
    return render(request, 'game/confirm.html', {'form': form})

@login_required
def delete_ingredient(request, pk):
    ingredient = Ingredient.objects.get(id=pk)
    ingredient.delete()

    return HttpResponseRedirect(reverse('shop', kwargs={"pk":ingredient.owner.id}))

@login_required
def delete_business(request, pk):
    game = Business.objects.get(id=pk)
    game.delete()

    return HttpResponseRedirect(reverse('game-home'))

@login_required
def carlot(request, pk):
    user = request.user
    business = get_object_or_404(Business, id=pk)
    available_trucks = FoodTruck.objects.filter(scenerio=business.scenerio, master=True)

    return render(request,'game/carlot.html', {
        'business':business,
        'available_trucks':available_trucks,
    })

@login_required
def purhcase_truck(request,pk):
    user = request.user
    truck = get_object_or_404(FoodTruck, id=pk)
    scenerio = truck.scenerio
    business = get_object_or_404(Business, user=user)

    if request.method == 'POST':
        form = PurchaseTruckForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = business
            instance.scenerio = scenerio
            instance.name = truck.name
            instance.price = truck.price
            instance.description = truck.description
            instance.qualityBonus = truck.qualityBonus
            instance.capacityBonus = truck.capacityBonus
            instance.master = False
            instance.save()
            form.save()

            business.cashBalance = business.cashBalance - instance.price
            business.save()

            risk = 1
            if truck.price >=10000:
                risk = 2
            if truck.price >=20000:
                risk = 3

            log = LogEntry(business=business, round =business.current_round, message = f"{business} bought {truck.name} Food Truck.", risk=risk )
            log.save()

            return HttpResponseRedirect(reverse('player_dashboard', kwargs={'pk':business.id}))
    else:
        form = PurchaseTruckForm()
    return render(request, 'game/confirm.html', {'form': form})

@login_required
def bank(request, pk):
    user = request.user
    business = get_object_or_404(Business, id=pk)
    available_loans = Loan.objects.filter(scenerio=business.scenerio, master=True)
    business = get_object_or_404(Business, user=user)
    trucks = FoodTruck.objects.filter(owner=business, master=False)
    loans = Loan.objects.filter(owner=business, master=False)

    ft_balance = 0
    for i in trucks:
        ft_balance += i.price

    liabilites = 0
    for i in loans:
        liabilites += i.total_value

    assets = business.cashBalance + ft_balance

    business_value = float(assets) - float(liabilites)

    debt_to_equity = liabilites/business_value

    for i in available_loans: 
        i.payment = paymentCalc(i.amount,i.intrest,i.how_many_months)
        i.total_value = i.payment * i.how_many_months
        i.save()

    return render(request,'game/bank.html', {
        'business':business,
        'available_loans':available_loans,
        'business_value': business_value,
        'debt_to_equity': debt_to_equity,
    })

@login_required
def vc(request, pk):
    user = request.user
    business = get_object_or_404(Business, user=user)
    trucks = FoodTruck.objects.filter(owner=business, master=False)
    loans = Loan.objects.filter(owner=business, master=False)

    ft_balance = 0
    for i in trucks:
        ft_balance += i.price

    liabilites = 0
    for i in loans:
        liabilites += i.total_value

    assets = business.cashBalance + ft_balance

    business_value = float(assets) - float(liabilites)

    debt_to_equity = liabilites/business_value

    business_value_after_vc = business_value - ((float(business.vcOwnership))*business_value)

    offer = business_value_after_vc * .02

    return render(request,'game/vc.html', {
        'business':business,
        'business_value': business_value,
        'debt_to_equity':debt_to_equity,
        'assets':assets,
        'liabilites':liabilites,
        'business_value_after_vc': business_value_after_vc,
        'offer':offer,
    })

@login_required
def vc_trade(request,pk):
    if request.method == 'POST':
        business = get_object_or_404(Business, id=pk)

        trucks = FoodTruck.objects.filter(owner=business, master=False)
        loans = Loan.objects.filter(owner=business, master=False)

        ft_balance = 0
        for i in trucks:
            ft_balance += i.price

        liabilites = 0
        for i in loans:
            liabilites += i.total_value

        assets = business.cashBalance + ft_balance

        business_value = float(assets) - float(liabilites)

        debt_to_equity = liabilites/business_value

        business_value_after_vc = business_value - ((float(business.vcOwnership))*business_value)

        offer = business_value_after_vc * .02

        business.vcOwnership = business.vcOwnership + .02
        business.cashBalance = business.cashBalance + offer
        business.save()

        risk = 1
        log = LogEntry(business=business, round =business.current_round, message = f"{business} made a deal with a VC.", risk=risk )
        log.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def take_loan(request,pk):
    user = request.user
    loan = get_object_or_404(Loan, id=pk)
    scenerio = loan.scenerio
    business = get_object_or_404(Business, user=user, scenerio=scenerio)

    if request.method == 'POST':
        form = TakeLoanForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = business
            instance.bank_name = loan.bank_name
            instance.scenerio = scenerio
            instance.amount = loan.amount
            instance.intrest = loan.intrest
            instance.payment = loan.payment
            instance.total_value = loan.total_value
            instance.master = False
            instance.save()
            form.save()

            business.cashBalance = business.cashBalance + instance.amount
            business.save()

            risk = 1
            if loan.amount > 10000:
                risk = 2


            log = LogEntry(business=business, round =business.current_round, message = f"{business} took out a loan for {loan.amount}", risk=risk )
            log.save()

            return HttpResponseRedirect(reverse('player_dashboard', kwargs={'pk':business.id}))
    else:
        form = TakeLoanForm()
    return render(request, 'game/confirm.html', {'form': form})

@login_required
def staffing(request, pk):
    user = request.user
    business = get_object_or_404(Business, id=pk)
    available_employees = Employee.objects.filter(scenerio=business.scenerio, master=True)

    return render(request,'game/staffing.html', {
        'business':business,
        'available_employees':available_employees,
    })

@login_required
def hire_employee(request,pk):
    user = request.user
    employee = get_object_or_404(Employee, id=pk)
    scenerio = employee.scenerio
    business = get_object_or_404(Business, user=user)

    if request.method == 'POST':
        form = HireForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = business
            instance.name = employee.name
            instance.scenerio = scenerio
            instance.description = employee.description
            instance.qualityBonus = employee.qualityBonus
            instance.capacityBonus = employee.capacityBonus
            instance.salary = employee.salary
            instance.comission = employee.comission
            instance.master = False
            instance.save()
            form.save()

            risk = 1
            if employee.salary > 1000:
                risk =2

            log = LogEntry(business=business, round =business.current_round, message = f"{business} hired {employee.name}", risk=risk )
            log.save()

            return HttpResponseRedirect(reverse('player_dashboard', kwargs={'pk':business.id}))
    else:
        form = HireForm()
    return render(request, 'game/confirm.html', {'form': form})

@login_required
def delete_truck(request, pk):
    ft = FoodTruck.objects.get(id=pk)
    ft.delete()

    company = ft.owner
    company.cashBalance = company.cashBalance + ft.price
    company.save()

    return HttpResponseRedirect(reverse('player_dashboard', kwargs={"pk":ft.owner.id}))

@login_required
def delete_employee(request, pk):
    e = Employee.objects.get(id=pk)
    e.delete()

    return HttpResponseRedirect(reverse('player_dashboard', kwargs={"pk":e.owner.id}))

@login_required
def delete_marketing(request, pk):
    mkt = MarketingCampaign.objects.get(id=pk)
    mkt.delete()

    return HttpResponseRedirect(reverse('player_dashboard', kwargs={"pk":mkt.owner.id}))

@login_required
def payoff_loan(request, pk):
    loan = Loan.objects.get(id=pk)
    business = get_object_or_404(Business, user=request.user)

    if loan.amount < loan.total_value:
        business.cashBalance -= loan.amount
    else:
        business.cashBalance = business.cashBalance - loan.total_value
        
    business.save()
    loan.delete()


    return HttpResponseRedirect(reverse('player_dashboard', kwargs={"pk":business.id}))

@login_required
def next_round(request,pk):
    business = get_object_or_404(Business, id=pk)
    scenerio = business.scenerio
    rounds = RoundNew.objects.filter(business=business)
    ingredients = Ingredient.objects.filter(owner=business, master=False)
    trucks = FoodTruck.objects.filter(owner=business, master=False)
    employees = Employee.objects.filter(owner=business, master=False)
    marketing_campaigns = MarketingCampaign.objects.filter(owner=business)
    demographics = MarketSegment.objects.filter(scenerio=scenerio)
    business_type = business.foodType
    loans = Loan.objects.filter(owner=business, master=False)

    round_number = rounds.count()+1

    business.current_round = round_number
    business.save()

    meal_cost = 0
    for i in ingredients:
            meal_cost = meal_cost + i.price

    salaries = 0
    comissions = 0
    for e in employees:
        salaries = salaries + e.salary
        comissions = comissions + e.comission

    loan_payments = 0
    for l in loans:
        loan_payments = loan_payments + l.payment
        l.total_value = l.total_value - l.payment
        l.save()

    #demographic turnout
    turnout = dict()
    for d in demographics:
        turnout[d.name] = d.population * d.weatherSensitivity

    market_share = dict()
    for d in demographics:
        market_share[d.name] = (d.priceSensitivity * business.priceStrat) + (d.qualitySensitivity*business.quality) + (d.onlineMarketingSensitivity * business.onlineMarketing) + (d.printMarketingSensitivity * business.printMarketing) + (d.wordOfMouthMarketingSensitivity * business.wordOfMouthMarketing)

    #Weather
    weather = random.randrange(50,100)/100
    
    ms_quantity_sold = dict()
    for d in demographics:
        if business.foodType == "Comfort Food":
            ms_quantity_sold[d.name] = (d.comfortFoodPreference * (d.population*d.weatherSensitivity*weather)) * ((d.priceSensitivity * business.priceStrat) + (d.qualitySensitivity*business.quality) + (d.onlineMarketingSensitivity * business.onlineMarketing) + (d.printMarketingSensitivity * business.printMarketing) + (d.wordOfMouthMarketingSensitivity * business.wordOfMouthMarketing))
        elif business.foodType == "Italian":
            ms_quantity_sold[d.name] = (d.italianFoodPreference * (d.population*d.weatherSensitivity*weather)) * ((d.priceSensitivity * business.priceStrat) + (d.qualitySensitivity*business.quality) + (d.onlineMarketingSensitivity * business.onlineMarketing) + (d.printMarketingSensitivity * business.printMarketing) + (d.wordOfMouthMarketingSensitivity * business.wordOfMouthMarketing))
        elif business.foodType == "Asian":
            ms_quantity_sold[d.name] = (d.asianFoodPreference * (d.population*d.weatherSensitivity*weather)) * ((d.priceSensitivity * business.priceStrat) + (d.qualitySensitivity*business.quality) + (d.onlineMarketingSensitivity * business.onlineMarketing) + (d.printMarketingSensitivity * business.printMarketing) + (d.wordOfMouthMarketingSensitivity * business.wordOfMouthMarketing))
        elif business.foodType == "Dessert":
            ms_quantity_sold[d.name] = (d.dessertPreference * (d.population*d.weatherSensitivity*weather)) * ((d.priceSensitivity * business.priceStrat) + (d.qualitySensitivity*business.quality) + (d.onlineMarketingSensitivity * business.onlineMarketing) + (d.printMarketingSensitivity * business.printMarketing) + (d.wordOfMouthMarketingSensitivity * business.wordOfMouthMarketing))
        elif business.foodType == "Smoothie":
            ms_quantity_sold[d.name] = (d.smoothieFoodPreference * (d.population*d.weatherSensitivity*weather)) * ((d.priceSensitivity * business.priceStrat) + (d.qualitySensitivity*business.quality) + (d.onlineMarketingSensitivity * business.onlineMarketing) + (d.printMarketingSensitivity * business.printMarketing) + (d.wordOfMouthMarketingSensitivity * business.wordOfMouthMarketing))
        
    total_sales = 0
    values = ms_quantity_sold.values()
    for v in values: 
        total_sales = total_sales + v

    if total_sales <= 0:
        total_sales = 0
    elif total_sales > business.capacity:
        total_sales = business.capacity
    else: 
        total_sales = total_sales

    total_quantity_sold = round(total_sales)
    round_count = rounds.count()
    revenue = total_quantity_sold * business.price  
    comission_cost = revenue * comissions  
    marketing_spend = marketing_campaigns.count()*250
    ingredient_cost = meal_cost * total_quantity_sold
    total_varriable_cost = ingredient_cost + comission_cost
    gm = revenue - total_varriable_cost
    event_payments = 250
    loan_payments = loan_payments
    total_fixed_cost = event_payments + loan_payments + salaries + marketing_spend
    net_income = revenue - total_varriable_cost - total_fixed_cost
    tax_expense = .20 * net_income
    profit = round(net_income -tax_expense)
    
    message = ""

    if round_number >= 10:
        message = message + "This is the last round! Click End Game to see your results. "

    if total_quantity_sold == business.capacity:
        message = message + "Dang! You sold out. You need to increase your capacity. Consider hiring staff or investing in another food truck. What's your bottle neck right now? What's stopping you from making more meals? "

    if profit > 0: 
        message = message + "Congrats! You made positive profits this month. Keep the trend going! "
    else: message = message + "Uh-Oh, looks like you were in the red this month. Take a look at your fixed and varriable costs. Can you increase your meal price? Can you lower your monthly expenses somehow? "

    message = message + f"It looks like you sold {total_quantity_sold} meals at ${business.price}, resulting in a net revenue of ${revenue}. After expenses, you brought in ${profit}. "



    #Ingredient Cost

    if request.method == 'POST':
        form = RoundForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.weather = weather
            instance.number = round_number
            instance.sales = total_quantity_sold
            instance.revenue = revenue
            instance.comission_cost = comission_cost
            instance.business = business
            instance.ingredient_cost = ingredient_cost
            instance.total_varriable_cost = total_varriable_cost
            instance.gm = gm
            instance.salaries = salaries
            instance.loan_payments = loan_payments
            instance.scenerio = scenerio
            instance.marketing_spend = marketing_spend
            instance.event_payments = event_payments
            instance.total_fixed_cost = total_fixed_cost
            instance.net_income = net_income
            instance.tax_expense = tax_expense
            instance.profit = profit
            instance.description = message

            business.cashBalance = business.cashBalance + profit
            business.save()

            instance.save()
            form.save()

            return HttpResponseRedirect(reverse('player_dashboard', kwargs={'pk':business.id}))
    else:
        form = RoundForm()
    return render(request, 'game/round_form.html', {'form': form})

@login_required
def new_report(request,pk):
    business = get_object_or_404(Business, id=pk)
    scenerio = business.scenerio
    rounds = RoundNew.objects.filter(business=business)
    ingredients = Ingredient.objects.filter(owner=business, master=False)
    trucks = FoodTruck.objects.filter(owner=business, master=False)
    employees = Employee.objects.filter(owner=business, master=False)
    marketing_campaigns = MarketingCampaign.objects.filter(owner=business)
    demographics = MarketSegment.objects.filter(scenerio=scenerio)
    business_type = business.foodType
    loans = Loan.objects.filter(owner=business, master=False)

    assets = business.cashBalance
    for t in trucks:
        assets = assets + t.price

    liabilities = 0
    for l in loans:
        liabilities = liabilities + l.total_value
    

    owners_equity = float(assets) - float(liabilities)

    vc_split = business.vcOwnership * owners_equity

    final_score = owners_equity - vc_split

    total_sales = 0
    total_revenue = 0
    total_ingredient_costs = 0
    total_comissions = 0
    total_varriable_costs = 0
    total_salaries = 0
    total_loan_payments = 0
    total_event_payments = 0
    total_marketing_spend = 0
    total_fixed_costs = 0
    total_net_income = 0
    total_tax_payments = 0
    total_profit = 0

    for i in rounds: 
        total_sales += i.sales
        total_revenue += i.revenue
        total_ingredient_costs += i.ingredient_cost
        total_comissions += i.comission_cost
        total_varriable_costs += i.total_varriable_cost
        total_salaries += i.salaries
        total_loan_payments += i.loan_payments
        total_event_payments += i.event_payments
        total_marketing_spend += i.marketing_spend
        total_fixed_costs += i.total_fixed_cost
        total_net_income += i.net_income
        total_tax_payments += i.tax_expense
        total_profit += i.profit

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.business = business
            instance.scenerio = scenerio
            instance.assets = assets
            instance.liabilities = liabilities
            instance.owners_equity = owners_equity
            instance.vc_cut = vc_split
            instance.final_score = final_score
            instance.total_sales = total_sales
            instance.total_revenue = total_revenue
            instance.total_ingredient_costs = total_ingredient_costs
            instance.total_comissions = total_comissions
            instance.total_varriable_costs = total_varriable_costs
            instance.total_salaries = total_salaries
            instance.total_loan_payments = total_loan_payments
            instance.total_event_payments = total_event_payments
            instance.total_marketing_spend = total_marketing_spend
            instance.total_fixed_costs = total_fixed_costs
            instance.total_net_income = total_net_income
            instance.total_tax_payments = total_tax_payments
            instance.total_profit = total_profit
            business.save()

            instance.save()
            form.save()

            return HttpResponseRedirect(reverse('the_end', kwargs={'pk':instance.id}))
    else:
        form = ReportForm()
    return render(request, 'game/report_form.html', {'form': form})

@login_required
def the_end(request, pk):
    user = request.user
    report = get_object_or_404(Report, id=pk)
    business = report.business
    scenerio = business.scenerio
    rounds = RoundNew.objects.filter(business=business)
    ingredients = Ingredient.objects.filter(owner=business, master=False)
    trucks = FoodTruck.objects.filter(owner=business, master=False)
    employees = Employee.objects.filter(owner=business, master=False)
    marketing_campaigns = MarketingCampaign.objects.filter(owner=business)
    demographics = MarketSegment.objects.filter(scenerio=scenerio)
    business_type = business.foodType
    loans = Loan.objects.filter(owner=business, master=False)
    logs = LogEntry.objects.filter(business=business)

    riskiness_score = 0
    for i in logs:
        riskiness_score += i.risk

    loan_amount = 0
    for i in loans:
        loan_amount = loan_amount + i.total_value

    return render(request,'game/the_end.html', {
        'business':business,
        'report':report,
        'trucks':trucks,
        'loans': loans,
        'loan_amount': loan_amount,
        'logs': logs,
        'riskiness_score':riskiness_score,
    })

@login_required
def scoreboard(request, pk):
    report = get_object_or_404(Report, id=pk)
    scenerio = report.scenerio
    reports = Report.objects.filter(scenerio=scenerio).order_by("-final_score")
    business = report.business
    

    return render(request,'game/leaderboard.html', {
        'business':business,
        'report':report,
        'scenerio':scenerio,
        'reports':reports,
    })

