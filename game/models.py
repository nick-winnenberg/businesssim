from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Scenerio(models.Model):
    name = models.CharField(max_length=200)
    gm = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gm")
    description = models.CharField(max_length=2000, default="description")
    max_rounds = models.IntegerField(default=10)
    

    def __str__(self):
        return self.name

class Business(models.Model):
    # Food Type Choices
    comfortFood = "Comfort Food"
    italian = "Italian"
    asian = "Asian"
    dessert = "Dessert"
    smoothie = "Smoothie"
    foodTypeChoices = [
        (comfortFood, 'Comfort Food'),
        (italian, 'Italian'),
        (asian, "Asian"),
        (dessert, 'Dessert'),
        (smoothie, 'Smoothie'),
    ]

    # Gender Options
    male = "Male"
    female = "Female"
    nonbinary = "Non-Binary"
    other = "Other"
    genderChoicesChoices = [
        (male, 'Male'),
        (female, 'Female'),
        (nonbinary, "Non-Binary"),
        (other, 'Other'),
    ]

    #Survey Information
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE,)
    firstAndLastName = models.CharField(max_length=200, verbose_name="First and Last Name?")
    gender = models.CharField(max_length=200, choices=genderChoicesChoices, default="Other")
    yearsProfessionalExperince = models.IntegerField(default=5, verbose_name="How many years of Professional Experince in your field?")
    yearsofBusinessEducationExperince = models.IntegerField(default=5, verbose_name="How many years of Formal Business Education?")
    jobTitle = models.CharField(max_length=200, verbose_name="Current Job Title?")
    industry = models.CharField(max_length=200, verbose_name="Current Industry?")
    summarize_your_strategy = models.CharField(max_length=2000, default="")

    #Food Truck Information
    foodTruckName = models.CharField(max_length=200)
    scenerio = models.ForeignKey(Scenerio, on_delete=models.CASCADE, related_name="food_truck_bus_scenerio")
    quality = models.FloatField(default=.10)
    capacity = models.IntegerField(default=100)
    price = models.IntegerField(default=10)
    priceStrat = models.FloatField(default=.50)
    onlineMarketing = models.FloatField(default=.10)
    printMarketing = models.FloatField(default=.10)
    wordOfMouthMarketing = models.FloatField(default=.10)
    foodType = models.CharField(max_length=200, choices=foodTypeChoices, default=comfortFood)
    mission = models.CharField(max_length=2000)
    vision = models.CharField(max_length=2000)
    values = models.CharField(max_length=2000)
    cashBalance = models.IntegerField(default=10000)
    vcOwnership = models.FloatField(default=.00)
    current_round = models.FloatField(default= 1, null=True)


    def __str__(self):
        return self.foodTruckName

    
class FoodTruck(models.Model):
    name = models.CharField(max_length=200)
    scenerio = models.ForeignKey(Scenerio, on_delete=models.CASCADE, related_name="food_truck_scenerio")
    price = models.DecimalField(default=10000, max_digits=100, decimal_places=2)
    description = models.CharField(max_length=2000)
    capacityBonus = models.IntegerField(default=1000)
    qualityBonus = models.FloatField(default=.03)
    master = models.BooleanField(default=True)
    owner = models.ForeignKey(Business, null=True, on_delete=models.CASCADE,)

    def __str__(self):
        return self.name
    
class Employee(models.Model):
    name = models.CharField(max_length=200)
    scenerio = models.ForeignKey(Scenerio, on_delete=models.CASCADE, related_name="employee_scenerio")
    description = models.CharField(max_length=2000)
    salary = models.IntegerField(default=10000)
    comission = models.FloatField(default=.03)
    capacityBonus = models.IntegerField(default=1000)
    qualityBonus = models.FloatField(default=.03)
    master = models.BooleanField(default=True)
    owner = models.ForeignKey(Business, null=True, on_delete=models.CASCADE,)

    def __str__(self):
        return self.name
    
class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    scenerio = models.ForeignKey(Scenerio, on_delete=models.CASCADE, related_name="ingredient_scenerio")
    description = models.CharField(max_length=2000)
    price = models.FloatField(default=1.50)
    qualityBonus = models.FloatField(default=.03)
    capacityCost = models.FloatField(default=.33)
    master = models.BooleanField(default=True)
    owner = models.ForeignKey(Business, null=True, on_delete=models.CASCADE,)

    def __str__(self):
        return self.name
    
class MarketSegment(models.Model):
    name = models.CharField(max_length=200)
    scenerio = models.ForeignKey(Scenerio, on_delete=models.CASCADE, related_name="market_segment_scenerio")
    population = models.IntegerField(default=10000)
    description = models.CharField(max_length=2000)
    priceSensitivity = models.FloatField(default=.10)
    qualitySensitivity = models.FloatField(default=.10)
    onlineMarketingSensitivity = models.FloatField(default=.10)
    printMarketingSensitivity = models.FloatField(default=.10)
    wordOfMouthMarketingSensitivity = models.FloatField(default=.10)
    weatherSensitivity = models.FloatField(default=.10)
    comfortFoodPreference = models.FloatField(default=.10)
    italianFoodPreference = models.FloatField(default=.10)
    asianFoodPreference = models.FloatField(default=.10)
    dessertPreference = models.FloatField(default=.10)
    smoothieFoodPreference = models.FloatField(default=.10)
    master = models.BooleanField(default=True)
    owner = models.ForeignKey(Business, null=True, on_delete=models.CASCADE,)

    def __str__(self):
        return self.name
    
class MarketingCampaign(models.Model):
    # Type Choices
    online = "Online"
    print = "Print"
    word_of_mouth = "Word of Mouth"
    typeChoices = [
        (online, 'Online'),
        (print, 'Print'),
        (word_of_mouth, "Word of Mouth"),
    ]
    
    name = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(Business, null=True, on_delete=models.CASCADE,)
    marketing_type = models.CharField(max_length=200, choices=typeChoices, default="Online")


    def __str__(self):
        return self.name
    
class Loan(models.Model):
    # Type Choices
    bank_name = models.CharField(max_length=200)
    scenerio = models.ForeignKey(Scenerio, on_delete=models.CASCADE, related_name="loan_scenerio")
    owner = models.ForeignKey(Business, null=True, on_delete=models.CASCADE,)
    amount = models.FloatField(default=10000.00)
    intrest = models.FloatField(default= .08)
    master = models.BooleanField(default=True)
    how_many_months = models.FloatField(default=36)
    payment = models.FloatField(default=0)
    total_value = models.FloatField(default=0)
    

    def __str__(self):
        return self.bank_name
    
class RoundNew(models.Model):
    number = models.IntegerField(default=1)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="roundnew_business")
    scenerio = models.ForeignKey(Scenerio, on_delete=models.CASCADE, related_name="roundnew_scenerio")
    description = models.CharField(max_length=2000)
    weather = models.DecimalField(default=.50, max_digits=100, decimal_places=2)
    turnout_chance = models.DecimalField(default=.10, max_digits=100, decimal_places=2)
    round_number = models.IntegerField(default=1)
    sales = models.FloatField(default=0)
    revenue = models.FloatField(default=0)
    ingredient_cost = models.FloatField(default=0)
    comission_cost = models.FloatField(default=0)
    total_varriable_cost = models.FloatField(default=0)
    gm = models.FloatField(default=0)
    salaries = models.FloatField(default=0)
    loan_payments = models.FloatField(default=0)
    event_payments = models.FloatField(default=0)
    marketing_spend = models.FloatField(default=0)
    total_fixed_cost = models.FloatField(default=0)
    net_income = models.FloatField(default=0)
    tax_expense = models.FloatField(default=0)
    profit = models.FloatField(default=0)
    comments = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.number
    
class Report(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="report_business")
    scenerio = models.ForeignKey(Scenerio, on_delete=models.CASCADE, related_name="report_scenerio")
    assets = models.FloatField(default=0)
    liabilities = models.FloatField(default=0)
    owners_equity = models.FloatField(default=0)
    vc_cut = models.FloatField(default=0)
    final_score = models.FloatField(default=0)
    feedback = models.CharField(max_length=2000, default="")
    total_sales = models.FloatField(default=0)
    total_revenue = models.FloatField(default=0)
    total_ingredient_costs = models.FloatField(default=0)
    total_comissions = models.FloatField(default=0)
    total_varriable_costs = models.FloatField(default=0)
    total_salaries = models.FloatField(default=0)
    total_loan_payments = models.FloatField(default=0)
    total_event_payments = models.FloatField(default=0)
    total_fixed_costs = models.FloatField(default=0)
    total_net_income = models.FloatField(default=0)
    total_tax_payments = models.FloatField(default=0)
    total_profit = models.FloatField(default=0)
    average_quantity_sold = models.FloatField(default=0)
    average_meal_price = models.FloatField(default=0)
    total_marketing_spend = models.FloatField(default=0)
    total_score = models.FloatField(default=0)
    def __str__(self):
        return self.business
    
class LogEntry(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="log_business", null=True)
    round = models.FloatField(default=0)
    message = models.CharField(max_length=2000)
    risk = models.FloatField(default=0)
    def __str__(self):
        return self.message
    
