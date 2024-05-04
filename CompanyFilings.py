from pandarallel import pandarallel
from sec_api import QueryApi
import pandas as pd
API_KEY = '3502f92a9f18ebf54f3fcc7c779fe15a21c909c6c1246ebb388890c6c4fa29cc'
# Instantiate QueryApi
queryApi = QueryApi(API_KEY)

def get_filings(query):
    from_param = 0
    size_param = 200
    all_filings = []

    while True:
        query['from'] = from_param
        query['size'] = size_param

        response = queryApi.get_filings(query)  # Use query instead of search_query
        filings = response['filings']

        if len(filings) == 0:
            break

        all_filings.extend(filings)

        from_param += size_param

    return pd.json_normalize(all_filings)

form_type_query = 'formType:("10-K") AND NOT formType:("10-K/A", NT)'
ticker_query = 'ticker:(MSFT, TSLA)'
date_range_query = 'filedAt:[1995-01-01 TO 2023-12-31]'

lucene_query = f"{form_type_query} AND {ticker_query} AND {date_range_query}"

search_query = {
    "query": lucene_query,
    "from": "0",
    "size": "200",
    "sort": [{"filedAt": {"order": "desc"}}]
}

filings = get_filings(search_query)
#print(filings.head())

urls = filings[['ticker', 
                'formType', 
                'periodOfReport',
                'filedAt', 
                'linkToFilingDetails']].rename(columns={'linkToFilingDetails': 'filingUrl'})

urls['financialReportsUrl'] = urls['filingUrl'].apply(lambda url: '/'.join(url.split('/')[:-1]) + '/Financial_Report.xlsx')

#print(urls.head(10))
import os, requests

folder_path = './reports'

if not os.path.exists(folder_path):
  os.makedirs(folder_path)


def download_report(filing):
  reports_path = filing['financialReportsUrl'].replace('https://www.sec.gov/Archives/edgar/data/', '')
  base_url = 'https://archive.sec-api.io/' + reports_path
  render_api_url = base_url + '?token=' + API_KEY

  response = requests.get(render_api_url)

  file_name = f"{filing['ticker']}-{filing['periodOfReport']}-{filing['formType']}.xlsx"
  file_path = f"{folder_path}/{file_name}"

  output = open(file_path, 'wb')
  output.write(response.content)
  output.close()
  
number_of_workers = 4
pandarallel.initialize(progress_bar=True, nb_workers=number_of_workers, verbose=0)
urls.parallel_apply(download_report, axis=1)
print(f"✅ Downloaded {len(urls)} reports")
