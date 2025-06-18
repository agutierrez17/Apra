CREATE VIEW [dbo].[APRA_HTML] AS

SELECT 
J.HTML AS JobPostingsPage, 
E.HTML AS JobPostingsEmail,
C.HTML AS ChapterEvents
FROM dbo.JobPostingsPageHTML J WITH (NOLOCK), 
	dbo.JobPostingsEmailHTML E WITH (NOLOCK),
	dbo.ChapterEventsHTML C WITH (NOLOCK)
GO