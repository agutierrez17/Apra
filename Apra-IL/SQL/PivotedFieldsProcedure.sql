CREATE PROCEDURE [dbo].[Pivot_Contact_Fields] AS 

-- Drop table if exists
IF OBJECT_ID('dbo.[Contact_Field_Values_Pivoted]', 'U') IS NOT NULL 
  DROP TABLE dbo.[Contact_Field_Values_Pivoted]; 

-- Pivot table with one row and five columns
SELECT 
[Contact ID],
[Archived],
[Donor],
[Event registrant],
[Member],
[Suspended member],
[Event announcements],
[Member emails and newsletters],
[Email delivery disabled],
[Email delivery disabled automatically],
[Receiving emails disabled],
[Balance],
[Total donated],
[Registered for specific event], 
[Profile last updated], 
[Profile last updated by], 
[Creation date], 
[Last login date], 
[Administrator role], 
[Notes], 
[Terms of use accepted], 
[Subscription source], 
[Member ID], 
[First Name], 
[Last Name], 
[Preferred Pronouns], 
[Title], 
[Organization], 
[Organization Type], 
[Address Line 1], 
[Address Line 2], 
[City], 
[State], 
[Zip Code], 
[Country], 
[Phone], 
[E-Mail], 
[Website], 
[Twitter Handle], 
[Interested in volunteering with APRA-IL?], 
[Volunteering Interest], 
[Anything else we should know?], 
[Member role], 
[Member since], 
[Renewal due], 
[Membership level ID], 
[Access to profile by others], 
[Renewal date last changed], 
[Level last changed], 
[Bundle ID], 
[Membership status], 
[Membership enabled], 
[Group participation], 
[Years in Prospect Development], 
[What track do you identify with most in regards to your daily work?], 
[What track are you most interested in for programming?]
INTO DBO.[Contact_Field_Values_Pivoted]
FROM (
    SELECT 
    CFV.[Contact ID],
	CF.[Field Name],
	CASE 
	WHEN C.[Contact ID] IS NOT NULL THEN C.[Display Name]
	WHEN ML.[Level ID] IS NOT NULL THEN ML.[Level Name]
	WHEN FV.[Value ID] IS NOT NULL THEN FV.[Value Label] 
	ELSE REPLACE(CFV.Value,'[]','') END AS "Value"
    FROM DBO.Contact_Field_Values CFV WITH (NOLOCK)
	INNER JOIN DBO.Contact_Fields CF WITH (NOLOCK) ON CFV.[System Code] = CF.[System Code]
	LEFT OUTER JOIN DBO.Field_Values FV WITH (NOLOCK) ON CF.[Field ID] = FV.[Field ID] AND CFV.Value = FV.[Value ID]
	LEFT OUTER JOIN DBO.Membership_Levels ML WITH (NOLOCK) ON CFV.Value = ML.[Level ID] AND CF.[Field Name] = 'Membership level ID'
	LEFT OUTER JOIN DBO.Contacts C WITH (NOLOCK) ON CFV.Value = C.[Contact ID] AND CF.[Field Name] = 'Profile last updated by'
) AS SourceTable
PIVOT (
    MIN([Value])
	FOR [Field Name] IN (
	[Archived],
	[Donor],
	[Event registrant],
	[Member],
	[Suspended member],
	[Event announcements],
	[Member emails and newsletters],
	[Email delivery disabled],
	[Email delivery disabled automatically],
	[Receiving emails disabled],
	[Balance],
	[Total donated],
	[Registered for specific event], 
	[Profile last updated], 
	[Profile last updated by], 
	[Creation date], 
	[Last login date], 
	[Administrator role], 
	[Notes], 
	[Terms of use accepted], 
	[Subscription source], 
	[Member ID], 
	[First Name], 
	[Last Name], 
	[Preferred Pronouns], 
	[Title], 
	[Organization], 
	[Organization Type], 
	[Address Line 1], 
	[Address Line 2], 
	[City], 
	[State], 
	[Zip Code], 
	[Country], 
	[Phone], 
	[E-Mail], 
	[Website], 
	[Twitter Handle], 
	[Interested in volunteering with APRA-IL?], 
	[Volunteering Interest], 
	[Anything else we should know?], 
	[Member role], 
	[Member since], 
	[Renewal due], 
	[Membership level ID], 
	[Access to profile by others], 
	[Renewal date last changed], 
	[Level last changed], 
	[Bundle ID], 
	[Membership status], 
	[Membership enabled], 
	[Group participation], 
	[Years in Prospect Development], 
	[What track do you identify with most in regards to your daily work?], 
	[What track are you most interested in for programming?]
	)
) AS PivotTable

GO