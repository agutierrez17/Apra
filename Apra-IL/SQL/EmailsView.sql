CREATE VIEW dbo.[APRA-IL_Emails] AS

SELECT DISTINCT
---- EMAIL DATA
E.[Email ID],
[Subject],
[Email Type],
[Sender ID],
[Sender Name],
[Sending Type],
[Sent Date],
[Recipient Count],
[SuccessfullySentCount],
[ReadCount],
[FailedCount],
[RecipientsThatClickedAnyLinkCount],
[UniqueLinkClickCount],
[Origin ID] AS "Event ID",
[Origin Name] AS "Event Name",

---- RECIPIENT DATA
ER.[Contact ID],
ER.[Recipient Name],
ER.[Last Name],
ER.[First Name],
OC.[Corrected Org Name] AS "Organization",
ER.[Is Delivered],
ER.[Is Opened],
CASE WHEN LC.[Contact ID] IS NOT NULL THEN 1 ELSE 0 END AS "Clicked"

FROM [APRA-IL].[dbo].[Emails] E WITH (NOLOCK) 
LEFT OUTER JOIN dbo.EmailRecipients ER WITH (NOLOCK) ON E.[Email ID] = ER.[Email ID]
LEFT OUTER JOIN dbo.Organization_Crosswalk OC WITH (NOLOCK) ON ER.Organization = OC.Organization
LEFT OUTER JOIN dbo.LinkClicks LC WITH (NOLOCK) ON ER.[Email ID] = LC.[Email ID] AND ER.[Contact ID] = LC.[Contact ID]

WHERE
E.Recipient IS NULL

GO