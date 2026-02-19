import urllib.parse
import json
import WaApi
import pyodbc
from time import sleep
from datetime import timedelta

##### Link to Wild Apricot API Documentation: https://app.swaggerhub.com/apis-docs/WildApricot/wild-apricot_public_api/7.24.0#/Accounts/GetAccountsList
##### Link to obtain application credentials: https://help.wildapricot.com/display/DOC/API+V2+authentication#APIV2authentication-Authorizingyourapplication

# Connect to database and open SQL cursor
print('Connecting to database...')
print('')
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

#### Authenticate API Connection ####
print('Authenticating administrator account...')
print('')
accounts = api.execute_request("/v2/accounts")
account = accounts[0]
AccountID = account.Id

print('Successfully logged in to: ' + account.PrimaryDomainName)
print('Account ID: ' + str(AccountID))
print('')

# Get unpaid invoices from prior years
cursor.execute("""
SELECT 
[Invoice ID]
FROM [APRA-IL].[dbo].[Invoices] I
LEFT OUTER JOIN [dbo].[APRA-IL_Contacts] C ON I.[Contact ID] = C.[Contact ID]

WHERE
[Created Date] <= '2025-12-31'
AND
[Is Paid] = 0

ORDER BY
[Created Date] DESC
""")
data = cursor.fetchall()

# Get date of most recent invoice for parameter
for invoice in data:
    InvoiceID = invoice[0]
    print(InvoiceID)
    params = {'invoiceId': InvoiceID}

    # Build URL
    url = "/v2/rpc/" + str(AccountID) + "/VoidInvoice?" + urllib.parse.urlencode(params)
    print(url)
    api.execute_request(url, method = "POST")

print('All invoices voided')
print('')

cursor.close()
conn.close()
