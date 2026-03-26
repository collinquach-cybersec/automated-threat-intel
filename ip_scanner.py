import requests
import argparse
import csv
import os
from dotenv import load_dotenv

# Load the hidden API key from the .env file
load_dotenv()
API_KEY = os.getenv('ABUSEIPDB_API_KEY')
URL = 'https://api.abuseipdb.com/api/v2/check'

def check_ip(ip_address):
    """Query AbuseIPDB for a single IP address and return a dictionary of the results."""
    querystring = {
        'ipAddress': ip_address,
        'maxAgeInDays': '90'
    }
    headers = {
        'Accept': 'application/json',
        'Key': API_KEY
    }
    
    try:
        response = requests.get(url=URL, headers=headers, params=querystring)
        response.raise_for_status() 
        data = response.json()['data']
        
        # Format the data we care about into a clean dictionary
        return {
            'IP Address': data['ipAddress'],
            'ISP / Owner': data['isp'],
            'Domain': data.get('domain', 'N/A'),
            'Malicious Score (%)': data['abuseConfidenceScore'],
            'Total Reports': data['totalReports']
        }
    except requests.exceptions.RequestException as e:
        print(f"[!] Error checking IP {ip_address}: {e}")
        return None

def main():
    # Setup the Command Line Interface (CLI) arguments
    parser = argparse.ArgumentParser(description="Automated Threat Intel IP Scanner")
    parser.add_argument('-i', '--ip', help="Single IP address to scan")
    parser.add_argument('-f', '--file', help="Text file containing a list of IPs (one per line)")
    parser.add_argument('-o', '--output', help="Output CSV file name (e.g., report.csv)")
    
    args = parser.parse_args()
    
    # Security check: Ensure the API key loaded correctly
    if not API_KEY:
        print("[!] Error: API Key not found. Please check your .env file.")
        return

    results = []

    # Scenario 1: User provided a single IP
    if args.ip:
        print(f"[*] Scanning single IP: {args.ip}...")
        result = check_ip(args.ip)
        if result:
            results.append(result)
            print(f"    [+] Score: {result['Malicious Score (%)']}% | ISP: {result['ISP / Owner']}")
            
    # Scenario 2: User provided a text file full of IPs
    elif args.file:
        print(f"[*] Reading IPs from file: {args.file}...")
        try:
            with open(args.file, 'r') as file:
                # Read lines, strip whitespace, and ignore empty lines
                ips = [line.strip() for line in file if line.strip()]
                
            for ip in ips:
                result = check_ip(ip)
                if result:
                    results.append(result)
                    print(f"    [+] {ip} -> Score: {result['Malicious Score (%)']}%")
        except FileNotFoundError:
            print(f"[!] Error: File '{args.file}' not found.")
            return
    else:
        print("[!] Please provide an IP (-i) or a file (-f). Use -h for help.")
        return

    # Export to CSV if the user requested it
    if args.output and results:
        keys = results[0].keys()
        try:
            with open(args.output, 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(results)
            print(f"\n[*] Success: Threat Intel Report saved to {args.output}")
        except IOError:
            print(f"[!] Error writing to {args.output}")

if __name__ == '__main__':
    main()