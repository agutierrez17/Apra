import urllib.parse
import json
import WaApi
import pyodbc
from time import sleep

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

# Query IDs of recently-unsubscribed contacts
cursor.execute("""SELECT DISTINCT [Contact ID], [Note] FROM [APRA-IL].[dbo].[ContactsForUnsubscribe]""")
contact_ids = cursor.fetchall()

# Loop through IDs and update communication preferences
print('Looping through contacts...')
print('')
for contact in contact_ids:
    contact_id = contact[0]
    note = contact[1]
    
    data = {
    'Id': str(contact_id),
    'FieldValues': [{'FieldName': 'Event announcements', 'SystemCode': 'ReceiveEventReminders','Value': 'False'},{'FieldName': 'Member emails and newsletters', 'SystemCode': 'ReceiveNewsletters','Value': 'False'},{'FieldName': 'Notes', 'SystemCode': 'Notes','Value': note}]
    }

    url = "/v2/accounts/" + str(AccountID) + "/contacts/" + str(contact_id)
    print(url)

    try:
        response = api.execute_request(url, api_request_object=data, method = "PUT")

        # Run procedure to update entry in table
        cursor.execute("""EXEC [dbo].[Update_Unsubscribed_Contacts] '%s'""" % (contact_id))
        cursor.commit()
    except Exception as e:
        print(e)
        pass

# Re-run contact values pivot table procedure
cursor.execute("""EXEC [dbo].[Pivot_Contact_Fields]""")
cursor.commit()

print('All contacts unsubscribed')
cursor.close()
conn.close()

