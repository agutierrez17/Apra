CREATE VIEW [dbo].[ExcelEmails] AS

SELECT 
[Email ID],
[Subject],
[Email Type],
[Sender ID],
[Sender Name],
[Sending Type],
CONVERT(DATE,ISNULL(REPLACE(LEFT([Sent Date],10),'None','1901-01-01'),'1901-01-01')) AS "Sent Date",
[Recipient Count],
[SuccessfullySentCount],
[ReadCount],
[FailedCount],
[RecipientsThatClickedAnyLinkCount],
[UniqueLinkClickCount],
[Event ID],
[Event Name],
E.[Contact ID],
[Recipient Name],
E.[Last Name],
E.[First Name],
CASE
WHEN [Primary Contact Group] = 'Member-Active' THEN '1 Member-Active'
WHEN [Primary Contact Group] = 'Member-Pending Renewal' THEN '2 Member-Pending Renewal'
WHEN [Primary Contact Group] = 'Member-Lapsed' THEN '3 Member-Lapsed'
WHEN [Primary Contact Group] = 'Member-Suspended' THEN '4 Member-Suspended'
WHEN [Primary Contact Group] = 'Event attendee' THEN '5 Event attendee'
WHEN [Primary Contact Group] = 'Email recipient' THEN '6 Email recipient'
WHEN [Primary Contact Group] = 'Archived' THEN '7 Archived' END AS "Contact Group",
E.[Organization],
[Is Delivered],
[Is Opened],
[Clicked]
FROM [APRA-IL].[dbo].[APRA-IL_Emails] E WITH (NOLOCK)
LEFT OUTER JOIN dbo.[APRA-IL_Contacts] C WITH (NOLOCK) ON E.[Contact ID] = C.[Contact ID]

GO