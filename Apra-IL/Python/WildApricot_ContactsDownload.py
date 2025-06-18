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


###############################################
#### Get list of all custom contact fields ####
print('Retrieving list of all custom contact fields...')
fields, values, levels = [], [], []
url = "/v2/accounts/" + str(AccountID) + "/contactfields"
print(url)
print('')

contactfields = api.execute_request(url)

# Loop through all fields and pull down metadata
print('Looping through all custom fields...')
print('')
for field in contactfields:
    try:
        FieldID = field.Id
    except Exception as e:
        FieldID = None
        
    try:
        FieldName = field.FieldName
    except Exception as e:
        FieldName = None
        
    try:
        SystemCode = field.SystemCode
    except Exception as e:
        SystemCode = None
        
    try:
        IsSystem = field.IsSystem
    except Exception as e:
        IsSystem = None
        
    try:
        Description = field.Description
    except Exception as e:
        Description = None
        
    try:
        Order = field.Order
    except:
        Order = None
        
    try:
        FieldType = field.FieldType
    except Exception as e:
        FieldType = None
        
    try:
        Access = field.Access
    except Exception as e:
        Access = None
        
    try:
        AdminOnly = field.AdminOnly
    except Exception as e:
        AdminOnly = None
        
    try:
        MemberAccess = field.MemberAccess
    except Exception as e:
        MemberAccess = None
        
    try:
        MemberOnly = field.MemberOnly
    except Exception as e:
        MemberOnly = None
        
    try:
        IsBuiltIn = field.IsBuiltIn
    except Exception as e:
        IsBuiltIn = None
        
    try:
        SupportSearch = field.SupportSearch
    except Exception as e:
        SupportSearch = None
        
    try:
        IsEditable = field.IsEditable
    except Exception as e:
        IsEditable = None

    try:
        for item in field.ExistsInLevels:
            ID = item.Id
            Url = item.Url
            
            LevelRow = (FieldID,ID,Url)
            levels.append(LevelRow)
    except Exception as e:
        pass

    try:
        for value in field.AllowedValues:
            try:
                Id = value.Id
            except Exception as e:
                Id = None
                
            try:  
                Label = value.Label
            except Exception as e:
                Label = None

            try:
                Position = value.Position
            except Exception as e:
                Position = None

            try:
                SelectedByDefault = value.SelectedByDefault
            except Exception as e:
                SelectedByDefault = None

            try:
                Value = value.Value
            except Exception as e:
                Value = None
            
            ValueRow = (FieldID,Id,Label,Position,SelectedByDefault,Value)
            values.append(ValueRow)
    except Exception as e:
        pass
    
    row = (FieldID,FieldName,FieldType,SystemCode,IsSystem,Description,Order,Access,AdminOnly,MemberAccess,MemberOnly,IsBuiltIn,SupportSearch,IsEditable)
    fields.append(row)

# INSERT DATA INTO CONTACT FIELDS TABLE
cursor.execute("""TRUNCATE TABLE [dbo].[Contact_Fields]""")
cursor.commit()

print('Inserting data into Contact_Fields table...')
cursor.executemany("""
INSERT INTO [dbo].[Contact_Fields] ([Field ID],[Field Name],[Field Type],[System Code],[Is System],[Field Description],[Field Order],[Field Access],[Admin Only],[Member Access],[Member Only],[Is Built In],[Support Search],[Is Editable])
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", fields)
cursor.commit()
sleep(1)

# INSERT DATA INTO FIELD VALUES TABLE
cursor.execute("""TRUNCATE TABLE [dbo].[Field_Values]""")
cursor.commit()

print('Inserting data into Field_Values table...')
cursor.executemany("""
INSERT INTO [dbo].[Field_Values] ([Field ID],[Value ID],[Value Label],[Value Position],[Selected by Default],[Value Name])
    VALUES (?,?,?,?,?,?)""", values)
cursor.commit()
sleep(1)

# INSERT DATA INTO FIELD MEMBERSHIP LEVELS TABLE
cursor.execute("""TRUNCATE TABLE [dbo].[Field_Membership_Levels]""")
cursor.commit()

print('Inserting data into Field_Membership_Levels table...')
cursor.executemany("""
INSERT INTO [dbo].[Field_Membership_Levels] ([Field ID],[Membership Level ID],[Membership Level URL])
    VALUES (?,?,?)""", levels)
cursor.commit()
sleep(1)

print('All contact fields data inserted')
print('')


##########################################
#### Get list of all membership types ####
print('Retrieving list of all membership types...')
rows = []
url = "/v2/accounts/" + str(AccountID) + "/membershiplevels"
print(url)
print('')

memberships = api.execute_request(url)

# Loop through all rows
print('Looping through all membership levels...')
print('')
for level in memberships:
    try:
        LevelID = level.Id
    except Exception as e:
        LevelID = None
        
    try:
        LevelName = level.Name
    except Exception as e:
        LevelName = None
        
    try:
        MembershipFee = level.MembershipFee
    except Exception as e:
        MembershipFee = None
        
    try:
        PublicCanApply = level.PublicCanApply
    except Exception as e:
        PublicCanApply = None
        
    try:
        Description = level.Description
    except Exception as e:
        Description = None
        
    try:
        DisableSelfRenewal = level.DisableSelfRenewal
    except:
        DisableSelfRenewal = None
        
    try:
        LevelType = level.Type
    except Exception as e:
        LevelType = None
        
    try:
        LevelUrl = level.Url
    except Exception as e:
        LevelUrl = None
        
    try:
        RenewalPeriod = level.RenewalPeriod.Kind
    except Exception as e:
        RenewalPeriod = None
        
    try:
        StartFromJoinDate = level.RenewalPeriod.StartFromJoinDate
    except Exception as e:
        StartFromJoinDate = None
        
    try:
        YearPeriod = level.RenewalPeriod.YearPeriod
    except Exception as e:
        YearPeriod = None
    
    row = (LevelID,LevelName,MembershipFee,PublicCanApply,Description,DisableSelfRenewal,LevelType,LevelUrl,RenewalPeriod,StartFromJoinDate,YearPeriod)
    rows.append(row)

# INSERT DATA INTO FIELD MEMBERSHIP LEVELS TABLE
cursor.execute("""TRUNCATE TABLE [dbo].[Membership_Levels]""")
cursor.commit()

print('Inserting data into Membership_Levels table...')
cursor.executemany("""
INSERT INTO [dbo].[Membership_Levels] ([Level ID],[Level Name],[Fee],[Public Can Apply],[Description],[Disable Self Renewal],[Level Type],[URL],[Renewal Period],[Start From Join Date],[Year Period])
    VALUES (?,?,?,?,?,?,?,?,?,?,?)""", rows)
cursor.commit()
sleep(1)

print('All membership level data inserted')
print('')


#### Get list of all contacts ####
print('Retrieving list of all APRA-IL members...')
rows, fields = [],[]
params = {'$async': 'false'}
url = "/v2/accounts/" + str(AccountID) + '/Contacts?' + urllib.parse.urlencode(params)
print(url)

print('')
contacts = [api.execute_request(url).Contacts]

#### Loop through all contacts in list ####
print('Looping through members...')
print('')
for contact in contacts[0]:
    try:
        ContactID = contact.Id
    except Exception as e:
        ContactID = None

    try:
        ContactURL = contact.Url
    except Exception as e:
        ContactURL = None

    try:
        FirstName = contact.FirstName
    except Exception as e:
        FirstName = None

    try:
        LastName = contact.LastName
    except Exception as e:
        LastName = None

    try:
        Organization = contact.Organization
    except Exception as e:
        Organization = None

    try:
        Email = contact.Email
    except Exception as e:
        Email = None

    try:
        DisplayName = contact.DisplayName
    except Exception as e:
        DisplayName = None

    try:
        ProfileLastUpdated = contact.ProfileLastUpdated
    except Exception as e:
        ProfileLastUpdated = None

    try:
        MembershipEnabled = contact.MembershipEnabled
    except Exception as e:
        MembershipEnabled = None

    try:
        Status = contact.Status
    except Exception as e:
        Status = None

    try:
        IsAdmin = contact.IsAccountAdministrator
    except Exception as e:
        IsAdmin = None

    try:
        TermsOfUseAccepted = contact.TermsOfUseAccepted
    except Exception as e:
        TermsOfUseAccepted = None

    try:
        MembershipLevel = contact.MembershipLevel.Id
    except Exception as e:
        MembershipLevel = None

    for field in contact.FieldValues:
        SystemCode = field.SystemCode

        try:
            Value = str(field.Value.Id)
        except Exception as e:
            try:
                Value = str(field.Value[0].Id)
            except Exception as e:
                Value = str(field.Value)

        ValueRow = (ContactID,SystemCode,Value)
        fields.append(ValueRow)

    row = (ContactID,ContactURL,FirstName,LastName,Organization,Email,DisplayName,ProfileLastUpdated,MembershipEnabled,Status,IsAdmin,TermsOfUseAccepted,MembershipLevel)
    rows.append(row)

# INSERT DATA INTO CONTACTS TABLE
cursor.execute("""TRUNCATE TABLE [dbo].[Contacts]""")
cursor.commit()

print('Inserting data into Contacts table...')
cursor.executemany("""
INSERT INTO [dbo].[Contacts] ([Contact ID],[Contact URL],[First Name],[Last Name],[Organization],[Email],[Display Name],[Profile Last Updated],[Membership Enabled],[Status],[Is Admin],[Terms Of Use Accepted],[Membership Level])
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", rows)
cursor.commit()
sleep(1)

# INSERT DATA INTO CONTACT FIELD VALUES TABLE
cursor.execute("""TRUNCATE TABLE [dbo].[Contact_Field_Values]""")
cursor.commit()

print('Inserting data into Contact_Field_Values table...')
cursor.executemany("""INSERT INTO [dbo].[Contact_Field_Values] ([Contact ID],[System Code],[Value]) VALUES (?,?,?)""", fields)
cursor.commit()
sleep(1)

print('All contacts data inserted')
print('')

# RUN PROCEDURE TO REFRESH PIVOTED CONTACT FIELDS TABLE
print('Running SQL procedure to refresh pivoted contact fields table...')
cursor.execute("""EXEC [dbo].[Pivot_Contact_Fields]""")
cursor.commit()
print('Procedure completed.')
print('')

cursor.close()
conn.close()
