import requests
def crawler():
    response = requests.get("https://www.google.com/search?q=houses+leicester")
    response.raise_for_status()
    print(response.text)
if __name__ == "__main__":
    crawler()