from django import forms
from .models import *
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

class ScenerioForm(forms.ModelForm):
    class Meta:
        model = Scenerio
        fields = ['name','description',"max_rounds"]

class FoodTruckForm(forms.ModelForm):
    class Meta:
        model = FoodTruck
        fields = ['name','price','description','capacityBonus','qualityBonus']

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name','description','salary','comission','capacityBonus','qualityBonus']

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name','description','price','qualityBonus','capacityCost']

class MarketSegmentForm(forms.ModelForm):
    class Meta:
        model = MarketSegment
        fields = ['name','description','population','priceSensitivity','qualitySensitivity','onlineMarketingSensitivity','onlineMarketingSensitivity','printMarketingSensitivity','wordOfMouthMarketingSensitivity','weatherSensitivity','comfortFoodPreference','italianFoodPreference','asianFoodPreference','dessertPreference','smoothieFoodPreference']

class RoundForm(forms.ModelForm):
    class Meta:
        model = RoundNew
        fields = []

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['firstAndLastName','gender','yearsofBusinessEducationExperince','yearsProfessionalExperince','jobTitle','industry']

class BusinessIdentityForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['foodType','foodTruckName','mission','vision','values','summarize_your_strategy']

class PriceForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['price']

class MarketingCampaignForm(forms.ModelForm):
    class Meta:
        model = MarketingCampaign
        fields = ['name',"marketing_type"]

class PurchaseIngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = []

class PurchaseTruckForm(forms.ModelForm):
    class Meta:
        model = FoodTruck
        fields = []

class HireForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = []

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ['bank_name', 'amount','intrest','how_many_months']

class TakeLoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = []

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["feedback"]