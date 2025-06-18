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

#### Create function for payment allocation types ####
def get_allocs(PaymentId):
    alloc_list = []
    params = {'PaymentId': int(PaymentId)}

    # Build URL
    url = "/v2/accounts/" + str(AccountID) + "/paymentAllocations?" + urllib.parse.urlencode(params)

    # Run GET request
    allocs = api.execute_request(url)

    # Loop
    for alloc in allocs:
        try:
            AllocId = alloc.Id
        except Exception as e:
            AllocId = None

        try:
            InvoiceId = alloc.Invoice.Id
        except Exception as e:
            InvoiceId = None

        try:
            InvoiceNumber = alloc.InvoiceNumber
        except Exception as e:
            InvoiceNumber = None

        try:
            PaymentId = alloc.Payment.Id
        except Exception as e:
            PaymentId = None

        try:
            PaymentType = alloc.PaymentType
        except Exception as e:
            PaymentType = None

        try:
            PaymentValue = alloc.Value
        except Exception as e:
            PaymentValue = None

        alloc_row = (AllocId,InvoiceId,InvoiceNumber,PaymentId,PaymentType,PaymentValue)
        alloc_list.append(alloc_row)
        
    return alloc_list

##########################################
#### Get list of all finance invoices ####
print('Retrieving list of all finance invoices...')
rows = []

# Get date of most recent invoice for parameter
cursor.execute("""SELECT MAX(CONVERT(DATE,[Created Date])) FROM Invoices""")
last_invoice = cursor.fetchone()[0]
print('Most recent invoice was dated ' + str(last_invoice))
date_param = last_invoice + timedelta(days=1)
params = {'startDate': date_param}

# Build URL
url = "/v2/accounts/" + str(AccountID) + "/invoices?" + urllib.parse.urlencode(params)
print(url)
print('')

# Run GET request
invoices = api.execute_request(url)

# Loop through all fields and pull down metadata
print('Looping through all invoices...')
print('')
for invoice in invoices:
    try:
        InvoiceID = invoice.Id
    except Exception as e:
        InvoiceID = None

    try:
        Value = invoice.Value
    except Exception as e:
        Value = None

    try:
        IsPaid = invoice.IsPaid
    except Exception as e:
        IsPaid = None

    try:
        PaidAmount = invoice.PaidAmount
    except Exception as e:
        PaidAmount = None

    try:
        ContactID = invoice.Contact.Id
    except Exception as e:
        ContactID = None

    try:
        CreatedBy = invoice.CreatedBy.Id
    except Exception as e:
        CreatedBy = None

    try:
        CreatedDate = invoice.CreatedDate
    except Exception as e:
        CreatedDate = None

    try:
        DocumentDate = invoice.DocumentDate
    except Exception as e:
        DocumentDate = None

    try:
        DocumentNumber = invoice.DocumentNumber
    except Exception as e:
        DocumentNumber = None

    try:
        OrderType = invoice.OrderType
    except Exception as e:
        OrderType = None

    try:
        Memo = invoice.Memo
    except Exception as e:
        Memo = None

    try:
        UpdatedBy = invoice.UpdatedBy.Id
    except Exception as e:
        UpdatedBy = None

    try:
        UpdatedDate = invoice.UpdatedDate
    except Exception as e:
        UpdatedDate = None

    try:
        Url = invoice.Url
    except Exception as e:
        Url = None
    
    row = (InvoiceID,Value,IsPaid,PaidAmount,ContactID,CreatedBy,CreatedDate,DocumentDate,DocumentNumber,OrderType,Memo,UpdatedBy,UpdatedDate,Url)
    rows.append(row)

# INSERT DATA INTO INVOICES TABLE
print('Inserting data into Invoices table...')
if rows:
    cursor.executemany("""
    INSERT INTO [dbo].[Invoices] ([Invoice ID],[Value],[Is Paid],[Paid Amount],[Contact ID],[Created By],[Created Date],[Document Date],[Document Number],[Order Type],[Memo],[Updated By],[Updated Date],[Url])
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", rows)
    cursor.commit()
sleep(1)

print('All invoice data inserted')
print('')


##########################################
#### Get list of all finance payments ####
print('Retrieving list of all finance payments...')
rows, alloclist = [], []

# Get date of most recent payment for parameter
cursor.execute("""SELECT MAX(CONVERT(DATE,[Created Date])) FROM Payments""")
last_payment = cursor.fetchone()[0]
print('Most recent payment was dated ' + str(last_payment))
date_param = last_payment + timedelta(days=1)
params = {'startDate': date_param}

# Build URL
url = "/v2/accounts/" + str(AccountID) + "/payments?" + urllib.parse.urlencode(params)
print(url)
print('')

# Run GET request
payments = api.execute_request(url)

# Loop through all fields and pull down metadata
print('Looping through all payments...')
print('')
for payment in payments:
    try:
        PaymentID = payment.Id
    except Exception as e:
        PaymentID = None

    try:
        Value = payment.Value
    except Exception as e:
        Value = None

    try:
        AllocatedValue = payment.AllocatedValue
    except Exception as e:
        AllocatedValue = None

    try:
        PaymentType = payment.Type
    except Exception as e:
        PaymentType = None

    try:
        ContactID = payment.Contact.Id
    except Exception as e:
        ContactID = None

    try:
        TenderID = payment.Tender.Id
    except Exception as e:
        TenderID = None

    try:
        CreatedBy = payment.CreatedBy.Id
    except Exception as e:
        CreatedBy = None

    try:
        CreatedDate = payment.CreatedDate
    except Exception as e:
        CreatedDate = None

    try:
        Comment = payment.Comment
    except Exception as e:
        Comment = None

    try:
        RefundedAmount = payment.RefundedAmount
    except Exception as e:
        RefundedAmount = None

    try:
        UpdatedBy = payment.UpdatedBy.Id
    except Exception as e:
        UpdatedBy = None

    try:
        UpdatedDate = payment.UpdatedDate
    except Exception as e:
        UpdatedDate = None

    try:
        DocumentDate = payment.DocumentDate
    except Exception as e:
        DocumentDate = None

    try:
        Url = payment.Url
    except Exception as e:
        Url = None

    # Payment allocations
    alloclist = alloclist + get_allocs(PaymentID)
    
    row = (PaymentID,Value,AllocatedValue,PaymentType,ContactID,TenderID,CreatedBy,CreatedDate,Comment,RefundedAmount,UpdatedBy,UpdatedDate,DocumentDate,Url)
    rows.append(row)

# INSERT DATA INTO PAYMENTS TABLE
print('Inserting data into Payments table...')
if rows:
    cursor.executemany("""
    INSERT INTO [dbo].[Payments] ([Payment ID],[Value],[Allocated Value],[Payment Type],[Contact ID],[Tender ID],[Created By],[Created Date],[Comment],[Refunded Amount],[Updated By],[Updated Date],[Document Date],[Url])
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", rows)
    cursor.commit()
sleep(1)

print('All payments data inserted')
print('')

# INSERT DATA INTO PAYMENT ALLOCATIONS TABLE
print('Inserting data into Payment Allocations table...')
if alloclist:
    cursor.executemany("""INSERT INTO [dbo].[PaymentAllocations] ([Allocation ID],[Invoice ID],[Invoice Number],[Payment ID],[Payment Type],[Payment Value]) VALUES (?,?,?,?,?,?)""", alloclist)
    cursor.commit()
sleep(1)

print('All payment allocations inserted')
print('')


###############################################
#### Get list of all finance refunds ####
print('Retrieving list of all finance refunds...')
rows = []

# Get date of most recent refund for parameter
cursor.execute("""SELECT MAX(CONVERT(DATE,[Created Date])) FROM Refunds""")
last_refund = cursor.fetchone()[0]
print('Most recent refund was dated ' + str(last_refund))
date_param = last_refund + timedelta(days=1)
params = {'startDate': date_param}

# Build URL
url = "/v2/accounts/" + str(AccountID) + "/refunds?" + urllib.parse.urlencode(params)
print(url)
print('')

# Run GET request
refunds = api.execute_request(url)

# Loop through all fields and pull down metadata
print('Looping through all refunds...')
print('')
for refund in refunds:
    try:
        RefundID = refund.Id
    except Exception as e:
        RefundID = None

    try:
        Value = refund.Value
    except Exception as e:
        Value = None

    try:
        SettledValue = refund.SettledValue
    except Exception as e:
        SettledValue = None

    try:
        ContactID = refund.Contact.Id
    except Exception as e:
        ContactID = None

    try:
        TenderID = refund.Tender.Id
    except Exception as e:
        TenderID = None

    try:
        CreatedBy = refund.CreatedBy.Id
    except Exception as e:
        CreatedBy = None

    try:
        CreatedDate = refund.CreatedDate
    except Exception as e:
        CreatedDate = None

    try:
        Comment = refund.Comment
    except Exception as e:
        Comment = None

    try:
        PublicComment = refund.PublicComment
    except Exception as e:
        PublicComment = None

    try:
        UpdatedBy = refund.UpdatedBy.Id
    except Exception as e:
        UpdatedBy = None

    try:
        UpdatedDate = refund.UpdatedDate
    except Exception as e:
        UpdatedDate = None

    try:
        DocumentDate = refund.DocumentDate
    except Exception as e:
        DocumentDate = None

    try:
        Url = refund.Url
    except Exception as e:
        Url = None
    
    row = (RefundID,Value,SettledValue,ContactID,TenderID,CreatedBy,CreatedDate,Comment,PublicComment,UpdatedBy,UpdatedDate,DocumentDate,Url)
    rows.append(row)

# INSERT DATA INTO REFUNDS TABLE
print('Inserting data into Refunds table...')
if rows:
    cursor.executemany("""
    INSERT INTO [dbo].[Refunds] ([Refund ID],[Value],[Settled Value],[Contact ID],[Tender ID],[Created By],[Created Date],[Comment],[Public Comment],[Updated By],[Updated Date],[Document Date],[Url])
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", rows)
    cursor.commit()
sleep(1)

print('All refunds data inserted')
print('')


###############################################
#### Get list of all finance tenders ####
print('Retrieving list of all finance tenders...')
rows = []

# Build URL
url = "/v2/accounts/" + str(AccountID) + "/tenders"
print(url)
print('')

# Run GET request
tenders = api.execute_request(url)

# Loop through all fields and pull down metadata
print('Looping through all tenders...')
print('')
for tender in tenders:
    try:
        TenderID = tender.Id
    except Exception as e:
        TenderID = None

    try:
        Name = tender.Name
    except Exception as e:
        Name = None

    try:
        IsCustom = tender.IsCustom
    except Exception as e:
        IsCustom = None

    try:
        Url = tender.Url
    except Exception as e:
        Url = None
    
    row = (TenderID,Name,IsCustom,Url)
    rows.append(row)

# INSERT DATA INTO TENDERS TABLE
cursor.execute("""TRUNCATE TABLE [dbo].[Tenders]""")
cursor.commit()

print('Inserting data into Tenders table...')
if rows:
    cursor.executemany("""
    INSERT INTO [dbo].[Tenders] ([Tender ID],[Name],[Is Custom],[Url])
        VALUES (?,?,?,?)""", rows)
    cursor.commit()
sleep(1)

print('All tender data inserted')
print('')

cursor.close()
conn.close()
