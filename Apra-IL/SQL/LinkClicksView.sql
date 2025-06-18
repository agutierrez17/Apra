ALTER VIEW dbo.[Click_Detail] AS 

SELECT DISTINCT
LC.[Contact ID],
ER.[Recipient Name],
OC.[Corrected Org Name] AS "Organization",
E.[Email ID],
E.[Sent Date],
E.Subject AS "Email Subject",
CAST(LC.[URL] AS varchar(max)) AS "Link URL",
[Clicked],
[ClicksCount] AS "Link Total Clicks Count",

CASE 
WHEN LC.URL LIKE '%apraillinois%%.org%' THEN 'APRA-IL Website'
WHEN LC.URL LIKE '%LINKEDIN%' THEN 'LinkedIn'
WHEN LC.URL LIKE '%Annual%%Report%' THEN 'Annual Report'
WHEN LC.URL LIKE '%Unsubscribe%' THEN 'Unsubscribe'
WHEN LC.URL LIKE '%apraillinois%%event%' THEN 'Event'
WHEN LC.URL LIKE '%apraillinois%%blog%' THEN 'Blog'
WHEN LC.URL LIKE '%twitter%' THEN 'Twitter'
WHEN LC.URL LIKE '%drive.google%' THEN 'Google Drive'
WHEN LC.URL LIKE '%docs.google%' THEN 'Google Docs'
WHEN LC.URL LIKE '%Zoom%' THEN 'Zoom'
WHEN LC.URL LIKE '%surveymonkey%' THEN 'Survey'
WHEN LC.URL LIKE '%apra%' and LC.URL not LIKE '%illinois%'THEN 'Other APRA Chapter'
WHEN LC.URL LIKE '%jobs%' THEN 'Job Posting'
ELSE 'Other' END AS "Link Category",

CASE 
WHEN LC.URL LIKE '%apraillinois%%.org%%event%' THEN 'Event Registration'
WHEN LC.URL LIKE '%apraillinois%%.org%%resources%' THEN 'Resources'
WHEN LC.URL LIKE '%apraillinois%%.org%%blog%' THEN 'Blog'
WHEN LC.URL LIKE '%apraillinois%%.org%%join%' THEN 'Membership'
ELSE '' END AS "Link Sub Category",

ISNULL(CASE
WHEN EV.[Event ID] IS NOT NULL THEN EV.[Event Name]
ELSE (SELECT EV.[Event Name] FROM dbo.Events EV WITH (NOLOCK) WHERE EV.[Event ID] = CASE WHEN LC.URL LIKE '%apraillinois%%.org%%event%%[0-9]%' THEN REPLACE(SUBSTRING(LC.URL, CHARINDEX('event',LC.URL,0),13),'event-','') END) END,'') AS "Event Name"

FROM [APRA-IL].[dbo].[LinkClicks] LC WITH (NOLOCK)
INNER JOIN dbo.Emails E WITH (NOLOCK) ON LC.[Email ID] = E.[Email ID]
INNER JOIN dbo.EmailRecipients ER WITH (NOLOCK) ON LC.[Contact ID] = ER.[Contact ID] AND ER.[Email ID] = E.[Email ID]
LEFT OUTER JOIN dbo.Organization_Crosswalk OC WITH (NOLOCK) ON ER.Organization = OC.Organization
LEFT OUTER JOIN dbo.EventRegistrations EVR WITH (NOLOCK) ON EVR.[Registration ID] = ER.[Event Registration ID]
LEFT OUTER JOIN dbo.Events EV WITH (NOLOCK) ON EVR.[Event ID] = EV.[Event ID]

GO