# bulk-crypto-data
Customizable bulk download of market, on-chain, and alternative data from CryptoCompare, Glassnode, and CoinMetrics platforms. Basic data cleaning and feature engineering in 'Analysis' folder

# Main Data Retrieval Script

`gather_data.py`

This code is used to call various data providers for different metric types. The user is prompted to enter the name of the data provider, and then is given further options depending on the chosen data provider. 

The data providers available are `glassnode`, `coinmetrics`, and `cryptocompare`. 

For `glassnode`, the user can choose to either manually enter a metric list, automatically enter a metric list, or view a list of all metrics by entering `m`, `a`, or `all` respectively. 

For `coinmetrics`, the user has the same options as with `glassnode`. 

For `cryptocompare`, the user must choose the type of data they would like to receive, either `list`, `latest`, or `timeseries`.

The code then uses `exec` to execute the appropriate Python script for the chosen data provider and metric type, which is located at the specified file path.


# Glassnode Data Retrieval Script

`Call_Glassnode.py`

## Overview

This script retrieves cryptocurrency data from Glassnode, a blockchain data analysis platform, based on user inputs. The data can be filtered by a cryptocurrency symbol, a date range, a frequency interval, and desired metrics.

## Input Parameters

- `Digital Asset`: The base cryptocurrency symbol of interest.
- `Start date`: The start date of the desired date range, entered in the format of YYYY-MM-DD.
- `End date`: The end date of the desired date range, entered in the format of YYYY-MM-DD.
- `Interval`: The frequency interval unit length, options include 1h, 24h, 10m, 1w, 1month.
- `Metric ID`: The desired metrics, entered as a comma-separated list.
- `Currency denomination`: Optional currency denomination, e.g. USD.

## Output

The script outputs the cryptocurrency data from Glassnode based on the user inputs.

## Implementation Details

- The input dates are transformed into Unix timestamps to be used in the data retrieval process.
- The `metric_id` inputs are used to obtain relevant `data_categories` metrics.
- The script then retrieves the data using either `Glassnode_OHLC.py` or `Glassnode_Close.py` based on the frequency interval entered.
- The output data is in the format a CSV file.

## Auto and All
`Auto_Glassnode.py` and `All_Glassnode.py` work similarly to `Call_Glassnode.py` above except one is not prompted during the running of either to manually input desired metrics. Instead, with
- Auto, one hard-codes a list of desired metrics into the `Auto_Glassnode.py` script prior to running.
- All, a hardcoded list of all avaiable metrics from the Glassnode platform is requested.

# Glassnode Data Import Script

`Glassnode_OHLC.py`

## Overview

This script fetches market data from Glassnode API and processes it for analysis. The data is obtained in the form of a time series, which is processed and transformed into a Pandas dataframe.
## Import statements

This script imports the following libraries:

-Requests
-Json
-Pandas

## Variables

The following variables are defined and used in the script:

- `GLASSNODE_TOKEN`: The Glassnode API key is obtained from the config.py file and stored in this variable.
- `param_dict`: A dictionary containing the necessary `api_key` parameter, which is required to make API calls.
- `res`: A variable to store the API response.
- `df`: A variable to store the data obtained from the API response, in a Pandas dataframe format.
- `ohlc_df`: A variable to store the 'Open-High-Low-Close' data obtained from the API response, in a Pandas dataframe format.
- `glassnode_df`: A variable to store the processed data from the API response, in a Pandas dataframe format.
- `append_df`: A variable to store a working copy of the `glassnode_df` dataframe.
- `tier_endpoints`: A list containing the desired endpoints for data to be fetched from.
- `metric_ids`: A list containing the names of the metrics that need to be obtained from the Glassnode API.

## Function: tier_df

This function makes API calls to Glassnode API, obtains the desired data and processes it into a Pandas dataframe. The processed data is then appended to the `glassnode_df` dataframe.
## Function: dictionary_column_split

This function splits the columns in the `glassnode_df` dataframe that consist of a series of dictionaries, into separate columns consisting of its separate constituent elements. The columns are then renamed using the original dictionary metric name as a prefix to constituent element column names.
## Execution

The script executes the `tier_df` function for the desired `tier_endpoints` and obtains the data. The obtained data is then processed and the `dictionary_column_split` function is executed for each separate dictionary column. The processed data is then concatenated with the original `glassnode_df` dataframe. The final processed data is stored in the `glassnode_df` dataframe.

## Input

The code requires two external inputs:

- `config.py` file, containing the CryptoCompare API key, to access its variables.
- Glassnode API endpoint, which is a URL that is used to request data from Glassnode's database.

## Output

The code returns a pandas dataframe that contains the information from Glassnode's database. The resulting dataframe includes columns that consist of different crypto-metrics such as OHLC (Open-High-Low-Close) prices and ATH price drawdowns. The columns that consist of dictionary elements are transformed into separate columns that include each element of the original dictionary. The time series index of the resulting dataframe is set to the time column.
## Code flow

1. The code imports the required packages (`requests`, `json`, `pandas`) and the `config.py` file.
2. The `config.py` file is used to obtain the Glassnode API key, which is then assigned to a local variable `GLASSNODE_TOKEN`.
3. A patch is applied to avoid the 'ValueError: Value is too big' message when using the `pd.read_json` function.
4. A GET request is made to the Glassnode API endpoint to obtain the OHLC prices.
5. The response of the API request is converted into a pandas dataframe and is processed to extract the OHLC values.
6. The resulting dataframe is assigned to the `glassnode_df` variable.
7. The `tier_df` function is called for the desired crypto-metrics to obtain additional information and concatenate it to the `glassnode_df` dataframe.
8. The OHLC columns are removed from the resulting dataframe and the columns that consist of dictionary elements are transformed into separate columns.
9. The resulting dataframe is assigned to the `glassnode_df` variable.

## Close I/O OHLC
The `Glassnode_Close.py` script works similarly to `Glassnode_OHLC.py`, except it only imports closing price data instead of OHLC data.

# Miscelaneous File
The script `glassnode_data_cat_from_sub_cat.py` is run by `Call_Glassnode.py`, `Auto_Glassnode.py`, and `All_Glassnode.py`.

This code imports the Pandas library and uses it to read data from two sheets ('T1' & 'T2') in an excel file ('Glassnode_Metrics.xlsx') located at the specified 'excel_link'. The two sheets are stored as separate Pandas dataframes ('glassnode_T1' & 'glassnode_T2') and then concatenated into a single dataframe ('df'). Finally, the code creates a list of 'data_category' values for given 'metric_id' values by using a lambda function and filtering the 'df' dataframe.

Note: The variable 'metric_ids' is not defined in this code and is instead devined and provided via `Call_Glassnode.py`, `Auto_Glassnode.py`, or `All_Glassnode.py`.

# Update
Documentation for code contained within 'CryptoCompare' and 'CoinMetrics' folders, as well as files contained within the 'Analysis' folder is forthcoming. In the meantime, please see `Cryptocurrency_Market_and_On-Chain_Data.pptx` file for a broad overview of inputs and outputs in the bulk data retrieval, cleaning, and feature engineering processes.
