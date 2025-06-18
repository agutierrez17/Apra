USE [APRA-IL]
GO

/****** Object:  View [dbo].[ContactsForUnsubscribe]    Script Date: 2/17/2025 3:20:47 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

ALTER VIEW [dbo].[ContactsForUnsubscribe] AS

SELECT DISTINCT
ER.[Contact ID],
[Recipient Name],
ER.Email,
ER.Organization,
E.[Email ID],
Subject,
[Sent Date],
[Is Opened],
CAST(LC.URL AS VARCHAR) AS URL,
Clicked,
ClicksCount,
AC.[Email delivery disabled],
AC.[Email delivery disabled automatically],
AC.[Receiving emails disabled],
AC.[Member emails and newsletters],
AC.[Event announcements],
CASE
WHEN Notes = '' THEN CONCAT('Unsubscribed from emails by Andrew Gutierrez on ',CAST(CONVERT(DATE,GETDATE()) AS VARCHAR))
ELSE CONCAT(Notes,CHAR(10),CHAR(10),'Unsubscribed from emails by Andrew Gutierrez on ',CAST(CONVERT(DATE,GETDATE()) AS VARCHAR)) END AS "Note"
FROM dbo.Emails E WITH (NOLOCK)
INNER JOIN dbo.EmailRecipients ER WITH (NOLOCK) ON E.[Email ID] = ER.[Email ID]
INNER JOIN dbo.LinkClicks LC WITH (NOLOCK) ON ER.[Email ID] = LC.[Email ID] AND ER.[Contact ID] = LC.[Contact ID]
INNER JOIN dbo.[APRA-IL_Contacts] AC WITH (NOLOCK) ON ER.[Contact ID] = AC.[Contact ID]

WHERE
LC.[URL] LIKE '%UNSUBSCRIBE%'
AND
[Sent Date] >= '2025-02-11'
AND
(AC.[Member emails and newsletters] = 'TRUE' OR AC.[Event announcements] = 'TRUE')

GO


