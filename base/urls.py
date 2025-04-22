from django.urls import path
from .views import Add_Domain,get_domain_priority
urlpatterns=[
    path('addDomain/',Add_Domain),
    path('get/',get_domain_priority),
]