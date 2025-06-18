CREATE VIEW [dbo].[JobPostingsEmailHTML] AS

SELECT
'<tr><td align="left" style="background:transparent;font-size:0px;padding:0px;word-break:break-word;">' +
'<div style="font-family:Arial, Helvetica, sans-serif;font-size:16px;line-height:1;text-align:left;color:#000000;"><ul style="line-height: 21px;">' +
REPLACE(REPLACE(REPLACE(REPLACE(
STUFF((
SELECT TOP 10 ' ' +
'<li><font face="Georgia" color="#2E4261" style="font-size: 14px;"><strong><u><a href="' + RTRIM([Link]) + 
'" target="_blank">' + RTRIM([Job Title]) + 
'</a></u></strong> - ' + RTRIM([Organization]) + '</font></li>'

FROM dbo.[JobPostings] WITH (NOLOCK)
WHERE [Active] = 'Y'
ORDER BY [Date Posted] DESC
FOR XML PATH('')), 1, 1, ''),'&lt;','<'),'&gt;','>'),'&nbsp;',' '),'&amp;','&') + '</ul></div></td></tr>'
AS HTML

GO