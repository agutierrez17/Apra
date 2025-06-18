CREATE VIEW [dbo].[ChapterEventsHTML] AS

SELECT
'<div style="font-family:Arial, Helvetica, sans-serif;font-size:16px;line-height:1;text-align:left;color:#000000;"><ul style="margin-top: 0px !important;">' +
REPLACE(REPLACE(REPLACE(REPLACE(
STUFF((
SELECT TOP 6 ' ' +
'<li><font face="Georgia" color="#2E4261" style="font-size: 14px;"><strong>&nbsp;</strong><a href="' + [Link] + 
'" target="_blank"><strong>' + [Event Name] + ' (' + [Chapter Name] +')</strong></a>&nbsp;- ' + CONVERT(VARCHAR,CONVERT(DATE,[Date]),101) + '</font></li>' +
'<li style="list-style: none; display: inline"><ul style="margin-bottom: 1em !important;">' + 
'<li><span><font color="#2E4261" face="Georgia" style="font-size: 14px;"><em>' + [Description] + '</em></font></span></li></ul></li>'
FROM [dbo].[OtherChapterEvents] WITH (NOLOCK)
WHERE 
[Event Name] NOT LIKE '%Streaming Serenity%'
AND
([Location] LIKE '%Zoom%' OR [Location] LIKE '%virtual%' OR [Location] LIKE '%online%' OR [Location] LIKE '%Google Meet%')
AND
CONVERT(DATE,[Date]) > GETDATE()
ORDER BY CONVERT(DATE,[Date])
FOR XML PATH('')), 1, 1, ''),'&lt;','<'),'&gt;','>'),'&nbsp;',' '),'&amp;','&') + '</div>' AS HTML

GO