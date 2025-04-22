from django.shortcuts import render
from .models import Domain,SubDomain,Config
from .serializers import Domain_Serializer,SubDomain_Serializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.utils import timezone
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import JsonResponse
 
 
import socket
import subprocess
 
import json
import os
from datetime import datetime
# Define top 100 ports
TOP_100_PORTS = "21,22,23,25,53,80,110,135,139,143,443,445,993,995,1723,3306,3389,5900,8080,1025,1720,2049,5060,5061,5432,5357,49152,49153,49154,49155,49156,49157,1352,1433,1521,3306,5432,6379,27017,5985,5986,8888,9200,5601,6379,8000,8001,8443,9000,9001,9090,9091,5353,161,162,500,4500,1723,47,50,51,1194,1701,1812,1813,3306,5432,6667,6697,7000,8081,8082,8083,8084,8085,8086,8087,8088,8089,8889,8890,8891,8892,9092,9093,9094,9095,9201,9202,9300,9418,27015,27016,27017,27018,27019,27020"
 
 
@api_view(['POST'])
def Add_Domain(request):
    serializer = Domain_Serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
 
def check_subdomain_ports(subdomain_obj,ip):
    try:
        result = subprocess.check_output(['nmap', '-p', TOP_100_PORTS, '--open', '-Pn', ip], stderr=subprocess.DEVNULL)
        open_ports = [line.split('/')[0] for line in result.decode().split('\n') if '/tcp' in line and 'open' in line]
        subdomain_obj.subdomain_open_ports = ', '.join(open_ports) if open_ports else "NA"
        subdomain_obj.save()
        print(f'{subdomain_obj} save updated for open ports.....')
    except subprocess.CalledProcessError:
        print(f'Namp Scan Failed... for {subdomain_obj}')
 
 
 
def get_subdomain_geolocation(subdomain_obj,ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,isp,as,query")
        if response.status_code==200:
            data = response.json()
            print(data)
            ip_version = "IPv6" if ":" in data.get("query", "") else "IPv4"
            subdomain_obj.subdomain_country = data.get("country", "NA")
            subdomain_obj.subdomain_state = data.get("regionName", "NA")
            subdomain_obj.subdomain_city = data.get("city", "NA")
            subdomain_obj.subdomain_latitude = str(data.get("lat", "NA"))
            subdomain_obj.subdomain_longitude = str(data.get("lon", "NA"))
            subdomain_obj.subdomain_isp = data.get("isp", "NA")
            subdomain_obj.subdomain_asn = data.get("as", "NA")
            subdomain_obj.save()
            print(f'{subdomain_obj} save updated for geolocation...')
    except:
        print(f'subdomain geolocation call failed...{subdomain_obj}')
 
 
 
def scan_all_subdomains():
    print('Hello from get_subdomain().........................')
    # if ip == None:
    #     return {"country": "NA", "state": "NA", "city": "NA", "latitude": "NA", "longitude": "NA", "isp": "NA", "asn": "NA", "ip_version": "NA"}
    domain_list = Domain.objects.filter(domain_scan_start_time__isnull=False,
    domain_scan_end_time__isnull=True,domain_status='SubFinder Scan Completed').order_by('-priority')
    if len(domain_list)==0:
        print('There is no scannable domain available for scan_all_subdomains()..')
        return 'There is no scannable domain available for scan_all_subdomains()'
    domain_obj = domain_list.first()
    subdomain_list = SubDomain.objects.filter(domain=domain_obj)
 
    for subdomain in subdomain_list:
        ip = get_ip(subdomain.subdomain_name)
        if ip:
            print(f'get_ip function successfully executed with result as {ip}')
            subdomain.subdomain_ip=ip
            subdomain.save()
            get_subdomain_geolocation(subdomain,subdomain.subdomain_ip)
            check_subdomain_ports(subdomain,subdomain.subdomain_ip)
            print(f'This subdomain scan has been completed...')
            domain_obj.domain_scan_end_time = timezone.now()
            domain_obj.domain_status = 'Domain Scanning Completed'
            domain_obj.save()
        else:
            print(f'This subdomain object has been skipped {subdomain}')
            continue
 
def get_subdomains():
    print('Hello from get_subdomain().........................')
    # if ip == None:
    #     return {"country": "NA", "state": "NA", "city": "NA", "latitude": "NA", "longitude": "NA", "isp": "NA", "asn": "NA", "ip_version": "NA"}
    domain_list = Domain.objects.filter(domain_scan_start_time__isnull=False,
    domain_scan_end_time__isnull=True,domain_status='Nmap Scan Completed').order_by('-priority')
    if len(domain_list)==0:
        print('There is no scannable domain available for get_subdomain()..')
        return 'There is no scannable domain available for get_subdomain()..'
    domain_obj = domain_list.first()
    print(domain_obj)
    d_name = domain_obj.domain_name
    try:
        result = subprocess.check_output(['subfinder', '-d', d_name], stderr=subprocess.DEVNULL)
        subdomain_output=result.decode().splitlines()
        domain_obj.subdomain_count=len(subdomain_output)
        domain_obj.domain_status='SubFinder Scan Completed'
        domain_obj.save()
        for i in subdomain_output:
            if not SubDomain.objects.filter(subdomain_name=i,domain=domain_obj).exists():
                SubDomain.objects.create(subdomain_name=i,domain=domain_obj)
                print(f'Created Subdomain {i}')
            else:
                print(f'{i} skipped cause it already exists....')
    except subprocess.CalledProcessError:
        print(f'No Subdomain found for {domain_obj.domain_name}')
        domain_obj.domain_status = 'Domain Scanning Completed'
        domain_obj.domain_stop_reason = 'Subfinder process got aborted....'
        domain_obj.subdomain_count=0
        domain_obj.save()
        config = Config.objects.get(pk=1)
        config.scan_count-=1
        config.save()
 
def check_ports():
    print('Hello from check_ports().........................')
    # if ip == None:
    #     return {"country": "NA", "state": "NA", "city": "NA", "latitude": "NA", "longitude": "NA", "isp": "NA", "asn": "NA", "ip_version": "NA"}
    domain_list = Domain.objects.filter(domain_scan_start_time__isnull=False,
    domain_scan_end_time__isnull=True,domain_status='Geolocation Scan Completed').order_by('-priority')
    if len(domain_list)==0:
        print('There is no scannable domain available for check_ports()..')
        return 'There is no scannable domain available for check_ports()..'
    domain_obj = domain_list.first()
    print(domain_obj)
    ip = domain_obj.domain_ip
    print(ip)
    try:
        result = subprocess.check_output(['nmap', '-p', TOP_100_PORTS, '--open', '-Pn', ip], stderr=subprocess.DEVNULL)
        open_ports = [line.split('/')[0] for line in result.decode().split('\n') if '/tcp' in line and 'open' in line]
        print(', '.join(open_ports) if open_ports else "NA")
        domain_obj.domain_open_ports = ', '.join(open_ports) if open_ports else "NA"
        domain_obj.domain_status = 'Nmap Scan Completed'
        domain_obj.save()
        print(f'{domain_obj} check ports data successfully.......')
   
    except:
        # domain_obj.domain_status = 'Domain Scanning Aborted'
        print(f'{domain_obj} nmap scan aborted.')
        domain_obj.domain_stop_reason= 'Nmap subprocess code failure....'
        # domain_obj.domain_scan_end_time=timezone.now()
        # print(f'{domain_obj} scan aborted at {domain_obj.domain_scan_end_time} due to {domain_obj.domain_stop_reason}')
        domain_obj.save()

 
def get_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None
 
def get_geolocation():
    print('Hello from get_geolocation().........................')
    # if ip == None:
    #     return {"country": "NA", "state": "NA", "city": "NA", "latitude": "NA", "longitude": "NA", "isp": "NA", "asn": "NA", "ip_version": "NA"}
    domain_list = Domain.objects.filter(domain_scan_start_time__isnull=False,
    domain_scan_end_time__isnull=True,domain_status='Domain ip found').order_by('-priority')
    if len(domain_list)==0:
        print('There is no scannable domain available for get_geolocation()..')
        return 'There is no scannable domain available for get_geolocation()..'
    domain_obj = domain_list.first()
 
    print(domain_obj.domain_id)
    ip = domain_obj.domain_ip
    print(ip)
    print(f'Domain name of {domain_obj.domain_name} is running in function get_geolocation()...')
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,isp,as,query")
        if response.status_code==200:
            data = response.json()
            print(data)
            ip_version = "IPv6" if ":" in data.get("query", "") else "IPv4"
            print(f'Hello this is the domain obj :{domain_obj}')
            domain_obj.domain_country = data.get("country", "NA")
            domain_obj.domain_state = data.get("regionName", "NA")
            domain_obj.domain_city = data.get("city", "NA")
            domain_obj.domain_latitude = str(data.get("lat", "NA"))
            domain_obj.domain_longitude = str(data.get("lon", "NA"))
            domain_obj.domain_isp = data.get("isp", "NA")
            domain_obj.domain_asn = data.get("as", "NA")
            domain_obj.domain_ip_version = ip_version
            domain_obj.domain_status = 'Geolocation Scan Completed'
            domain_obj.save(force_update=True)
            print('Domain object saved successfully.')
            config = Config.objects.get(pk=1)
            config.scan_count-=1
            config.save()
   
    except:
        # return {"country": "NA", "state": "NA", "city": "NA", "latitude": "NA", "longitude": "NA", "isp": "NA", "asn": "NA", "ip_version": "NA"}
        domain_obj.domain_status = 'Domain Scanning Aborted'
        domain_obj.domain_stop_reason= 'Ip call for geolocation function failed....'
        domain_obj.domain_scan_end_time=timezone.now()
        print(f'{domain_obj} scan aborted at {domain_obj.domain_scan_end_time} due to {domain_obj.domain_stop_reason}')
        domain_obj.save()
        config = Config.objects.get(pk=1)
        config.scan_count-=1
        config.save()
 
 
 
def get_ip_check():
    print('Hello from get_ip_check()..........................')
    domain_list = Domain.objects.filter(domain_scan_start_time__isnull=False,
    domain_scan_end_time__isnull=True,domain_status='Domain Scanning InProgress').order_by('-priority')
    if len(domain_list)==0:
        print('There is no scannable domain available for get_ip_check()..')
        return 'There is no scannable domain available for get_ip_check()..'
    domain_obj=domain_list.first()
    print(f'Domain name of {domain_obj.domain_name} is running in function get_ip()...')
    ip = get_ip(domain_obj.domain_name)
    if ip:
        domain_obj.domain_status = 'Domain ip found'
        print(domain_obj.domain_status)
        print(f'get_ip function successfully executed with result as {ip}')
        domain_obj.domain_ip = ip
        domain_obj.save()
    else:
        domain_obj.domain_status = 'Domain Scanning Aborted'
        domain_obj.domain_stop_reason= 'Ip not found for the particular domain...'
        domain_obj.domain_scan_end_time=timezone.now()
        print(f'{domain_obj} scan aborted at {domain_obj.domain_scan_end_time} due to {domain_obj.domain_stop_reason}')
        domain_obj.save()
        config = Config.objects.get(pk=1)
        config.scan_count-=1
        config.save()
 
def start_scan():
 
    print('Start Scan Function is called................')
    unscanned_domain_objects = Domain.objects.filter(domain_scan_start_time__isnull=True,
    domain_scan_end_time__isnull=True).order_by('-priority')
 
    print(unscanned_domain_objects)
    config = Config.objects.get(pk=1)
    print(f'The scan count of the script is : {config.scan_count}')
    if len(unscanned_domain_objects)>0:
        for domain_obj in unscanned_domain_objects:
            # start_scan(domain_obj)
            if config.scan_count==0:
                config.scan_count += 1
                domain_obj.domain_scan_start_time = timezone.now()
                print(f'Updated {domain_obj} start time to {timezone.now()}')
                domain_obj.domain_status = 'Domain Scanning InProgress'
                print(f'Updated {domain_obj} status to Domain Scanning InProgress')
                config.save()
                domain_obj.save()
                print(f'Added {domain_obj} to the Scan at {timezone.now()}')
            else:
                print('Cannot add anymore Domain for scan as the queue is full........')
                break
    else:
        print('No Domains available for Scan.................')
 
 
@api_view(['GET'])
def get_domain_priority(request):
    start_scan()
    get_ip_check()
    get_geolocation()
    check_ports()
    get_subdomains()
    scan_all_subdomains()