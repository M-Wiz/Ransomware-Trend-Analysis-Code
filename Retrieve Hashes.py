import os
import requests

api_key = ""
directory = ""  # Working directory containing plain text files
for filename in os.listdir(directory):  # count filenames
    if filename.endswith(".txt"):  # only consider plain text
        address = filename[:-4]  # retrieve wallet address from filename
        url = f"https://api.blockchair.com/bitcoin/dashboards/address/{address}?limit=10000&key={api_key}" # construct address-based API query
        response = requests.get(url)  # get request to API
        data = response.json()  #  populate data with raw json response
        transactions = data['data'][address]['transactions']  # parse response for transactions involving our address
        with open(f"{directory}/{filename}", "w") as f:  # write transaction hashes in address file
            for tx in transactions:
                f.write(f"{tx}\n")
            print(f"Successfully retrieved {len(transactions)} transaction hashes for {address}.")
