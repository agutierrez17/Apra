USE [APRA-IL]
GO

/****** Object:  StoredProcedure [dbo].[Update_Unsubscribed_Contacts]    Script Date: 2/17/2025 9:39:16 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

ALTER PROCEDURE [dbo].[Update_Unsubscribed_Contacts] 
@contact_id VARCHAR(50) 
AS

UPDATE CFT 
SET [Value] = CU.Note
FROM dbo.Contact_Field_Values CFT WITH (NOLOCK)
INNER JOIN dbo.ContactsForUnsubscribe CU WITH (NOLOCK) ON CFT.[Contact ID] = CU.[Contact ID]
WHERE 
CFT.[System Code] IN ('Notes')
AND
CFT.[Contact ID] = @contact_id


UPDATE CFT 
SET [Value] = 'False' 
FROM dbo.Contact_Field_Values CFT WITH (NOLOCK)
INNER JOIN dbo.ContactsForUnsubscribe CU WITH (NOLOCK) ON CFT.[Contact ID] = CU.[Contact ID]
WHERE 
CFT.[System Code] IN ('ReceiveNewsletters','ReceiveEventReminders')
AND
CFT.[Contact ID] = @contact_id

GO


