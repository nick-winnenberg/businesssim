from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', views.home, name='game-home'),
    path('scenerio/new', views.new_scenerio, name='new_scenerio'),
    path('scenerio/maker/<int:pk>', views.scenerio_maker, name='scenerio_maker'),
    path('foodtruck/new/<int:pk>', views.new_food_truck, name='new_food_truck'),
    path('employee/new/<int:pk>', views.new_employee, name='new_employee'),
    path('ingredient/new/<int:pk>', views.new_ingredient, name='new_ingredient'),
    path('market_segment/new/<int:pk>', views.new_market_segment, name='new_market_segment'),
    path('loan/new/<int:pk>', views.new_loan, name='new_loan'),
    path('round/new/<int:pk>', views.new_round, name='new_round'),
    path('business/new/<int:pk>', views.new_business, name='new_business'),
    path('business/edit_identity/<int:pk>', views.edit_identity, name='edit_identity'),
    path('player_dashboard/<int:pk>', views.player_dashboard, name='player_dashboard'),
    path('shop/<int:pk>', views.shop, name='shop'),
    path('business/increase_price/<int:pk>', views.increase_price, name='increase_price'),
    path('business/decrease_price/<int:pk>', views.decrease_price, name='decrease_price'),
    path('business/new_marketing_campaign/<int:pk>', views.new_marketing_campaign, name='new_marketing_campaign'),
    path('business/purchase_ingredient/<int:pk>', views.purhcase_ingredient, name='purchase_ingredient'),
    path('business/delete_ingredient/<int:pk>', views.delete_ingredient, name='delete_ingredient'),
    path('business/carlot/<int:pk>', views.carlot, name='carlot'),
    path('business/purchase_truck/<int:pk>', views.purhcase_truck, name='purchase_truck'),
    path('business/staffing/<int:pk>', views.staffing, name='staffing'),
    path('business/hire_employee/<int:pk>', views.hire_employee, name='hire_employee'),
    path('business/market_research/<int:pk>', views.market_research, name='market_research'),
    path('business/delete_e/<int:pk>', views.delete_employee, name='delete_employee'),
    path('business/delete_ft/<int:pk>', views.delete_truck, name='delete_truck'),
    path('business/delete_mkt/<int:pk>', views.delete_marketing, name='delete_marketing'),
    path('business/next_round/<int:pk>', views.next_round, name='next_round'),
    path('business/bank/<int:pk>', views.bank, name='bank'),
    path('business/take_loan/<int:pk>', views.take_loan, name='take_loan'),
    path('business/delete_business/<int:pk>', views.delete_business, name='delete_business'),
    path('business/vc/<int:pk>', views.vc, name='vc'),
    path('business/vc_trade/<int:pk>', views.vc_trade, name='vc_trade'),
    path('business/new_report/<int:pk>', views.new_report, name='new_report'),
    path('the_end/<int:pk>', views.the_end, name='the_end'),
    path('scoreboard/<int:pk>', views.scoreboard, name='scoreboard'),
    path('payoff_loan/<int:pk>', views.payoff_loan, name='payoff_loan'),
    path('pull_results/<int:pk>', views.pull_results, name='pull_results'),

]