#Imports
import scratchattach as sa
import oslogin
import os
import requests
import conversion

#Setup
password = os.getenv('PASSWORD')  # Password stored in environment variable PASSWORD

session = sa.login("uukelele", password)
cloud = session.connect_scratch_cloud("1100152494")
client = cloud.requests(no_packet_loss=True, respond_order="finish")
tcloud = sa.get_tw_cloud("1100152494")
tclient = tcloud.requests(no_packet_loss=True, respond_order="finish")

#Setting up directories
os.makedirs("user_data", exist_ok=True)

@client.event
def on_ready():
    print("[TitanicOS Backend] [scratch] Request handler is running!")

@tclient.event
def on_ready():
    print("[TitanicOS Backend] [turbowarp] Request handler is running!")

@client.request
def ping(username):
    print(f"[TitanicOS Backend] [scratch] Pinged by {username}")
    return "pong"

@tclient.request
def ping(username):
    print(f"[TitanicOS Backend] [turbowarp] Pinged by {username}")
    return "pong"

@client.request
def login(username, password):
    print("[TitanicOS Backend] [scratch] Login request received.")
    response = oslogin.process_login(username, password)
    print(f"[TitanicOS Backend] {response}")
    return response

@tclient.request
def login(username, password):
    print("[TitanicOS Backend] [turbowarp] Login request received.")
    response = oslogin.process_login(username, password)
    print(f"[TitanicOS Backend] {response}")
    return response

@client.request
def check_user(username):
    print(f"[TitanicOS Backend] [scratch] Check user request received for Scratch username: {username}")
    response = oslogin.process_check_user(username)
    print(response)
    return response

@tclient.request
def check_user(username):
    print(f"[TitanicOS Backend] [turbowarp] Check user request received for Scratch username: {username}")
    response = oslogin.process_check_user(username)
    print(response)
    return response

@client.request
def create_account(username, password):
    print(f"[scratch] Create account request received for username: {username}")
    response = oslogin.process_create_account(username, password)
    os.makedirs(f"user_data/{username}")
    print(response)
    return response

@tclient.request
def create_account(username, password):
    print(f"[turbowarp] Create account request received for username: {username}")
    response = oslogin.process_create_account(username, password)
    os.makedirs(f"user_data/{username}")
    print(response)
    return response

@client.request
def bot_ai(model, query, username):
    response = requests.get(f"http://uukelele.ddns.net/duckchat?model={model}&q={query}").content.decode("utf-8")
    with open('capture.log', 'a') as file:
        file.write(f"\n{username} --- Used {model} to request '{query}', and the model responded with '{response}'")
    return response

@tclient.request
def bot_ai(model, query, username):
    response = requests.get(f"http://uukelele.ddns.net/duckchat?model={model}&q={query}").content.decode("utf-8")
    with open('capture.log', 'a') as file:
        file.write(f"\n{username} --- Used {model} to request '{query}'.")
    return response

@client.request
def view_folder(username):
    parent_folder = f'./user_data/{username}'
    items = os.listdir(parent_folder)
    items_list = []

    for item in items:
        item_path = os.path.join(parent_folder, item)
        if os.path.isdir(item_path):
            items_list.append(f"1{item}")
        else:
            items_list.append(f"0{item}")
    
    return items_list

@tclient.request
def view_folder(username):
    parent_folder = f'./user_data/{username}'
    items = os.listdir(parent_folder)
    items_list = []

    for item in items:
        item_path = os.path.join(parent_folder, item)
        if os.path.isdir(item_path):
            items_list.append(f"1{item}")
        else:
            items_list.append(f"0{item}")
    
    return items_list

@client.request
def get_weather(location):
    # Your WeatherAPI key
    api_key = 'b5d7f18efb744bfe9c4135951242408'
    
    # Fetch weather data from WeatherAPI
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    response = requests.get(url)
    
    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()
        
        # Extract necessary details from the response
        location_name = data['location']['name']
        region = data['location']['region']
        country = data['location']['country']
        temp_c = data['current']['temp_c']
        condition = data['current']['condition']['text']
        wind_mph = data['current']['wind_mph']
        humidity = data['current']['humidity']
        feelslike_c = data['current']['feelslike_c']

        # Format the return as requested
        weather_info = [location_name,condition,f"Temp: {temp_c}°C",f"Wind: {wind_mph} mph",f"Humidity: {humidity}%",f"Feels like: {feelslike_c}°C"]
        
        return weather_info
    else:
        return f"Error fetching weather data for {location}"

@tclient.request
def get_weather(location):
    # Your WeatherAPI key
    api_key = 'b5d7f18efb744bfe9c4135951242408'
    
    # Fetch weather data from WeatherAPI
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    response = requests.get(url)
    
    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()
        
        # Extract necessary details from the response
        location_name = data['location']['name']
        region = data['location']['region']
        country = data['location']['country']
        temp_c = data['current']['temp_c']
        condition = data['current']['condition']['text']
        wind_mph = data['current']['wind_mph']
        humidity = data['current']['humidity']
        feelslike_c = data['current']['feelslike_c']

        # Format the return as requested
        weather_info = [location_name,condition,f"Temp: {temp_c}°C",f"Wind: {wind_mph} mph",f"Humidity: {humidity}%",f"Feels like: {feelslike_c}°C"]
        
        return weather_info
    else:
        return f"Error fetching weather data for {location}"

@client.request
def get_news(location):
    # Fetch news from NewsAPI, limiting to 5 results
    response = requests.get(f"https://newsapi.org/v2/everything?q={location}&apiKey=3fc7112ae7f84c2e8ec14106576d2a0f&pageSize=5")
    
    # Parse the response JSON
    news_data = response.json()
    
    # Check if the request was successful
    if news_data.get("status") == "ok" and news_data.get("articles"):
        articles = news_data["articles"]
        
        # Format the articles to a readable string
        news_list = []
        for article in articles:
            title = article.get("title", "No title")
            description = article.get("description", "No description")
            url = article.get("url", "No URL")
            image_url = article.get("urlToImage", "No image")
            
            # Format each article for output
            news_list.append(title)
            news_list.append(description)
            news_list.append(url)
            news_list.append(image_url)
            
        return news_list
    else:
        return "No news found or an error occurred."

@tclient.request
def get_news(location):
    # Fetch news from NewsAPI, limiting to 5 results
    response = requests.get(f"https://newsapi.org/v2/everything?q={location}&apiKey=3fc7112ae7f84c2e8ec14106576d2a0f&pageSize=5")
    
    # Parse the response JSON
    news_data = response.json()
    
    # Check if the request was successful
    if news_data.get("status") == "ok" and news_data.get("articles"):
        articles = news_data["articles"]
        
        # Format the articles to a readable string
        news_list = []
        for article in articles:
            title = article.get("title", "No title")
            description = article.get("description", "No description")
            url = article.get("url", "No URL")
            image_url = article.get("urlToImage", "No image")
            if not image_url:
                image_url = "https://www.huber-online.com/daisy_website_files/_processed_/8/0/csm_no-image_d5c4ab1322.jpg"
            
            # Format each article for output
            news_list.append(title)
            news_list.append(description)
            news_list.append(url)

            try:
                response = requests.get(image_url).content
                image_data = conversion.convert_img(response, 32)
            except:
                response = requests.get("https://www.huber-online.com/daisy_website_files/_processed_/8/0/csm_no-image_d5c4ab1322.jpg").content
                image_data = conversion.convert_img(response, 32)
                
            news_list.append(str(image_data))
            
        return news_list
    else:
        return "No news found or an error occurred."

@client.request
def add_location(username, location):
    print(f"[client] Add location request received for username: {username}")
    response = oslogin.update_data("location", username, location)
    print(response)
    return response

@tclient.request
def add_location(username, location):
    print(f"[tclient] Add location request received for username: {username}")
    response = oslogin.update_data("location", username, location)
    print(response)
    return response


@client.request
def get_location(username):
    print(f"[client] Get location request received for username: {username}")
    response = oslogin.get_data("location", username)
    print(response)
    return response

@tclient.request
def get_location(username):
    print(f"[tclient] Get location request received for username: {username}")
    response = oslogin.get_data("location", username)
    print(response)
    return response

@client.request
def update_data(data, username, content):
    return oslogin.update_data(data,username,content)

@client.request
def get_data(data, username):
    return oslogin.get_data(data, username)

@tclient.request
def update_data(data, username, content):
    return oslogin.update_data(data,username,content)

@tclient.request
def get_data(data, username):
    return oslogin.get_data(data, username)

@client.request
def get_team_id(query):
    response = requests.get(f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={query}").json()
    return response["teams"][0]["idTeam"]

@client.request
def get_sports_data(team_id):
    response = requests.get(f"https://www.thesportsdb.com/api/v1/json/3/eventslast.php?id={team_id}").json()
    to_return = []
    for i in range(5):
        event = response["results"][i]
        to_return.append(event["strEvent"])
        to_return.append(f"{event['intHomeScore']}-{event['intAwayScore']}")
        to_return.append(event['strTimestamp'])
        to_return.append(f"{event['strVenue']}, {event['strCountry']}")
    return to_return

@tclient.request
def get_team_id(query):
    response = requests.get(f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={query}").json()
    return response["teams"][0]["idTeam"]

@tclient.request
def get_sports_data(team_id):
    response = requests.get(f"https://www.thesportsdb.com/api/v1/json/3/eventslast.php?id={team_id}").json()
    to_return = []
    for i in range(5):
        event = response["results"][i]
        
        # Add basic event details
        to_return.append(event["strEvent"])
        to_return.append(f"{event['intHomeScore']}-{event['intAwayScore']}")
        to_return.append(event['strTimestamp'])
        to_return.append(f"{event['strVenue']}, {event['strCountry']}")
        
        # Fetch and convert home team image
        home_img_url = event["strThumb"] if event.get("strThumb") else "https://www.huber-online.com/daisy_website_files/_processed_/8/0/csm_no-image_d5c4ab1322.jpg"
        home_image_data = conversion.convert_img(requests.get(home_img_url).content, 32)
        to_return.append(f"{str(home_image_data)}")
        
        # Fetch and convert away team image
        away_img_url = event["strAwayThumb"] if event.get("strAwayThumb") else "https://www.huber-online.com/daisy_website_files/_processed_/8/0/csm_no-image_d5c4ab1322.jpg"
        away_image_data = conversion.convert_img(requests.get(away_img_url).content, 32)
        to_return.append(f"{str(away_image_data)}")
    
    return to_return
    


client.start(thread=True)
tclient.start(thread=True)
