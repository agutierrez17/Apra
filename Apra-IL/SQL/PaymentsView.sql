CREATE VIEW dbo.[APRA-IL_Payments] AS

SELECT 
P.[Payment ID],
P.[Value] AS "Payment Amount",
P.[Created Date] AS "Payment Date",
P.[Payment Type],
P.[Contact ID],
C2.[Display Name] AS "Contact Name",
C2.[Last Name] AS "Contact Last Name",
C2.[First Name] AS "Contact First Name",
OC.[Corrected Org Name] AS "Contact Organization",
T.Name AS "Tender Type",
C.[Display Name] AS "Payment Created By",
[Comment],
I.[Invoice ID],
I.[Created Date] AS "Invoice Date",
I.[Order Type] as "Invoice Type",
I.Memo AS "Invoice Memo",
C3.[Display Name] AS "Invoice Created By"

FROM [APRA-IL].[dbo].[Payments] P WITH (NOLOCK)
LEFT OUTER JOIN dbo.PaymentAllocations PA WITH (NOLOCK) ON P.[Payment ID] = PA.[Payment ID]
LEFT OUTER JOIN dbo.Invoices I WITH (NOLOCK) ON PA.[Invoice ID] = I.[Invoice ID]
LEFT OUTER JOIN dbo.Contacts C WITH (NOLOCK) ON P.[Created By] = C.[Contact ID]
LEFT OUTER JOIN dbo.Tenders T WITH (NOLOCK) ON P.[Tender ID] = T.[Tender ID]
LEFT OUTER JOIN dbo.Contacts C2 WITH (NOLOCK) ON P.[Contact ID] = C2.[Contact ID]
LEFT OUTER JOIN dbo.Organization_Crosswalk OC WITH (NOLOCK) ON C2.Organization = OC.Organization
LEFT OUTER JOIN dbo.Contacts C3 WITH (NOLOCK) ON I.[Created By] = C3.[Contact ID]

GO