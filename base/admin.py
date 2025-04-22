from django.contrib import admin
from .models import Domain,SubDomain,Config

class ConfigAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        if Config.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False

class SubDomainAdmin(admin.ModelAdmin):
    search_fields = ['subdomain_name']

    list_display=['subdomain_name','domain','subdomain_ip','subdomain_ip','subdomain_open_ports']


class DomainAdmin(admin.ModelAdmin):
    search_fields = ['domain_name']

    list_display=['domain_name','domain_ip','domain_open_ports','domain_status']


admin.site.register(Domain,DomainAdmin)
admin.site.register(SubDomain,SubDomainAdmin)
admin.site.register(Config,ConfigAdmin)