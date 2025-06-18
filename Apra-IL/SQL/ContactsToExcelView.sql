CREATE VIEW [dbo].[ExcelContacts] AS

SELECT 
[Contact ID],
[Display Name],
[Last Name],
[First Name],
CASE
WHEN [Primary Contact Group] = 'Member-Active' THEN '1 Member-Active'
WHEN [Primary Contact Group] = 'Member-Pending Renewal' THEN '2 Member-Pending Renewal'
WHEN [Primary Contact Group] = 'Member-Lapsed' THEN '3 Member-Lapsed'
WHEN [Primary Contact Group] = 'Member-Suspended' THEN '4 Member-Suspended'
WHEN [Primary Contact Group] = 'Event attendee' THEN '5 Event attendee'
WHEN [Primary Contact Group] = 'Email recipient' THEN '6 Email recipient'
WHEN [Primary Contact Group] = 'Archived' THEN '7 Archived' END AS "Contact Group",
[Organization],
[Sub Organization],
[Organization Type],
[Title],
[E-Mail],
[Address Line 1],
[Address Line 2],
[City],
[State],
[Zip Code],
[Country],
[Phone],
[Member],
[Membership status],
[Membership Level],
[Archived],
[Event registrant],
[Suspended member],
[Event announcements],
[Member emails and newsletters],
[Email delivery disabled],
[Email delivery disabled automatically],
[Receiving emails disabled],
CONVERT(DATE,ISNULL(LEFT([Creation date],10),'1901-01-01')) AS "Creation date",
CONVERT(DATE,ISNULL(REPLACE(LEFT([Last login date],10),'None','1901-01-01'),'1901-01-01')) AS "Last login date",
[Interested in volunteering with APRA-IL?],
CONVERT(DATE,ISNULL(REPLACE(LEFT([Member since],10),'None','1901-01-01'),'1901-01-01')) AS "Member since",
CONVERT(DATE,ISNULL(REPLACE(LEFT([Renewal due],10),'None','1901-01-01'),'1901-01-01')) AS "Renewal due",
CONVERT(DATE,ISNULL(REPLACE(LEFT([Renewal date last changed],10),'None','1901-01-01'),'1901-01-01')) AS "Renewal date last changed",
CONVERT(DATE,ISNULL(REPLACE(LEFT([Level last changed],10),'None','1901-01-01'),'1901-01-01')) AS "Level last changed",
[Member Value],
[Outstanding Balance],
[Number of Payments],
CONVERT(DATE,ISNULL(REPLACE(LEFT([Last Payment Date],10),'None','1901-01-01'),'1901-01-01')) AS "Last Payment Date",
[Last Payment Amount],
[Last Purchase Item],
[Events Attended],
[Events Attended-In person],
[Events Attended-Virtual],
CONVERT(DATE,ISNULL(REPLACE(LEFT([Last Event Date],10),'None','1901-01-01'),'1901-01-01')) AS "Last Event Date",
[Last Event Name],
[Last Event Location],
[Emails Received],
[Emails Opened],
[Emails Clicked],
[Total Link Clicks],
CONVERT(DATE,ISNULL(REPLACE(LEFT([Last Email Received Date],10),'None','1901-01-01'),'1901-01-01')) AS "Last Email Received Date",
CONVERT(DATE,ISNULL(REPLACE(LEFT([Last Email Opened Date],10),'None','1901-01-01'),'1901-01-01')) AS "Last Email Opened Date",
CONVERT(DATE,ISNULL(REPLACE(LEFT([Last Email Click Date],10),'None','1901-01-01'),'1901-01-01')) AS "Last Email Click Date",
CONVERT(DATE,ISNULL(REPLACE(LEFT([Profile Last Updated],10),'None','1901-01-01'),'1901-01-01')) AS "Profile Last Updated",
[Profile last updated by]
FROM [APRA-IL].[dbo].[APRA-IL_Contacts]

GO