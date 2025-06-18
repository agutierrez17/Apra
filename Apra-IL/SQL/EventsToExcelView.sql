CREATE VIEW [dbo].[ExcelEvents] AS

SELECT
[Event ID],
[Event Name],
[Event Type],
[In-person/Virtual],
[Access Level],
[Location],
CONVERT(DATE,ISNULL(REPLACE(LEFT([Start Date],10),'None','1901-01-01'),'1901-01-01')) AS "Start Date",
CONVERT(DATE,ISNULL(REPLACE(LEFT([End Date],10),'None','1901-01-01'),'1901-01-01')) AS "End Date",
[Registration Enabled],
[Registrations Limit],
[Confirmed Registrations Count],
[Event Revenue],
E.[Contact ID],
E.[Display Name],
E.[Organization],
[Status],
CASE
WHEN [Primary Contact Group] = 'Member-Active' THEN '1 Member-Active'
WHEN [Primary Contact Group] = 'Member-Pending Renewal' THEN '2 Member-Pending Renewal'
WHEN [Primary Contact Group] = 'Member-Lapsed' THEN '3 Member-Lapsed'
WHEN [Primary Contact Group] = 'Member-Suspended' THEN '4 Member-Suspended'
WHEN [Primary Contact Group] = 'Event attendee' THEN '5 Event attendee'
WHEN [Primary Contact Group] = 'Email recipient' THEN '6 Email recipient'
WHEN [Primary Contact Group] = 'Archived' THEN '7 Archived' END AS "Contact Group",
CONVERT(DATE,ISNULL(REPLACE(LEFT([Registration Date],10),'None','1901-01-01'),'1901-01-01')) AS "Registration Date",
[Registration Fee],
[Paid Sum],
[Registration Type Name],
[Event Tags],
[Conference],
[Webinar],
[Board],
[Networking],
[Social],
[Educational],
[Membership]
FROM [APRA-IL].[dbo].[APRA-IL_Events] E WITH (NOLOCK)
LEFT OUTER JOIN dbo.[APRA-IL_Contacts] C WITH (NOLOCK) ON E.[Contact ID] = C.[Contact ID]

GO