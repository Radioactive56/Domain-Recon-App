from django.shortcuts import render
from .models import Domain,SubDomain,Config
from .serializers import Domain_Serializer,SubDomain_Serializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.utils import timezone


# import socket
# import subprocess
# import asyncio
# import aiohttp
# import json
# import os
# from datetime import datetime
# # Define top 100 ports
# TOP_100_PORTS = "21,22,23,25,53,80,110,135,139,143,443,445,993,995,1723,3306,3389,5900,8080,1025,1720,2049,5060,5061,5432,5357,49152,49153,49154,49155,49156,49157,1352,1433,1521,3306,5432,6379,27017,5985,5986,8888,9200,5601,6379,8000,8001,8443,9000,9001,9090,9091,5353,161,162,500,4500,1723,47,50,51,1194,1701,1812,1813,3306,5432,6667,6697,7000,8081,8082,8083,8084,8085,8086,8087,8088,8089,8889,8890,8891,8892,9092,9093,9094,9095,9201,9202,9300,9418,27015,27016,27017,27018,27019,27020"

# def save_to_file(data, domain):
#     timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     file_name = f"{domain}_{timestamp}.json"
#     file_path = os.path.join(os.getcwd(), file_name)
    
#     with open(file_path, 'w') as f:
#         json.dump(data, f, indent=4)
    
#     print(f"Results saved to {file_path}")

# def get_ip(domain):
#     try:
#         return socket.gethostbyname(domain)
#     except socket.gaierror:
#         return None

# async def get_geolocation(session, ip):
#     if ip == "Not Found":
#         return {"country": "NA", "state": "NA", "city": "NA", "latitude": "NA", "longitude": "NA", "isp": "NA", "asn": "NA", "ip_version": "NA"}
#     try:
#         async with session.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,isp,as,query", timeout=3) as response:
#             data = await response.json()
#             ip_version = "IPv6" if ":" in data.get("query", "") else "IPv4"
#             return {
#                 "country": data.get("country", "NA"),
#                 "state": data.get("regionName", "NA"),
#                 "city": data.get("city", "NA"),
#                 "latitude": str(data.get("lat", "NA")),
#                 "longitude": str(data.get("lon", "NA")),
#                 "isp": data.get("isp", "NA"),
#                 "asn": data.get("as", "NA"),
#                 "ip_version": ip_version
#             }
#     except:
#         return {"country": "NA", "state": "NA", "city": "NA", "latitude": "NA", "longitude": "NA", "isp": "NA", "asn": "NA", "ip_version": "NA"}

# async def check_ports(ip):
#     if ip == "Not Found":
#         return "NA"
#     try:
#         result = subprocess.check_output(['nmap', '-p', TOP_100_PORTS, '--open', '-Pn', ip], stderr=subprocess.DEVNULL)
#         open_ports = [line.split('/')[0] for line in result.decode().split('\n') if '/tcp' in line and 'open' in line]
#         return ', '.join(open_ports) if open_ports else "NA"
#     except subprocess.CalledProcessError:
#         return "NA"

# async def get_subdomains(domain):
#     try:
#         result = subprocess.check_output(['subfinder', '-d', domain], stderr=subprocess.DEVNULL)
#         return result.decode().splitlines()
#     except subprocess.CalledProcessError:
#         return []

# async def process_domain(domain, session):
#     ip = await get_ip(domain)
#     geo_info = await get_geolocation(session, ip)
#     open_ports = await check_ports(ip)
#     return {
#         "domain": domain,
#         "ip": ip,
#         "country": geo_info['country'],
#         "state": geo_info['state'],
#         "city": geo_info['city'],
#         "latitude": geo_info['latitude'],
#         "longitude": geo_info['longitude'],
#         "isp": geo_info['isp'],
#         "open_ports": open_ports,
#         "asn": geo_info['asn'],
#         "ip_version": geo_info['ip_version']
#     }

# async def process_domain_and_print(domain, session):
#     domain_results = [await process_domain(domain, session)]
#     subdomain_results = []
#     subdomains = await get_subdomains(domain)
    
#     # Track the count of subdomains
#     subdomain_count = len(subdomains)
    
#     for subdomain in subdomains:
#         subdomain_results.append(await process_domain(subdomain, session))

#     # Combine all results into a JSON structure
#     results = {
#         "domain": domain,
#         "domain_results": domain_results,
#         "subdomains": subdomain_results + [{"total_subdomains": subdomain_count}]
#     }

#     save_to_file(results, domain)
    
#     # Print all results as JSON to console
#     print(json.dumps(results, indent=4))

# async def main():
#     domains = input("Enter domain names (comma-separated): ").strip().split(',')
#     domains = [d.strip() for d in domains]
#     async with aiohttp.ClientSession() as session:
#         tasks = [process_domain_and_print(domain, session) for domain in domains]
#         await asyncio.gather(*tasks)

# if __name__ == "__main__":
#     domain_scan = 
#     process_domain_and_print(domain)

def get_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

def get_geolocation():
    # if ip == None:
    #     return {"country": "NA", "state": "NA", "city": "NA", "latitude": "NA", "longitude": "NA", "isp": "NA", "asn": "NA", "ip_version": "NA"}
    doamin_list = Domain.objects.filter(domain_scan_start_time__isnull=False,
    domain_scan_end_time__isnull=True,domain_status='Domain Scanning InProgress').order_by('-priority')
    domain_obj = domain_list.first()
    try:
        data = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,isp,as,query")
        data = data.json()
        ip_version = "IPv6" if ":" in data.get("query", "") else "IPv4"
        return {
            "country": data.get("country", "NA"),
            "state": data.get("regionName", "NA"),
            "city": data.get("city", "NA"),
            "latitude": str(data.get("lat", "NA")),
            "longitude": str(data.get("lon", "NA")),
            "isp": data.get("isp", "NA"),
            "asn": data.get("as", "NA"),
            "ip_version": ip_version
        }
    except:
        # return {"country": "NA", "state": "NA", "city": "NA", "latitude": "NA", "longitude": "NA", "isp": "NA", "asn": "NA", "ip_version": "NA"}
        domain_obj.domain_status = 'Domain Scanning Aborted'
        domain_obj.domain_abort_reason= 'Ip not found for the particular domain...'
        domain_obj.domain_scan_end_time=timezone.now()
        print(f'{domain_obj} scan aborted at {domain_obj.domain_scan_end_time} due to {domain_obj.domain_abort_reason}')




def get_ip_check():
    domain_list = Domain.objects.filter(domain_scan_start_time__isnull=False,
    domain_scan_end_time__isnull=True,domain_status='Domain Scanning InProgress').order_by('-priority')
    domain_obj=domain_list.first()
    print(f'Domain name of {domain_obj.domain_name} is sent to scan.... running this function get_ip(domain)...')
    ip = get_ip(domain)
    if ip:
        domain_obj.domain_status = 'Domain ip found successfully'
        print(f'get_ip function successfully executed with result as {ip}')
        domain_obj.domain_ip = ip
    else:
        domain_obj.domain_status = 'Domain Scanning Aborted'
        domain_obj.domain_abort_reason= 'Ip not found for the particular domain...'
        domain_obj.domain_scan_end_time=timezone.now()
        print(f'{domain_obj} scan aborted at {domain_obj.domain_scan_end_time} due to {domain_obj.domain_abort_reason}')


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


def check_status_for_completion():

    scan_in_progress_domain = Domain.objects.filter(domain_scan_start_time__isnull=False,
    domain_scan_end_time__isnull=True,domain_status='Domain Scanning InProgress')

    print(scan_in_progress_domain)




if __name__==__main__:
    
    if Config.scan_count==0:
        pass
    else:
        start_scan()


