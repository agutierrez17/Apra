USE [APRA-IL]
GO

/****** Object:  StoredProcedure [dbo].[Delete_Future_Events]    Script Date: 2/13/2025 3:43:51 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO


CREATE PROCEDURE [dbo].[Delete_Recent_Emails] AS

----- DELETE FROM LINK CLICKS TABLE
DELETE LC
FROM dbo.LinkClicks LC WITH (NOLOCK) 
INNER JOIN dbo.EmailRecipients ER WITH (NOLOCK) ON ER.[Email ID] = LC.[Email ID] AND ER.[Contact ID] = LC.[Contact ID]
INNER JOIN dbo.Emails E WITH (NOLOCK) ON ER.[Email ID] = E.[Email ID]
WHERE
CONVERT(DATE,[Sent Date]) >= GETDATE() - 14

----- DELETE FROM EMAIL RECIPIENTS TABLE
DELETE ER
FROM dbo.EmailRecipients ER WITH (NOLOCK) 
INNER JOIN dbo.Emails E WITH (NOLOCK) ON ER.[Email ID] = E.[Email ID]
WHERE
CONVERT(DATE,[Sent Date]) >= GETDATE() - 14

----- DELETE FROM EMAILS TABLE
DELETE E
FROM dbo.Emails E WITH (NOLOCK)
WHERE
CONVERT(DATE,[Sent Date]) >= GETDATE() - 14

GO


