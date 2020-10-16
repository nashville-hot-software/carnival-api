"""carnivalproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from carnivalapi.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'customers', Customers, 'customer')
router.register(r'dealerships', Dealerships, 'dealership')
router.register(r'sales', Sales, 'sales')
router.register(r'accountsreceivable', AccountsReceivable, 'accountsreceivable')
router.register(r'carrepairs', CarRepairTypes, 'carrepairs')
router.register(r'dealershipemployees', DealershipEmployees, 'dealershipemployees')
router.register(r'employees', Employees, 'employees')
router.register(r'employeetypes', EmployeeTypes, 'employeetypes')
router.register(r'vehicletype', VehicleTypes, 'vehicletype')
router.register(r'vehiclebodytype', VehicleBodyTypes, 'vehiclebodytype')
router.register(r'repairtype', RepairTypes, 'repairtype')
router.register(r'oilchangelog', OilChangeLogs, 'oilchangelog')

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
