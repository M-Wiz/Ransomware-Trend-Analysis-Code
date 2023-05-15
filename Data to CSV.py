import os
import pandas as pd
import requests

api_key = ""
ransomware_name = ""
csv_file = f"{ransomware_name}.csv"

df = pd.DataFrame(columns=['Value (BTC)', 'Value (USD)', 'Date', 'Recipient', 'Time']) # create pandas dataframe

directory = f"{ransomware_name}/"  # working directory changes depending on ransomware name
filenames = [f for f in os.listdir(directory) if f.endswith(".txt")]


for filename in filenames:  # loop through text files in working directory
    recipient_address = filename[:-4]
    with open(os.path.join(directory, filename), "r") as f:
        transaction_hashes = f.read().splitlines()

    for transaction_hash in transaction_hashes:  # loop through transaction hashes in plain text files
        url = f"https://api.blockchair.com/bitcoin/dashboards/transaction/{transaction_hash}?key={api_key}"
        response = requests.get(url)

        # create some empty lists
        value_list = []
        valueusd_list = []
        date_list = []
        time_list = []
        address_list = []
        ransomware_list = []

        data = response.json() # populate data with raw json response
        inputs = data['data'][transaction_hash]['inputs']  # parse inputs from json response
        outputs = data['data'][transaction_hash]['outputs']  # parse outputs from json response


        input_addresses = [input_['recipient'] for input_ in inputs]  # skip any transactions found coming from within our known address set
        if any(address in input_addresses for address in filenames):
            continue

        for output in outputs:  #  collect data about incoming transaction to our address
            if output['recipient'] == recipient_address:
                btc_value = output['value'] / 100000000
                usd_value = output['value_usd']
                date = output['date']
                time = output['time']
                recipient_value = output['recipient']
                # store in dataframe
                new_row = {'Value (BTC)': btc_value, 'Value (USD)': usd_value, 'Date': date, 'Time': time,
                           'Recipient': recipient_value, 'Name': ransomware_name, 'Hash': transaction_hash}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

df.to_csv(csv_file, index=False)  # export final dataframe to csv
print(f"{ransomware_name} saved as CSV")
