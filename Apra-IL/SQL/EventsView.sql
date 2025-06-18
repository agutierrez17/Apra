USE [APRA-IL]
GO

/****** Object:  View [dbo].[APRA-IL_Events]    Script Date: 2/17/2025 1:44:21 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

ALTER VIEW [dbo].[APRA-IL_Events] AS

SELECT DISTINCT
E.[Event ID],
[Event Name],
[Event Type],
CASE 
WHEN [Location] IN ('Conference Call','Webinar','Virtual','Zoom','Your Desk') THEN 'Virtual'
WHEN [Event Name] LIKE '%WEBINAR%' THEN 'Virtual'
WHEN [Location] = '' THEN 'Virtual'
ELSE 'In-person' END AS "In-person/Virtual",
[Access Level],
[Location],
[Start Date],
[End Date],
[Registration Enabled],
[Registrations Limit],
[Confirmed Registrations Count],
(SELECT SUM(ER.[Paid Sum]) FROM dbo.EventRegistrations ER WITH (NOLOCK) WHERE ER.[Event ID] = E.[Event ID] AND ER.Status = 'Paid') AS "Event Revenue",

---- REGISTRANTS DATA
ER.[Contact ID],
ER.[Display Name],
OC.[Corrected Org Name] AS "Organization",
ER.Status,
ER.[Registration Date],
ER.[Registration Fee],
ER.[Paid Sum],
ERT.[Registration Type Name],

---- EVENT TAGS
(SELECT STUFF((
        SELECT ', ' + ET.Tag
        FROM DBO.EventTags ET WITH (NOLOCK)
        WHERE E.[Event ID] = ET.[Event ID]
		ORDER BY ET.Tag
        FOR XML PATH('')), 1, 2, ''))  AS "Event Tags",
CASE WHEN E.[Event ID] IN (SELECT ET.[Event ID] FROM dbo.EventTags ET WITH (NOLOCK) WHERE ET.Tag = 'Conference') THEN 1 ELSE 0 END AS "Conference",
CASE WHEN E.[Event ID] IN (SELECT ET.[Event ID] FROM dbo.EventTags ET WITH (NOLOCK) WHERE ET.Tag = 'Webinar') THEN 1 ELSE 0 END AS "Webinar",
CASE WHEN E.[Event ID] IN (SELECT ET.[Event ID] FROM dbo.EventTags ET WITH (NOLOCK) WHERE ET.Tag = 'Board') THEN 1 ELSE 0 END AS "Board",
CASE WHEN E.[Event ID] IN (SELECT ET.[Event ID] FROM dbo.EventTags ET WITH (NOLOCK) WHERE ET.Tag = 'Networking') THEN 1 ELSE 0 END AS "Networking",
CASE WHEN E.[Event ID] IN (SELECT ET.[Event ID] FROM dbo.EventTags ET WITH (NOLOCK) WHERE ET.Tag = 'Social') THEN 1 ELSE 0 END AS "Social",
CASE WHEN E.[Event ID] IN (SELECT ET.[Event ID] FROM dbo.EventTags ET WITH (NOLOCK) WHERE ET.Tag = 'Educational') THEN 1 ELSE 0 END AS "Educational",
CASE WHEN E.[Event ID] IN (SELECT ET.[Event ID] FROM dbo.EventTags ET WITH (NOLOCK) WHERE ET.Tag = 'Membership') THEN 1 ELSE 0 END AS "Membership"

FROM [APRA-IL].[dbo].[Events] E WITH (NOLOCK)
INNER JOIN dbo.EventRegistrations ER WITH (NOLOCK) ON E.[Event ID] = ER.[Event ID]
LEFT OUTER JOIN dbo.Organization_Crosswalk OC WITH (NOLOCK) ON ER.Organization = OC.Organization
LEFT OUTER JOIN dbo.EventRegistrationTypes ERT WITH (NOLOCK) ON ER.[Event ID] = ERT.[Event ID] AND ER.[Registration Type ID] = ERT.[Registration Type ID]

GO


