import requests
import whois
import dns.resolver
from bs4 import BeautifulSoup
import socket
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import tweepy
import shodan
import os

class OSINTTool:
    def __init__(self, target_domain):
        self.target_domain = target_domain

  
    def get_ssl_certificate_info(domain):
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(socket.AF_INET), server_hostname=domain) as ssock:
            ssock.connect((domain, 443))
            cert = ssock.getpeercert(binary_form=True)
        
        x509cert = x509.load_der_x509_certificate(cert, default_backend())
        return {
            "Issuer": x509cert.issuer.rfc4514_string(),
            "Subject": x509cert.subject.rfc4514_string(),
            "Valid From": x509cert.not_valid_before,
            "Valid To": x509cert.not_valid_after,
        }
    except Exception as e:
        return str(e)

    def get_geolocation_info(ip_address):
    try:
        api_key = "YOUR_IPINFO_API_KEY"
        url = f"https://ipinfo.io/{ip_address}/json?token={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            geolocation_data = response.json()
            return {
                "City": geolocation_data.get("city", "N/A"),
                "Region": geolocation_data.get("region", "N/A"),
                "Country": geolocation_data.get("country", "N/A"),
                "Coordinates": geolocation_data.get("loc", "N/A"),
            }
        else:
            return f"Failed to retrieve geolocation data (HTTP {response.status_code})"
    except Exception as e:
        return str(e)



    def search_twitter_for_username(username):
      consumer_key = "YOUR_TWITTER_API_CONSUMER_KEY"
      consumer_secret = "YOUR_TWITTER_API_CONSUMER_SECRET"
      access_token = "YOUR_TWITTER_API_ACCESS_TOKEN"
      access_token_secret = "YOUR_TWITTER_API_ACCESS_TOKEN_SECRET"
    
      auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
      auth.set_access_token(access_token, access_token_secret)
      api = tweepy.API(auth)
    
      try:
        user = api.get_user(screen_name=username)
        return {
            "Twitter Username": user.screen_name,
            "Twitter Name": user.name,
            "Twitter Description": user.description,
            "Followers": user.followers_count,
            "Following": user.friends_count,
        }
      except tweepy.error.TweepError as e:
        return f"Twitter account not found: {str(e)}"

    def shodan_search(query, api_key):
      try:
        api = shodan.Shodan(api_key)
        results = api.search(query)
        return results
    except shodan.exception.APIError as e:
        return f"Shodan API Error: {str(e)}"

    def run(self):
        osint_results = {
            "Target Domain": self.target_domain,
            "Whois Information": self.get_whois_info(),
            "DNS Records": self.get_dns_records(),
            "Website Title": self.get_website_title(),
            "SSL Certificate Info": self.get_ssl_certificate_info(),
            "Geolocation Info": self.get_geolocation_info(),
            "Twitter Info": self.search_twitter_for_username(),
            "Shodan Info": self.shodan_search(),
            # Add more results from additional features here
        }
        return osint_results

if __name__ == "__main__":
    target_domain = input("Enter the target domain or website URL: ")
    osint_tool = OSINTTool(target_domain)
    results = osint_tool.run()
    
    # Display the results
    for key, value in results.items():
        print(f"{key}:\n{value}\n")
