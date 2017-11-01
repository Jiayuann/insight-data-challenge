# Insight Coding Challenge : Finding political donors

## Goal

Two output files containing :

1. medianvals_by_zip.txt

Contains a calculated running median, total dollar amount and total number of contributions by recipient and zip code


2. medianvals_by_date.txt

Has the calculated median, total dollar amount and total number of contributions by recipient and date.

---

## Approach

### 1. Get Median Values by Zip code for each recipient

Each row in the input file was streamed in a sequential manner.

- Preprocessing of each row consisted of :
1. Splitting on '|' delimiter
2. Convert numeric strings such as Transaction amt to numeric type
3. Corner case checkings

- A nested dictionary was created to store ZIP_KEY and corresponding zipcode and transaction amount.
- This final data was written to a text file.
- ZIP_KEY = CMTE_ID + '_' + ZIP_CODE

### 2. Get Median Values by Date code for each recipient

All Date was preprocessed and stored as a nested dictionary.

- Preprocessing of each row consisted of :

1. Splitting on '|' delimiter
2. Convert numeric strings such as Transaction amt to numeric type
3. Corner case checkings

- A nested dictionary was created to store DATE_KEY and corresponding zipcode and transaction amount.
- This final data was written to a text file.
- DATE_KEY = CMTE_ID + '_' + TRANSACTION_DT



