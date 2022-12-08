from django.contrib import admin

# Register your models here.
from django.contrib import admin
from water_system.models import RootS, AddrArea, User, Customer, CustomerAction, Water, WorkAction, Work, StoreHouse, ProviserAction, Provider, Money

admin.site.register(RootS)
admin.site.register(AddrArea)
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(CustomerAction)
admin.site.register(Work)
admin.site.register(Water)
admin.site.register(WorkAction)
admin.site.register(StoreHouse)
admin.site.register(Provider)
admin.site.register(ProviserAction)
admin.site.register(Money)



