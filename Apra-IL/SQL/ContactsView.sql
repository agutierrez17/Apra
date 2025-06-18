USE [APRA-IL]
GO

/****** Object:  View [dbo].[APRA-IL_Contacts]    Script Date: 3/1/2025 7:44:15 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO




ALTER VIEW [dbo].[APRA-IL_Contacts] AS

SELECT 
---- DEMOGRAPHIC INFO
C.[Contact ID],
C.[Display Name],
C.[Contact URL],
C.[Last Name],
C.[First Name],
ISNULL(O.[Corrected Org Name],'') AS "Organization",
ISNULL(O.[Sub-Org],'') AS "Sub Organization",
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

---- MEMBERSHIP INFO
CASE
WHEN Archived = 'TRUE' THEN 'Archived'
WHEN [Member] = 'TRUE' AND [Membership status] = 'Active' THEN 'Member-Active'
WHEN [Member] = 'TRUE' AND [Membership status] = 'Pending - Renewal' THEN 'Member-Pending Renewal'
WHEN [Membership status] <> 'Active' AND [Membership status] IS NOT NULL THEN 'Member-Lapsed'
WHEN [Suspended member] = 'TRUE' THEN 'Member-Suspended'
WHEN [Event registrant] = 'TRUE' THEN 'Event attendee'
WHEN [Receiving emails disabled] = 'TRUE' THEN 'Archived'
ELSE 'Email Recipient' END AS "Primary Contact Group",

[Member],
[Membership status],
[Membership level ID] AS "Membership Level",
[Archived],
[Event registrant],
[Suspended member],
[Event announcements],
[Member emails and newsletters],
[Email delivery disabled],
[Email delivery disabled automatically],
[Receiving emails disabled],
CONVERT(DATE,ISNULL(REPLACE(LEFT([Creation date],10),'None','1901-01-01'),'1901-01-01')) AS "Creation date",
CONVERT(DATE,ISNULL(REPLACE(LEFT([Last login date],10),'None','1901-01-01'),'1901-01-01')) AS "Last login date",
[Years in Prospect Development],
[Interested in volunteering with APRA-IL?],
CONVERT(DATE,ISNULL(REPLACE(LEFT([Member since],10),'None','1901-01-01'),'1901-01-01')) AS "Member since",
CONVERT(DATE,ISNULL(REPLACE(LEFT([Renewal due],10),'None','1901-01-01'),'1901-01-01')) AS "Renewal due",
CONVERT(DATE,ISNULL(REPLACE(LEFT([Renewal date last changed],10),'None','1901-01-01'),'1901-01-01')) AS "Renewal date last changed",
CONVERT(DATE,ISNULL(REPLACE(LEFT([Level last changed],10),'None','1901-01-01'),'1901-01-01')) AS "Level last changed",

---- PAYMENT DATA
COALESCE(SUM(I.[Paid Amount]),0) + COALESCE(SUM(R.[Value]),0) AS "Member Value",
[Balance] AS "Outstanding Balance",
(SELECT COUNT(DISTINCT P.[Payment ID]) FROM dbo.Payments P WITH (NOLOCK) WHERE P.[Contact ID] = C.[Contact ID]) AS "Number of Payments",
CONVERT(DATE,ISNULL(REPLACE(LEFT((SELECT MAX(P.[Created Date]) FROM dbo.Payments P WITH (NOLOCK) WHERE P.[Contact ID] = C.[Contact ID]),10),'None','1901-01-01'),'1901-01-01')) AS "Last Payment Date",
(SELECT P2.[Value] FROM dbo.Payments P2 WITH (NOLOCK) WHERE P2.[Contact ID] = C.[Contact ID] AND P2.[Payment ID] = (SELECT MAX(P.[Payment ID]) FROM dbo.Payments P WITH (NOLOCK) WHERE P.[Contact ID] = C.[Contact ID])) AS "Last Payment Amount",
(SELECT I.[Order Type] FROM DBO.[Invoices] I WITH (NOLOCK) WHERE I.[Invoice ID] = (SELECT MAX(PA.[Invoice ID]) FROM DBO.[PaymentAllocations] PA WITH (NOLOCK) WHERE PA.[Payment ID] = (SELECT MAX(P.[Payment ID]) FROM dbo.Payments P WITH (NOLOCK) WHERE P.[Contact ID] = C.[Contact ID]))) AS "Last Purchase Item",

---- EVENTS DATA
(SELECT COUNT(DISTINCT ER.[Event ID]) FROM dbo.EventRegistrations ER WITH (NOLOCK) WHERE ER.[Contact ID] = C.[Contact ID]) AS "Events Attended",
(SELECT COUNT(DISTINCT ER.[Event ID]) FROM dbo.[APRA-IL_Events] ER WITH (NOLOCK) WHERE ER.[Contact ID] = C.[Contact ID] AND ER.[In-person/Virtual] = 'In-person') AS "Events Attended-In person",
(SELECT COUNT(DISTINCT ER.[Event ID]) FROM dbo.[APRA-IL_Events] ER WITH (NOLOCK) WHERE ER.[Contact ID] = C.[Contact ID] AND ER.[In-person/Virtual] = 'Virtual') AS "Events Attended-Virtual",
CONVERT(DATE,ISNULL(REPLACE(LEFT((SELECT MAX(E.[Start Date]) FROM dbo.EventRegistrations ER WITH (NOLOCK) INNER JOIN dbo.Events E WITH (NOLOCK) ON ER.[Event ID] = E.[Event ID] WHERE ER.[Contact ID] = C.[Contact ID]),10),'None','1901-01-01'),'1901-01-01')) AS "Last Event Date",
(SELECT E.[Event Name] FROM DBO.[Events] E WITH (NOLOCK) WHERE E.[Start Date] = (SELECT MAX(E.[Start Date]) FROM dbo.EventRegistrations ER WITH (NOLOCK) INNER JOIN dbo.Events E WITH (NOLOCK) ON ER.[Event ID] = E.[Event ID] WHERE ER.[Contact ID] = C.[Contact ID])) AS "Last Event Name",
(SELECT E.Location FROM DBO.[Events] E WITH (NOLOCK) WHERE E.[Start Date] = (SELECT MAX(E.[Start Date]) FROM dbo.EventRegistrations ER WITH (NOLOCK) INNER JOIN dbo.Events E WITH (NOLOCK) ON ER.[Event ID] = E.[Event ID] WHERE ER.[Contact ID] = C.[Contact ID])) AS "Last Event Location",

---- EMAIL DATA
(SELECT COUNT(DISTINCT ER.[Email ID]) FROM dbo.EmailRecipients ER WITH (NOLOCK) WHERE ER.[Contact ID] = C.[Contact ID]) AS "Emails Received",
(SELECT COUNT(DISTINCT ER.[Email ID]) FROM dbo.EmailRecipients ER WITH (NOLOCK) WHERE ER.[Contact ID] = C.[Contact ID] AND ER.[Is Opened] = 1) AS "Emails Opened",
(SELECT COUNT(DISTINCT LC.[Email ID]) FROM dbo.LinkClicks LC WITH (NOLOCK) WHERE LC.[Contact ID] = C.[Contact ID]) AS "Emails Clicked",
(SELECT COUNT(*) FROM dbo.LinkClicks LC WITH (NOLOCK) WHERE LC.[Contact ID] = C.[Contact ID]) AS "Total Link Clicks",
CONVERT(DATE,ISNULL(REPLACE(LEFT((SELECT MAX(ER.[Sent Date]) FROM dbo.[APRA-IL_Emails] ER WITH (NOLOCK) WHERE ER.[Contact ID] = C.[Contact ID]),10),'None','1901-01-01'),'1901-01-01')) AS "Last Email Received Date",
CONVERT(DATE,ISNULL(REPLACE(LEFT((SELECT MAX(ER.[Sent Date]) FROM dbo.[APRA-IL_Emails] ER WITH (NOLOCK) WHERE ER.[Contact ID] = C.[Contact ID] AND ER.[Is Opened] = 1),10),'None','1901-01-01'),'1901-01-01')) AS "Last Email Opened Date",
CONVERT(DATE,ISNULL(REPLACE(LEFT((SELECT MAX(ER.[Sent Date]) FROM dbo.[APRA-IL_Emails] ER WITH (NOLOCK) WHERE ER.[Contact ID] = C.[Contact ID] AND ER.Clicked = 1),10),'None','1901-01-01'),'1901-01-01')) AS "Last Email Click Date",

---- AUDIT DATA
CONVERT(DATE,ISNULL(REPLACE(LEFT(C.[Profile Last Updated],10),'None','1901-01-01'),'1901-01-01')) AS "Profile Last Updated",
[Profile last updated by],
[Notes]

FROM [APRA-IL].[dbo].[Contacts] C WITH (NOLOCK)
INNER JOIN DBO.Contact_Field_Values_Pivoted CFP WITH (NOLOCK) ON C.[Contact ID] = CFP.[Contact ID]
LEFT OUTER JOIN dbo.Invoices I WITH (NOLOCK) ON C.[Contact ID] = I.[Contact ID]
LEFT OUTER JOIN dbo.Refunds R WITH (NOLOCK) ON C.[Contact ID] = R.[Contact ID]
LEFT OUTER JOIN dbo.Organization_Crosswalk O WITH (NOLOCK) ON C.Organization = O.Organization

GROUP BY
C.[Contact ID],
C.[Display Name],
C.[Contact URL],
C.[Last Name],
C.[First Name],
O.[Corrected Org Name],
O.[Sub-Org],
[Organization Type],
[Title],
C.[Email],
C.[Profile Last Updated],
C.[Membership Enabled],
C.[Status],
C.[Is Admin],
C.[Terms Of Use Accepted],
[Member],
[Membership level ID],
[Archived],
[Event registrant],
[Suspended member],
[Event announcements],
[Member emails and newsletters],
[Email delivery disabled],
[Email delivery disabled automatically],
[Receiving emails disabled],
[Balance],
[Registered for specific event],
[Profile last updated by],
[Creation date],
[Last login date],
[Administrator role],
[Notes],
[Member ID],
[Address Line 1],
[Address Line 2],
[City],
[State],
[Zip Code],
[Country],
[Phone],
[E-Mail],
[Interested in volunteering with APRA-IL?],
[Volunteering Interest],
[Anything else we should know?],
[Member since],
[Renewal due],
[Renewal date last changed],
[Level last changed],
[Membership status],
[Years in Prospect Development],
[What track do you identify with most in regards to your daily work?],
[What track are you most interested in for programming?]

GO


