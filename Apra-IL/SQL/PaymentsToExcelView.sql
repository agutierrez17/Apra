ALTER VIEW [dbo].[ExcelPayments] AS

SELECT 
[Payment ID],
[Payment Amount],
CONVERT(DATE,ISNULL(REPLACE(LEFT([Payment Date],10),'None','1901-01-01'),'1901-01-01')) AS "Payment Date",
[Payment Type],
P.[Contact ID],
[Contact Name],
[Contact Last Name],
[Contact First Name],
CASE
WHEN [Primary Contact Group] = 'Member-Active' THEN '1 Member-Active'
WHEN [Primary Contact Group] = 'Member-Pending Renewal' THEN '2 Member-Pending Renewal'
WHEN [Primary Contact Group] = 'Member-Lapsed' THEN '3 Member-Lapsed'
WHEN [Primary Contact Group] = 'Member-Suspended' THEN '4 Member-Suspended'
WHEN [Primary Contact Group] = 'Event attendee' THEN '5 Event attendee'
WHEN [Primary Contact Group] = 'Email recipient' THEN '6 Email recipient'
WHEN [Primary Contact Group] = 'Archived' THEN '7 Archived' END AS "Contact Group",
[Contact Organization],
[Tender Type],
[Payment Created By],
[Invoice ID],
CONVERT(DATE,ISNULL(REPLACE(LEFT([Invoice Date],10),'None','1901-01-01'),'1901-01-01')) AS "Invoice Date",
[Invoice Type],
[Invoice Created By]
FROM [APRA-IL].[dbo].[APRA-IL_Payments] P WITH (NOLOCK)
LEFT OUTER JOIN dbo.[APRA-IL_Contacts] C WITH (NOLOCK) ON P.[Contact ID] = C.[Contact ID]

GO