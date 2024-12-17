import requests

# Your SEMrush API key
api_key = '21f348341b7344c701b27e540f06a6ea'

# List of website URLs
websites = [
    'techinblog.org', 'hackerella.com', 'albumsthatrock.com', 'digitalblogs.co.uk', 'manapaisa.org',
    'viralreel.org', 'cyber-180.com', 'heavenclick.com', 'newsjotechgeek.com', 'intechpro.co.uk'
]  # Replace with your list of websites

# SEMrush API endpoint for Domain Overview
url = "https://api.semrush.com/"

# Function to get website traffic and authority score data
def get_traffic_and_as_data(website):
    params = {
        'type': 'domain_ranks',  # Type of report: domain overview
        'key': api_key,
        'domain': website,
        'database': 'us',  # Database for US, can change to other regions like 'uk' for the UK
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.text
        return data
    else:
        return f"Error fetching data for {website}: {response.status_code}"

# Function to parse traffic and Authority Score (AS)
def parse_traffic_and_as_data(raw_data):
    # Split the data by newline and skip the first row (headers)
    lines = raw_data.strip().split("\n")[1:]
    
    result = []
    for line in lines:
        columns = line.split(";")
        domain = columns[1]
        authority_score = columns[3]
        organic_traffic = columns[4]
        
        # Append the desired values (Authority Score and Organic Traffic)
        result.append(f"{domain}: AS = {authority_score}, Organic Traffic = {organic_traffic}")
    
    return result

# Create and open the output text file
with open('traffic_and_as.txt', 'w') as file:
    # Iterate through the list of websites
    for website in websites:
        traffic_as_info = get_traffic_and_as_data(website)
        
        # If data is valid, parse and save it
        if "Error" not in traffic_as_info:
            parsed_data = parse_traffic_and_as_data(traffic_as_info)
            for entry in parsed_data:
                print(entry)  # Print to terminal
                file.write(entry + "\n")  # Write to text file
        else:
            print(traffic_as_info)
            file.write(traffic_as_info + "\n")
