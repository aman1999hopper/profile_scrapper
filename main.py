import requests

def main():
    import requests
    from bs4 import BeautifulSoup
    from itertools import cycle

    # Sample Twitter profile URL
    url = 'https://twitter.com/sachin_rt'

    # List of proxy IPs
    proxies = ['proxy1_ip:port', 'proxy2_ip:port', 'proxy3_ip:port']

    # Create a proxy pool from the list of proxies
    proxy_pool = cycle(proxies)

    # Function to make a request with a proxy IP
    def make_request_with_proxy(url):
        proxy = next(proxy_pool)
        proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy
        }
        try:
            response = requests.get(url, proxies=proxies)
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
            # Retry with a new proxy
            return make_request_with_proxy(url)

    # Make the request using a proxy
    response = make_request_with_proxy(url)

    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the required data
        biography = soup.find('div', class_='ProfileHeaderCard-bio').text.strip()
        followers_count = int(
            soup.find('li', class_='ProfileNav-item--followers').find('span', class_='ProfileNav-value')['data-count'])
        following_count = int(
            soup.find('li', class_='ProfileNav-item--following').find('span', class_='ProfileNav-value')['data-count'])
        likes_count = int(
            soup.find('li', class_='ProfileNav-item--favorites').find('span', class_='ProfileNav-value')['data-count'])
        user_id = int(soup.find('div', class_='ProfileHeaderCard')['data-user-id'])

        # Print the extracted data
        print({
            'biography': biography,
            'followers_count': followers_count,
            'following_count': following_count,
            'likes_count': likes_count,
            'user_id': user_id
        })
    else:
        print(f"Request failed with status code {response.status_code}")

