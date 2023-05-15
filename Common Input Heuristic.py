import os
import pandas as pd
import requests
import sys

api_key = ""
ransomware_name = ""

df = pd.DataFrame(columns=['address'])  # create pandas dataframe

directory = f"{ransomware_name}/"  # read plain text hashes within files in working directory
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        seed_address = filename[:-4]
        with open(os.path.join(directory, filename), "r") as f:
            transaction_hashes = f.read().splitlines()

        for transaction_hash in transaction_hashes:  # make a hash-type API request to blockchair
            url = f"https://api.blockchair.com/bitcoin/dashboards/transaction/{transaction_hash}?key={api_key}"
            response = requests.get(url)

            input_addresses = []
            address_list = []

            data = response.json()
            inputs = data['data'][transaction_hash]['inputs']  # populate inputs with parsed json response


            if len(data['data'][transaction_hash]['inputs']) > 1:  # if there is more than one input parsed from reponse
                input_addresses = [input['recipient'] for input in data['data'][transaction_hash]['inputs']]
                if seed_address in input_addresses:  # check if the address already known is among inputs
                    input_addresses = [address for address in input_addresses if address != seed_address]  # remove seed address from inputs
                    address_list = input_addresses
                    print(f"Found {seed_address} for the transaction {transaction_hash}")  # add any address left after removing seed address to dataframe
                    for address in address_list:
                        new_row = {'address': address}
                        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                else:
                    print(f"Not found {seed_address} in inputs for {transaction_hash}.")

            else:
                print(f"Only one input in {transaction_hash}.")  # move on if only one input is present

        output_dir = f"{ransomware_name}/cospend"  # output into different directory
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)  # create output directory if it doesn't exist

        for index, row in df.iterrows():
            filename = row['address']  # name column after address retrieved from plain text filename
            file_path = os.path.join(output_dir, f'{filename}.txt')  # construct new directory file path
            with open(file_path, 'w') as f:  #  create empty plain text files bearing the co-spending addresses as name
                f.write('')