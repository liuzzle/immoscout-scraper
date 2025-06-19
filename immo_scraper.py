import json
import time
import random

# Base URL with filters applied
base_url = "https://www.immoscout24.ch/en/real-estate/rent/postcode-8003-zuerich?r=5000&nrf=4.5&pty=1%2C55%2C62%2C92&an=400&pt=8000"

# Headers to simulate a browser visit
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
def extract_apartment_data(soup):
    apartments = []
    listings = soup.find_all("div", class_="HgListingCard_info_RKrwz") 

    for listing in listings:
        try:
            rooms_size_price = listing.find("div", class_="HgListingRoomsLivingSpacePrice_roomsLivingSpacePrice_M6Ktp")
            
            if not rooms_size_price:
                continue
            
            strong_tags = rooms_size_price.find_all("strong")
            
            rooms = rooms_size_price.find("strong").text.strip() if len(strong_tags)> 0 else "N/A"
            size = rooms_size_price.find_all("strong")[1].text.strip() if len(strong_tags)> 1 else "N/A"
            
            price_tag = rooms_size_price.find("span", class_="HgListingRoomsLivingSpacePrice_price_u9Vee")
            price = price_tag.text.strip() if price_tag else "N/A"

            address_info = listing.find_all('div', class_='HgListingCard_address_JGiFv')[0]
            address = address_info.address.contents[0].strip() if address_info else "N/A"
            
            description_tag = listing.find("p", class_="HgListingDescription_title_NAAxy")
            description_text = description_tag.find("span").text.strip() if description_tag else "No description available"

            # Extract apartment link 
            listing_url = soup.find('a', {'class': 'HgCardElevated_link_EHfr7'})['href']
            link = f"https://www.immoscout24.ch/{listing_url}"
            
            # Store data in dictionary
            apartments.append({
                "rooms": rooms,
                "size": size,
                "price": price,
                "address": address,
                "description": description_text,
                "link": link
            })
            
        except Exception as e:
            print(f"Skipping a listing due to error: {e}")
            continue  # Skip listing if some details are missing

    return apartments

def scrape_immoscout(base_url):
    all_apartments = []
    page = 1

    while True:  # Keep paging until no more listings
        url = f"{base_url}&pn={page}"
        print(f"Scraping page {page}: {url}")

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch page {page}, status code: {response.status_code}") 
            #always check status code -> sometimes too many requests - then get a 429 error
            break

        soup = BeautifulSoup(response.text, "html.parser")
        apartments = extract_apartment_data(soup)

        if not apartments:  # Stop if no listings are found
            print("No more listings found. Stopping...")
            break

        for apartment in apartments:
            travel_times = extract_travel_times(apartment['link'])
            apartment['travel_times'] = travel_times

        all_apartments.extend(apartments)
        page += 1

        time.sleep(random.uniform(2, 5))  # Prevent rate limiting

    return all_apartments

def extract_travel_times(apartment_url):
    response = requests.get(apartment_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    travel_times = []
    
    travel_time_sections = soup.find_all("div", class_="TravelTime_travelTime_GZ1su")
    for section in travel_time_sections:
        locations = section.find_all("li", class_="TravelTime_travelTimePoiData_GN7yR")
        for location in locations:
            place = location.find("h4").get_text(strip=True) if location.find("h4") else "Unknown"
            time = location.find("span", class_="TravelTime_travelTimeListTime_SUflX").get_text(strip=True) if location.find("span", class_="TravelTime_travelTimeListTime_SUflX") else "Unknown"
            travel_times.append({"place": place, "time": time})
    
    return travel_times

scraped_data = scrape_immoscout(base_url) 
print(scraped_data)

# Save data to a JSON file
with open("immoscout_apartments.json", "w", encoding="utf-8") as file:
   json.dump(scraped_data, file, indent=4, ensure_ascii=False)
   
len(scraped_data)