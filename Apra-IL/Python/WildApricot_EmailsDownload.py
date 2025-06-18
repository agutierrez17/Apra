import urllib.parse
import json
import WaApi
import pyodbc
from time import sleep
from datetime import timedelta

##### Link to Wild Apricot API Documentation: https://app.swaggerhub.com/apis-docs/WildApricot/wild-apricot_public_api/7.24.0#/Accounts/GetAccountsList
##### Link to obtain application credentials: https://help.wildapricot.com/display/DOC/API+V2+authentication#APIV2authentication-Authorizingyourapplication

#### Create function for event registration types ####
def get_email_recips(EmailID):
    recips, links = [], []
    params = {'emailId': EmailID, 'LoadLinks': 'True'}
    url = "/v2/accounts/" + str(AccountID) + "/SentEmailRecipients?" + urllib.parse.urlencode(params)
    email_recips = api.execute_request(url)

    for recip in email_recips.Recipients:
        try:
            ContactID = recip.ContactId
        except Exception as e:
            ContactID = None

        try:
            EventRegistrationId = recip.EventRegistrationId
        except Exception as e:
            EventRegistrationId = None

        try:
            RecipientName = recip.RecipientName
        except Exception as e:
            RecipientName = None

        try:
            LastName = recip.LastName
        except Exception as e:
            LastName = None

        try:
            FirstName = recip.FirstName
        except Exception as e:
            FirstName = None

        try:
            Email = recip.Email
        except Exception as e:
            Email = None

        try:
            Organization = recip.Organization
        except Exception as e:
            Organization = None

        try:
            IsDelivered = recip.IsDelivered
        except Exception as e:
            IsDelivered = None

        try:
            IsOpened = recip.IsOpened
        except Exception as e:
            IsOpened = None

        try:
            for link in recip.ClickedLinks:
                try:
                    Url = link.Url
                except Exception as e:
                    Url = None

                try:
                    Clicked = link.Clicked
                except Exception as e:
                    Clicked = None

                try:
                    ClicksCount = link.ClicksCount
                except Exception as e:
                    ClicksCount = None
                
                linkrow =(ContactID,EmailID,Url,Clicked,ClicksCount)
                links.append(linkrow)
        except Exception as e:
            pass

        row = (EmailID,ContactID,EventRegistrationId,RecipientName,LastName,FirstName,Email,Organization,IsDelivered,IsOpened)
        recips.append(row)
        
    return recips, links

# Connect to database and open SQL cursor
print('Connecting to database...')
print('')
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

# Delete recent emails before pulling down fresh data
cursor.execute("""EXEC [dbo].[Delete_Recent_Emails]""")
cursor.commit()

#### Authenticate API Connection ####
print('Authenticating administrator account...')
print('')
accounts = api.execute_request("/v2/accounts")
account = accounts[0]
AccountID = account.Id

print('Successfully logged in to: ' + account.PrimaryDomainName)
print('Account ID: ' + str(AccountID))
print('')

# Get date of most recent email for parameter
cursor.execute("""SELECT MAX(CONVERT(DATE,LEFT(E.[Sent Date],10))) FROM DBO.Emails E WITH (NOLOCK) WHERE CONVERT(DATE,LEFT(E.[Sent Date],10)) <= GETDATE()""")
last_email = cursor.fetchone()[0]
print('Most recent email was sent ' + str(last_email))
date_param = last_email + timedelta(days=1)

#####################################
#### Get list of all sent emails ####
params = {'$filter': 'SendingType eq Manual and SentDate ge ' + str(date_param)}
print('Retrieving list of all sent emails...')
url = "/v2/accounts/" + str(AccountID) + "/SentEmails?" + urllib.parse.urlencode(params)
print(url)
print('')

emails = api.execute_request(url)

# Loop through all fields and pull down metadata
print('Looping through all sent emails...')
print('')
for email in emails.Emails:
    recipients, linklist = [], []
    
    try:
        EmailID = email.Id
    except Exception as e:
        EmailID = None

    try:
        Subject = email.Subject
    except Exception as e:
        Subject = None

    try:
        Body = email.Body
    except Exception as e:
        Body = None

    try:
        EmailType = email.Type
    except Exception as e:
        EmailType = None

    try:
        InProgress = email.InProgress
    except Exception as e:
        InProgress = None

    try:
        SenderID = email.SenderId
    except Exception as e:
        SenderID = None

    try:
        SenderName = email.SenderName
    except Exception as e:
        SenderName = None

    try:
        SendingType = email.SendingType
    except Exception as e:
        SendingType = None

    try:
        SentDate = email.SentDate
    except Exception as e:
        SentDate = None

    try:
        Recipient = email.Recipient.Id
    except Exception as e:
        Recipient = None

    try:
        RecipientType = email.Recipient.Type
    except Exception as e:
        RecipientType = None

    try:
        RecipientCount = email.RecipientCount
    except Exception as e:
        RecipientCount = None

    try:
        SuccessfullySentCount = email.SuccessfullySentCount
    except Exception as e:
        SuccessfullySentCount = None

    try:
        ReadCount = email.ReadCount
    except Exception as e:
        ReadCount = None

    try:
        FailedCount = email.FailedCount
    except Exception as e:
        FailedCount = None

    try:
        RecipientsThatClickedAnyLinkCount = email.RecipientsThatClickedAnyLinkCount
    except Exception as e:
        RecipientsThatClickedAnyLinkCount = None

    try:
        UniqueLinkClickCount = email.UniqueLinkClickCount
    except Exception as e:
        UniqueLinkClickCount = None

    try:
        IsCopySentToAdmins = email.IsCopySentToAdmins
    except Exception as e:
        IsCopySentToAdmins = None

    try:
        IsTrackingAllowed = email.IsTrackingAllowed
    except Exception as e:
        IsTrackingAllowed = None

    try:
        ReplyToAddress = email.ReplyToAddress
    except Exception as e:
        ReplyToAddress = None

    try:
        ReplyToName = email.ReplyToName
    except Exception as e:
        ReplyToName = None

    try:
        OriginId = email.Origin.Id
    except Exception as e:
        OriginId = None

    try:
        OriginName = email.Origin.Name
    except Exception as e:
        OriginName = None

    try:
        OriginType = email.Origin.OriginType
    except Exception as e:
        OriginType = None

    try:
        SubOriginId = email.SubOriginId
    except Exception as e:
        SubOriginId = None

    try:
        Url = email.Url
    except Exception as e:
        Url = None

    # Email recipients
    recips, links = get_email_recips(EmailID)
    recipients = recipients + recips
    if links:
        linklist = linklist + links
    
    row = (EmailID,Subject,Body,EmailType,InProgress,SenderID,SenderName,SendingType,SentDate,Recipient,RecipientType,RecipientCount,SuccessfullySentCount,ReadCount,FailedCount,RecipientsThatClickedAnyLinkCount,UniqueLinkClickCount,IsCopySentToAdmins,IsTrackingAllowed,ReplyToAddress,ReplyToName,OriginId,OriginName,OriginType,SubOriginId,Url)

    # INSERT DATA INTO EMAILS TABLE
    print('Inserting data into Emails table...')
    if row:
        cursor.execute("""
        INSERT INTO [dbo].[Emails] ([Email ID],[Subject],[Body],[Email Type],[In Progress],[Sender ID],[Sender Name],[Sending Type],[Sent Date],[Recipient],[Recipient Type],[Recipient Count],[SuccessfullySentCount],[ReadCount],[FailedCount],[RecipientsThatClickedAnyLinkCount],[UniqueLinkClickCount],[Is Copy Sent to Admins],[Is Tracking Allowed],[Reply To Address],[Reply To Name],[Origin ID],[Origin Name],[Origin Type],[Sub Origin ID],[Url])
             VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", row)
        cursor.commit()
    sleep(1)

    # INSERT DATA INTO EMAIL RECIPIENTS TABLE

    print('Inserting data into Email Recipients table...')
    if recipients:
        cursor.executemany("""
        INSERT INTO [dbo].[EmailRecipients] ([Email ID],[Contact ID],[Event Registration ID],[Recipient Name],[Last Name],[First Name],[Email],[Organization],[Is Delivered],[Is Opened])
             VALUES (?,?,?,?,?,?,?,?,?,?)""", recipients)
        cursor.commit()
    sleep(1)

    # INSERT DATA INTO EMAIL LINK CLICKS TABLE
    print('Inserting data into Email Link Clicks table...')
    if linklist:
        cursor.executemany("""
        INSERT INTO [dbo].[LinkClicks] ([Contact ID],[Email ID],[URL],[Clicked],[ClicksCount])
             VALUES (?,?,?,?,?)""", linklist)
        cursor.commit()
    sleep(1)

    print('All email data inserted')
    print('')

######################################
#### Get list of all draft emails ####
rows = []
params = {'$filter': 'IsScheduled eq true'}
print('Retrieving list of all email drafts...')
url = "/v2/accounts/" + str(AccountID) + "/EmailDrafts?" + urllib.parse.urlencode(params)
print(url)
print('')

drafts = api.execute_request(url)

# Loop through all fields and pull down metadata
print('Looping through all email drafts...')
print('')
for email in drafts.Emails:
    
    try:
        EmailID = email.Id
    except Exception as e:
        EmailID = None

    try:
        Subject = email.Subject
    except Exception as e:
        Subject = None

    try:
        Body = email.Body
    except Exception as e:
        Body = None

    try:
        EmailType = email.Type
    except Exception as e:
        EmailType = None

    try:
        Event = email.Event
    except Exception as e:
        Event = None

    try:
        CreatorID = email.Creator.Id
    except Exception as e:
        CreatorID = None

    try:
        CreatedDate = email.CreatedDate
    except Exception as e:
        CreatedDate = None

    try:
        LastModifier = email.Modifier.Id
    except Exception as e:
        LastModifier = None

    try:
        LastChangedDate = email.LastChangedDate
    except Exception as e:
        LastChangedDate = None

    try:
        SendingType = email.SendingType
    except Exception as e:
        SendingType = None

    try:
        ScheduledDate = email.ScheduledDate
    except Exception as e:
        ScheduledDate = None

    try:
        Recipient = email.Recipients[0].Id
    except Exception as e:
        Recipient = None

    try:
        RecipientType = email.Recipients[0].Type
    except Exception as e:
        RecipientType = None

    try:
        RecipientName = email.Recipients[0].Name
    except Exception as e:
        RecipientName = None

    try:
        IsScheduled = email.IsScheduled
    except Exception as e:
        IsScheduled = None

    try:
        IsLinkTrackingAllowed = email.IsLinkTrackingAllowed
    except Exception as e:
        IsLinkTrackingAllowed = None

    try:
        ReplyToAddress = email.ReplyToAddress
    except Exception as e:
        ReplyToAddress = None

    try:
        ReplyToName = email.ReplyToName
    except Exception as e:
        ReplyToName = None

    try:
        Url = email.Url
    except Exception as e:
        Url = None
    
    row = (EmailID,Subject,Body,EmailType,Event,CreatorID,CreatedDate,LastModifier,LastChangedDate,SendingType,IsScheduled,ScheduledDate,Recipient,RecipientType,RecipientName,IsLinkTrackingAllowed,ReplyToAddress,ReplyToName,Url)
    rows.append(row)

# INSERT DATA INTO EMAIL LINK CLICKS TABLE
cursor.execute("""TRUNCATE TABLE [dbo].[EmailDrafts]""")
cursor.commit()

print('Inserting data into Email Drafts table...')
if rows:
    cursor.executemany("""
    INSERT INTO [dbo].[EmailDrafts] ([Email ID],[Subject],[Body],[Email Type],[Event],[Creator ID],[Created Date],[Last Modifier],[Last Changed Date],[Sending Type],[Is Scheduled],[Scheduled Date],[Recipient],[Recipient Type],[Recipient Name],[Is Link Tracking Allowed],[Reply To Address],[Reply To Name],[Url])
         VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", rows)
    cursor.commit()
sleep(1)

print('All email drafts inserted')
print('')

cursor.close()
conn.close()
