ALTER VIEW [dbo].[ExcelLinkClicks] AS

SELECT 
CD.[Contact ID],
[Recipient Name],
CASE
WHEN [Primary Contact Group] = 'Member-Active' THEN '1 Member-Active'
WHEN [Primary Contact Group] = 'Member-Pending Renewal' THEN '2 Member-Pending Renewal'
WHEN [Primary Contact Group] = 'Member-Lapsed' THEN '3 Member-Lapsed'
WHEN [Primary Contact Group] = 'Member-Suspended' THEN '4 Member-Suspended'
WHEN [Primary Contact Group] = 'Event attendee' THEN '5 Event attendee'
WHEN [Primary Contact Group] = 'Email recipient' THEN '6 Email recipient'
WHEN [Primary Contact Group] = 'Archived' THEN '7 Archived' END AS "Contact Group",
CD.[Organization],
[Email ID],
CONVERT(DATE,ISNULL(REPLACE(LEFT([Sent Date],10),'None','1901-01-01'),'1901-01-01')) AS "Sent Date",
[Email Subject],
[Link URL],
[Clicked],
[Link Total Clicks Count],
[Link Category],
[Link Sub Category],
[Event Name]
FROM [APRA-IL].[dbo].[APRA-IL_Click_Detail] CD WITH (NOLOCK)
LEFT OUTER JOIN dbo.[APRA-IL_Contacts] C WITH (NOLOCK) ON CD.[Contact ID] = C.[Contact ID]

GO