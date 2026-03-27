import json
import urllib.request
import urllib.parse
import time
import os

# 225 Destinations of a Lifetime
natgeo_225 = [
    # Top 50 Iconic World Wonders
    "Machu Picchu, Peru", "Petra, Jordan", "Angkor Wat, Cambodia", "Acropolis of Athens, Greece",
    "Colosseum, Rome, Italy", "Stonehenge, UK", "Chichen Itza, Mexico", "Taj Mahal, India",
    "Great Wall of China", "Pyramids of Giza, Egypt", "Tikal, Guatemala", "Bagan, Myanmar",
    "Easter Island, Chile", "Borobudur, Indonesia", "Pompeii, Italy", "Teotihuacan, Mexico",
    "Ephesus, Turkey", "Ayutthaya, Thailand", "Karnak Temple, Egypt", "Valley of the Kings, Egypt",
    "Volubilis, Morocco", "Persepolis, Iran", "Palenque, Mexico", "Hampi, India",
    "Ellora Caves, India", "Jerash, Jordan", "Lalibela, Ethiopia", "Mesa Verde, USA",
    "Tulum, Mexico", "Potala Palace, Tibet, China", "Alhambra, Spain", "Mont Saint-Michel, France",
    "Parthenon, Greece", "Blue Mosque, Turkey", "Hagia Sophia, Turkey", "Forbidden City, China",
    "Terracotta Army, China", "Neuschwanstein Castle, Germany", "Edinburgh Castle, UK", "Sydney Opera House, Australia",
    "Statue of Liberty, USA", "Eiffel Tower, France", "Burj Khalifa, UAE", "Golden Gate Bridge, USA",
    "Mount Rushmore, USA", "Sagrada Familia, Spain", "St. Basil's Cathedral, Russia", "Christ the Redeemer, Brazil",
    "Mount Fuji, Japan", "Moai Statues, Easter Island",

    # World's Greatest Cities
    "Paris, France", "London, UK", "New York City, USA", "Tokyo, Japan", "Kyoto, Japan",
    "Rome, Italy", "Venice, Italy", "Florence, Italy", "Barcelona, Spain", "Madrid, Spain",
    "Istanbul, Turkey", "Jerusalem, Israel", "Dubai, UAE", "Cape Town, South Africa", "Rio de Janeiro, Brazil",
    "Buenos Aires, Argentina", "Sydney, Australia", "Melbourne, Australia", "Hong Kong, China", "Singapore",
    "Seoul, South Korea", "Berlin, Germany", "Vienna, Austria", "Prague, Czechia", "Budapest, Hungary",
    "St. Petersburg, Russia", "Amsterdam, Netherlands", "Lisbon, Portugal", "San Francisco, USA", "Chicago, USA",
    "Vancouver, Canada", "Montreal, Canada", "Quebec City, Canada", "Mexico City, Mexico", "Havana, Cuba",
    "Cartagena, Colombia", "Cusco, Peru", "Marrakech, Morocco", "Jaipur, India", "Varanasi, India",
    "Bangkok, Thailand", "Hanoi, Vietnam", "Luang Prabang, Laos", "Kathmandu, Nepal", "Lhasa, China",
    "Reykjavik, Iceland", "Stockholm, Sweden", "Copenhagen, Denmark", "Oslo, Norway", "Helsinki, Finland",

    # Wild Places & National Parks
    "Grand Canyon, USA", "Yellowstone National Park, USA", "Yosemite National Park, USA", "Zion National Park, USA",
    "Bryce Canyon, USA", "Banff National Park, Canada", "Jasper National Park, Canada", "Torres del Paine, Chile",
    "Iguazu Falls, Argentina/Brazil", "Victoria Falls, Zambia/Zimbabwe", "Niagara Falls, Canada/USA", "Angel Falls, Venezuela",
    "Amazon Rainforest, Brazil", "Galapagos Islands, Ecuador", "Serengeti National Park, Tanzania", "Masai Mara, Kenya",
    "Kruger National Park, South Africa", "Okavango Delta, Botswana", "Ngorongoro Crater, Tanzania", "Mount Kilimanjaro, Tanzania",
    "Sahara Desert, North Africa", "Namib Desert, Namibia", "Salar de Uyuni, Bolivia", "Atacama Desert, Chile",
    "Ha Long Bay, Vietnam", "Jeju Island, South Korea", "Plitvice Lakes, Croatia", "Lake Bled, Slovenia",
    "Matterhorn, Switzerland", "Mont Blanc, France/Italy", "Jungfraujoch, Switzerland", "Cliffs of Moher, Ireland",
    "Giant's Causeway, UK", "Fiordland National Park, New Zealand", "Milford Sound, New Zealand", "Great Barrier Reef, Australia",
    "Uluru, Australia", "Twelve Apostles, Australia", "Bora Bora, French Polynesia", "Maldives",
    "Seychelles", "Mauritius", "Santorini, Greece", "Capri, Italy", "Mount Everest, Nepal/China",
    "Ayers Rock, Australia", "K2, Pakistan/China", "Denali National Park, USA", "Glacier National Park, USA", "Antarctica",

    # Island Paradises & Coasts
    "Amalfi Coast, Italy", "Cinque Terre, Italy", "French Riviera, France", "Tahiti, French Polynesia", "Fiji",
    "Cook Islands", "Whitsunday Islands, Australia", "Maui, Hawaii, USA", "Kauai, Hawaii, USA", "Bali, Indonesia",
    "Phuket, Thailand", "Koh Samui, Thailand", "Langkawi, Malaysia", "Boracay, Philippines", "Palawan, Philippines",
    "Mykonos, Greece", "Crete, Greece", "Corsica, France", "Sardinia, Italy", "Sicily, Italy",
    "Mallorca, Spain", "Ibiza, Spain", "Canary Islands, Spain", "Azores, Portugal", "Madeira, Portugal",
    "Key West, USA", "Bahamas", "Turks and Caicos", "US Virgin Islands", "British Virgin Islands",
    "St. Lucia", "Barbados", "Tulum Beach, Mexico", "Galapagos Islands", "Seychelles",
    "Maldive Islands", "Raja Ampat, Indonesia", "Komodo Island, Indonesia", "Zanzibar, Tanzania", "Madagascar",
    "Faroe Islands, Denmark", "Lofoten Islands, Norway", "Svalbard, Norway", "Aitutaki, Cook Islands", "Palau",

    # Unique Landscapes & Scenic Routes
    "Antelope Canyon, USA", "Horseshoe Bend, USA", "Monument Valley, USA", "Arches National Park, USA", "Canyonlands, USA",
    "Death Valley, USA", "White Sands, USA", "Badlands National Park, USA", "Kenai Fjords, USA", "Lake Louise, Canada",
    "Moraine Lake, Canada", "Peyto Lake, Canada", "Columbia Icefield, Canada", "Bay of Fundy, Canada", "Gros Morne, Canada",
    "Vatnajokull, Iceland", "Blue Lagoon, Iceland", "Geysir, Iceland", "Gullfoss, Iceland", "Skogafoss, Iceland",
    "Reynisfjara, Iceland", "Jokulsarlon, Iceland", "Geirangerfjord, Norway", "Trolltunga, Norway", "Preikestolen, Norway",
    "North Cape, Norway", "Lake Como, Italy", "Lake Garda, Italy", "Dolomites, Italy", "Tuscany, Italy",
    "Provence, France", "Alsace, France", "Black Forest, Germany", "Rhine Valley, Germany", "Romantic Road, Germany",
    "Hallstatt, Austria", "Salzburg, Austria", "Grossglockner, Austria", "Swiss Alps, Switzerland", "Zermatt, Switzerland"
]

def geocode(place_name):
    # Use Photon API (based on OSM)
    url = f"https://photon.komoot.io/api/?q={urllib.parse.quote(place_name)}&limit=1"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'China5A-Tracker/2.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if "features" in data and len(data["features"]) > 0:
                coords = data["features"][0]["geometry"]["coordinates"]
                props = data["features"][0]["properties"]
                name = props.get("name", place_name)
                country = props.get("country", "")
                display = f"{name}, {country}" if country else name
                return {
                    "lat": float(coords[1]),
                    "lng": float(coords[0]),
                    "display_name": display
                }
    except Exception as e:
        print(f"Error geocoding {place_name}: {e}")
    
    return None

def generate_data(places_list, prefix):
    results = []
    for i, place in enumerate(places_list):
        print(f"Geocoding [{i+1}/{len(places_list)}]: {place}")
        geo = geocode(place)
        
        item = {
            "id": f"{prefix}_{i+1}",
            "name": place,
            "category": prefix,
            "location": geo["display_name"] if geo else place,
            "lat": geo["lat"] if geo else 0.0,
            "lng": geo["lng"] if geo else 0.0,
            "image": f"https://placehold.co/600x400?text={urllib.parse.quote(place)}"
        }
        results.append(item)
        time.sleep(0.1)
        
    return results

if __name__ == "__main__":
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    print("--- Generating NatGeo Destinations 225 ---")
    data_225 = generate_data(natgeo_225, "natgeo_225")
    
    output_path = os.path.join(data_dir, 'natgeo_225.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data_225, f, ensure_ascii=False, indent=2)
        
    print(f"\\nData generation complete! {len(data_225)} places saved to {output_path}")
