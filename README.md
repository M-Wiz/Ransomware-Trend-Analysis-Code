# Trend Analysis on Bitcoin Ransomware Transactions
**BSc Digital Forensics and Cyber Security — TU Dublin**  
Davide Russo · Mudassar Ali · Majdi Ben Tej  
*Supervised by Dr. Stephen O'Shaughnessy*

![Python](https://img.shields.io/badge/Python-3.x-blue) ![API](https://img.shields.io/badge/API-Blockchair-orange) ![Families](https://img.shields.io/badge/Ransomware_Families-20-red)

## Overview

This project analyses Bitcoin transactions associated with ransomware campaigns using the **merged input (common input ownership) heuristic** — when multiple addresses co-spend as inputs in a single transaction, they are likely controlled by the same entity. Starting from known seed addresses, the pipeline clusters co-spending addresses belonging to the same ransomware operator, extracts incoming payment data, and exports it for analysis. Applied across 20 ransomware families, the dataset identifies over **$107 million USD** in ransom payments between 2015 and 2022.

## Ransomware families covered

Ako, AlbDecryptor, Bagli, ChupaCabra, Conti, Cuba, Deadbolt, Egregor, Flyper, Lambdalocker, Lockbit, Locky, Medusalocker, Netwalker, NotPetya, Qlocker, Qweuirtksd, Samsam, SynAck, WannaCry

## Pipeline

```
Seed addresses (sourced from public threat intel)
        ↓
Retrieve Hashes.py        ← fetches all tx hashes per address via Blockchair API
        ↓
Common Input Heuristic.py ← finds co-spending addresses, expands cluster iteratively
        ↓
Data to CSV.py            ← filters internal txs, exports payment data to CSV
```

## Scripts

**`Retrieve Hashes.py`** — reads a directory of `.txt` files named after known Bitcoin addresses and writes all associated transaction hashes into each file via the Blockchair API.

**`Common Input Heuristic.py`** — for each transaction, checks whether the seed address co-appears as an input alongside others. New addresses are saved to a `cospend/` subdirectory for the next iteration.

**`Data to CSV.py`** — parses all cluster addresses for incoming payments, filters out intra-cluster movements, and exports BTC value, USD value, date, time, and recipient to a CSV file.

## Usage

Set your Blockchair API key and ransomware family name at the top of each script:

```python
api_key = "your_key_here"
ransomware_name = "ransomware_family_name"
```

Then run in order:

```bash
python "Retrieve Hashes.py"
python "Common Input Heuristic.py"   # repeat until no new addresses are found
python "Data to CSV.py"
```

## Directory structure

```
ransomware_name/
  <address>.txt       ← transaction hashes per address
  cospend/
    <address>.txt     ← co-spending addresses found by heuristic
ransomware_name.csv   ← final payment dataset
```

## Dependencies

```bash
pip install pandas requests
```

Requires a [Blockchair API key](https://blockchair.com/api).

## Dataset

The seed address dataset is included in this repository, sourced from publicly available threat intelligence. All USD values use historical BTC/USD conversion rates.
