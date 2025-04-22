from django.db import models

# Create your models here.
class Domain(models.Model):
    status_choices=[
        ('Domain Added','Domain Added'),
        ('Domain Scanning InProgress','Domain Scanning InProgress'),
        ('Domain ip found','Domain ip found'),
        ('Geolocation Scan Completed','Geolocation Scan Completed'),
        ('Nmap Scan Completed','Nmap Scan Completed'),
        ('SubFinder Scan Completed','SubFinder Scan Completed'),
        ('Domain Scanning Completed','Domain Scanning Completed'),
        ('Domain Scanning Aborted','Domain Scanning Aborted')
    ]
    ip_choices = [
        ('NA','NA'),
        ('IPv4','IPv4'),
        ('IPv6','IPv6')
    ]
    priority_choices =[
        ('2','Very High Priority'),
        ('1','High Priority'),
        ('0','Normal'),
    ]
    domain_id = models.BigAutoField(primary_key=True)
    domain_name = models.CharField(max_length=128,unique=True)
    domain_add_time = models.DateTimeField(auto_now_add=True)
    domain_scan_start_time = models.DateTimeField(blank=True,null=True)
    domain_scan_end_time = models.DateTimeField(blank=True,null=True)
    domain_ip = models.GenericIPAddressField(blank=True,null=True)
    domain_country = models.CharField(max_length=128,blank=True,null=True)
    domain_state = models.CharField(max_length=128,blank=True,null=True)
    domain_city = models.CharField(max_length=128,blank=True,null=True)
    domain_latitude = models.CharField(max_length=128,blank=True,null=True)
    domain_longitude = models.CharField(max_length=128,blank=True,null=True)
    domain_isp = models.CharField(max_length=128,blank=True,null=True)
    domain_open_ports = models.CharField(max_length=128,blank=True,null=True)
    domain_asn = models.CharField(max_length=128,blank=True,null=True)
    domain_ip_version = models.CharField(max_length=128,blank=True,null=True,choices=ip_choices)
    domain_status = models.CharField(max_length=128,choices=status_choices,default='Domain Added')
    domain_result_file = models.FileField(blank=True,null=True)
    domain_abort_reason = models.CharField(max_length=128,blank=True,null=True)
    subdomain_count = models.IntegerField(blank=True,null=True)
    priority = models.CharField(choices=priority_choices,max_length=2,default='0')

    def __str__(self):
        return self.domain_name

class SubDomain(models.Model):
    subdomain_id = models.BigAutoField(primary_key=True)
    domain = models.ForeignKey(Domain,on_delete=models.RESTRICT,to_field ='domain_id')
    subdomain_name =  models.CharField(max_length=128,unique=True)
    subdomain_ip = models.GenericIPAddressField(blank=True,null=True)
    subdomain_country = models.CharField(max_length=128,blank=True,null=True)
    subdomain_state = models.CharField(max_length=128,blank=True,null=True)
    subdomain_city = models.CharField(max_length=128,blank=True,null=True)
    subdomain_latitude = models.CharField(max_length=128,blank=True,null=True)
    subdomain_longitude = models.CharField(max_length=128,blank=True,null=True)
    subdomain_isp = models.CharField(max_length=128,blank=True,null=True)
    subdomain_open_ports = models.CharField(max_length=128,blank=True,null=True)
    subdomain_asn = models.CharField(max_length=128,blank=True,null=True)
    subdomain_ip_version = models.CharField(max_length=128,blank=True,null=True)

    def __str__(self):
        return self.subdomain_name


class Config(models.Model):
    scan_count = models.PositiveIntegerField(default=0, help_text="The current scan count of the domains in queue.")

    def __str__(self):
        return f'Scan Count of the Script is : {self.scan_count} '
