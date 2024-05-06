## Georgia-Tech-Assignment

# Task 1.1
Downloading Data of Microsoft and Tesla
In this  Python script is designed to download financial reports (specifically Excel files) from the SEC (U.S. Securities and Exchange Commission) website for specified companies and filing types. Here's a brief overview of how it works:

Query Generation: The script constructs a Lucene query combining criteria such as form type (10-K), ticker symbols (e.g., MSFT, TSLA), and a date range for filings.

Fetching Filings: It utilizes the SEC API to retrieve filings matching the constructed query. The get_filings() function loops through the results paginated by 200 filings at a time until all filings are fetched.

Data Preparation: Once filings are retrieved, relevant information like ticker, form type, period of report, filing date, and the URL to the filing details are extracted.

URL Transformation: The script modifies the filing URL to point to the financial report specifically, appending '/Financial_Report.xlsx' to the original URL.

Download Function: The download_report() function is defined to download each financial report. It constructs the URL for the financial report, makes a request to the SEC archive API, and saves the response content as an Excel file named based on ticker, period of report, and form type.

Parallel Execution: To expedite the download process, the script uses parallel processing with the pandarallel library. It initializes parallel execution with a specified number of workers (in this case, 4) and applies the download_report() function to each row of the DataFrame concurrently.

Folder Management: Before downloading, the script checks if a folder named 'reports' exists in the current directory. If not, it creates one to store the downloaded reports.

Progress Tracking: During execution, the script displays a progress bar indicating the status of the download process.

Completion Message: Once all reports are downloaded, it prints a success message along with the total number of reports downloaded.


## Tech Stack Included-Python

