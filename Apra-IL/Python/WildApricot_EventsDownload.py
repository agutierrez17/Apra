import urllib.parse
import json
import WaApi
import pyodbc
from time import sleep
from datetime import timedelta

##### Link to Wild Apricot API Documentation: https://app.swaggerhub.com/apis-docs/WildApricot/wild-apricot_public_api/7.24.0#/Accounts/GetAccountsList
##### Link to obtain application credentials: https://help.wildapricot.com/display/DOC/API+V2+authentication#APIV2authentication-Authorizingyourapplication

#### Create function for event registration types ####
def get_reg_types(EventID):
    types = []
    params = {'eventId': EventID}
    url = "/v2/accounts/" + str(AccountID) + "/EventRegistrationTypes?" + urllib.parse.urlencode(params)
    reg_types = api.execute_request(url)

    for Type in reg_types:
        try:
            TypeID = Type.Id
        except Exception as e:
            TypeID = None

        try:
            Name = Type.Name
        except Exception as e:
            Name = None

        try:
            IsEnabled = Type.IsEnabled
        except Exception as e:
            IsEnabled = None

        try:
            IsWaitlistEnabled = Type.IsWaitlistEnabled
        except Exception as e:
            IsWaitlistEnabled = None

        try:
            MultipleRegistrationAllowed = Type.MultipleRegistrationAllowed
        except Exception as e:
            MultipleRegistrationAllowed = None
        
        try:
            CurrentRegistrantsCount = Type.CurrentRegistrantsCount
        except Exception as e:
            CurrentRegistrantsCount = None

        try:
            WaitListRegistrationCount = Type.WaitListRegistrationCount
        except Exception as e:
            WaitListRegistrationCount = None

        try:
            Availability = Type.Availability
        except Exception as e:
            Availability = None

        try:
            BasePrice = Type.BasePrice
        except Exception as e:
            BasePrice = None

        try:
            GuestPrice = Type.GuestPrice
        except Exception as e:
            GuestPrice = None

        try:
            GuestRegistrationPolicy = Type.GuestRegistrationPolicy
        except Exception as e:
            GuestRegistrationPolicy = None

        try:
            Description = Type.Description
        except Exception as e:
            Description = None

        try:
            UnavailabilityPolicy = Type.UnavailabilityPolicy
        except Exception as e:
            UnavailabilityPolicy = None

        try:
            CancellationBehaviour = Type.CancellationBehaviour
        except Exception as e:
            CancellationBehaviour = None

        try:
            CancellationDaysBeforeEvent = Type.CancellationDaysBeforeEvent
        except Exception as e:
            CancellationDaysBeforeEvent = None

        try:
            Url = Type.Url
        except Exception as e:
            Url = None

        row = (EventID,TypeID,Name,IsEnabled,IsWaitlistEnabled,MultipleRegistrationAllowed,CurrentRegistrantsCount,WaitListRegistrationCount,Availability,BasePrice,GuestPrice,GuestRegistrationPolicy,Description,UnavailabilityPolicy,CancellationBehaviour,CancellationDaysBeforeEvent,Url)
        types.append(row)
        
    return types

#### Create function for event registrations ####
def get_registrations(EventID):
    registrants, fields = [], []
    params = {'eventId': EventID}
    url = "/v2/accounts/" + str(AccountID) + "/EventRegistrations?" + urllib.parse.urlencode(params)
    registrations = api.execute_request(url)

    for reg in registrations:
        try:
            RegID = reg.Id
        except Exception as e:
            RegID = None

        try:
            RegTypeId = reg.RegistrationTypeId
        except Exception as e:
            RegTypeId = None
            
        try:
            ContactID = reg.Contact.Id
        except Exception as e:
            ContactID = None

        try:
            DisplayName = reg.DisplayName
        except Exception as e:
            DisplayName = None

        try:
            InvoiceID = reg.InvoiceId
        except Exception as e:
            InvoiceID = None

        try:
            IsCheckedIn = reg.IsCheckedIn
        except Exception as e:
            IsCheckedIn = None

        try:
            IsGuestRegistration = reg.IsGuestRegistration
        except Exception as e:
            IsGuestRegistration = None

        try:
            IsPaid = reg.IsPaid
        except Exception as e:
            IsPaid = None

        try:
            OnWaitlist = reg.OnWaitlist
        except Exception as e:
            OnWaitlist = None

        try:
            Organization = reg.Organization
        except Exception as e:
            Organization = None

        try:
            RegistrationDate = reg.RegistrationDate
        except Exception as e:
            RegistrationDate = None

        try:
            RegistrationFee = reg.RegistrationFee
        except Exception as e:
            RegistrationFee = None

        try:
            PaidSum = reg.PaidSum
        except Exception as e:
            PaidSum = None

        try:
            ShowToPublic = reg.ShowToPublic
        except Exception as e:
            ShowToPublic = None

        try:
            Status = reg.Status
        except Exception as e:
            Status = None

        try:
            Url = reg.Url
        except Exception as e:
            Url = None

        try:
            for field in reg.RegistrationFields:
                try:
                    SystemCode = field.SystemCode
                except Exception as e:
                    SystemCode = None

                try:
                    Value = str(field.Value.Id)
                except Exception as e:
                    try:
                        Value = str(field.Value[0].Id)
                    except Exception as e:
                        Value = str(field.Value)
                
                fieldrow =(RegID,EventID,SystemCode,Value)
                fields.append(fieldrow)
        except Exception as e:
            pass

        regrow = (EventID,RegID,RegTypeId,ContactID,DisplayName,InvoiceID,IsCheckedIn,IsGuestRegistration,IsPaid,OnWaitlist,Organization,RegistrationDate,RegistrationFee,PaidSum,ShowToPublic,Status,Url)
        registrants.append(regrow)

    return registrants, fields

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

# Delete data from recent and future events
cursor.execute("""EXEC [dbo].[Delete_Future_Events]""")
cursor.commit()

# Get date of most recent event for parameter
cursor.execute("""SELECT MAX(CONVERT(DATE,LEFT([Start Date],10))) FROM DBO.[Events] E WITH (NOLOCK) WHERE CONVERT(DATE,LEFT(E.[Start Date],10)) <= GETDATE()""")
last_event = cursor.fetchone()[0]
print('Most recent event was held ' + str(last_event))
date_param = last_event + timedelta(days=1)
params = {'$filter': 'StartDate gt ' + str(date_param)}

################################
#### Get list of all events ####
rows, tags, regs, regis, fieldlist = [], [], [], [], []
print('Retrieving list of all events...')
url = "/v2/accounts/" + str(AccountID) + "/events?" + urllib.parse.urlencode(params)
print(url)
print('')

events = api.execute_request(url)

# Loop through all fields and pull down metadata
print('Looping through all events...')
print('')
for event in events.Events:
    try:
        EventID = event.Id
    except Exception as e:
        EventID = None

    try:
        Name = event.Name
    except Exception as e:
        Name = None

    try:
        EventType = event.EventType
    except Exception as e:
        EventType = None

    try:
        AccessLevel = event.AccessLevel
    except Exception as e:
        AccessLevel = None

    try:
        Location = event.Location
    except Exception as e:
        Location = None

    try:
        StartDate = event.StartDate
    except Exception as e:
        StartDate = None

    try:
        StartTimeSpecified = event.StartTimeSpecified
    except Exception as e:
        StartTimeSpecified = None

    try:
        EndDate = event.EndDate
    except Exception as e:
        EndDate = None

    try:
        EndTimeSpecified = event.EndTimeSpecified
    except Exception as e:
        EndTimeSpecified = None

    try:
        RegistrationEnabled = event.RegistrationEnabled
    except Exception as e:
        RegistrationEnabled = None

    try:
        RegistrationsLimit = event.RegistrationsLimit
    except Exception as e:
        RegistrationsLimit = None

    try:
        HasEnabledRegistrationTypes = event.HasEnabledRegistrationTypes
    except Exception as e:
        HasEnabledRegistrationTypes = None

    try:
        ConfirmedRegistrationsCount = event.ConfirmedRegistrationsCount
    except Exception as e:
        ConfirmedRegistrationsCount = None

    try:
        CheckedInAttendeesNumber = event.CheckedInAttendeesNumber
    except Exception as e:
        CheckedInAttendeesNumber = None

    try:
        PendingRegistrationsCount = event.PendingRegistrationsCount
    except Exception as e:
        PendingRegistrationsCount = None

    try:
        WaitListRegistrationCount = event.WaitListRegistrationCount
    except Exception as e:
        WaitListRegistrationCount = None

    try:
        Url = event.Url
    except Exception as e:
        Url = None

    try:
        for tag in event.Tags:
            tagrow = (EventID,tag)
            tags.append(tagrow)
    except Exception as e:
        pass

    # Event Registration Types
    regs = regs + get_reg_types(EventID)

    # Event Registrations
    registrants, fields = get_registrations(EventID)
    regis = regis + registrants
    fieldlist = fieldlist + fields
    
    row = (EventID,Name,EventType,AccessLevel,Location,StartDate,StartTimeSpecified,EndDate,EndTimeSpecified,RegistrationEnabled,RegistrationsLimit,HasEnabledRegistrationTypes,ConfirmedRegistrationsCount,CheckedInAttendeesNumber,PendingRegistrationsCount,WaitListRegistrationCount,Url)
    rows.append(row)


# INSERT DATA INTO EVENTS TABLE
print('Inserting data into Events table...')
if rows:
    cursor.executemany("""
    INSERT INTO [dbo].[Events] ([Event ID],[Event Name],[Event Type],[Access Level],[Location],[Start Date],[Start Time Specified],[End Date],[End Time Specified],[Registration Enabled],[Registrations Limit],[Has Enabled Registration Types],[Confirmed Registrations Count],[Checked In Attendees Number],[Pending Registrations Count],[WaitListRegistrationCount],[URL])
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", rows)
    cursor.commit()
sleep(1)

print('All events data inserted')
print('')

# INSERT DATA INTO EVENT TAGS TABLE
print('Inserting data into Event Tags table...')
if tags:
    cursor.executemany("""INSERT INTO [dbo].[EventTags] ([Event ID],[Tag]) VALUES (?,?)""", tags)
    cursor.commit()
sleep(1)

print('All event tags inserted')
print('')

# INSERT DATA INTO EVENT REGISTRATION TYPES TABLE
print('Inserting data into Event Registration Types table...')
if regs:
    cursor.executemany("""
    INSERT INTO [dbo].[EventRegistrationTypes] ([Event ID],[Registration Type ID],[Registration Type Name],[Is Enabled],[Is Waitlist Enabled],[Multiple Registration Allowed],[Current Registrants Count],[Waitlist Registration Count],[Availability],[Base Price],[Guest Price],[Guest Registration Policy],[Description],[Unavailability Policy],[Cancellation Behavior],[Cancellation Days Before Event],[URL])
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", regs)
    cursor.commit()
sleep(1)

print('All event registration types inserted')
print('')

# INSERT DATA INTO EVENT REGISTRATIONS TABLE
print('Inserting data into Event Registrations table...')
if regis:
    cursor.executemany("""
    INSERT INTO [dbo].[EventRegistrations] ([Event ID],[Registration ID],[Registration Type ID],[Contact ID],[Display Name],[Invoice ID],[Is Checked In],[Is Guest Registration],[Is Paid],[On Waitlist],[Organization],[Registration Date],[Registration Fee],[Paid Sum],[Show To Public],[Status],[URL])
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", regis)
    cursor.commit()
sleep(1)

print('All event registrations inserted')
print('')

# INSERT DATA INTO EVENT REGISTRATION FIELDS TABLE
print('Inserting data into Event Registration Fields table...')
if fieldlist:
    cursor.executemany("""INSERT INTO [dbo].[EventRegistrationFields] ([Registration ID],[Event ID],[System Code],[Value]) VALUES (?,?,?,?)""", fieldlist)
    cursor.commit()
sleep(1)

print('All event registration field data inserted')
print('')

cursor.close()
conn.close()
