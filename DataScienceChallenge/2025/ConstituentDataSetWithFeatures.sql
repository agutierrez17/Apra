SELECT 
[CONSTITUENT_ID],
[MANAGED_PROSPECT],
[LIFETIME_GIVING],
[Donor],
[Major Donor],
[LIFETIME_GIFT_COUNT],
[FIRST_GIFT_DATE],
[LAST_GIFT_DATE],
[Years of Giving],

[LIFETIME_CRM_INTERACTIONS],
[Lifetime Visits],
[Lifetime Phone Calls],
[Lifetime Correspondences],

[Interactions L5Y],
[Visits L5Y],
[Phone Calls L5Y],
[Correspondences L5Y],
[Interactions Prior to First Gift],
[Visits Prior to First Gift],
[Phone Calls Prior to First Gift],
[Correspondences Prior to First Gift],

[Lifetime Video Emails Opened],
[Lifetime Video Emails Clicked],
[Lifetime Video Views],
[Lifetime Videos Started],
[Lifetime Videos Watched 25 Percent],
[Lifetime Videos Watched 50 Percent],
[Lifetime Videos Watched 75 Percent],
[Lifetime Videos Finished],
[Lifetime Video Shares to Facebook],

[L5Y Video Emails Opened],
[L5Y Video Emails Clicked],
[L5Y Video Views],
[L5Y Videos Started],
[L5Y Videos Watched 25 Percent],
[L5Y Videos Watched 50 Percent],
[L5Y Videos Watched 75 Percent],
[L5Y Videos Finished],
[L5Y Video Shares to Facebook],

[Before First Gift Video Emails Opened],
[Before First Gift Video Emails Clicked],
[Before First Gift Video Views],
[Before First Gift Videos Started],
[Before First Gift Videos Watched 25 Percent],
[Before First Gift Videos Watched 50 Percent],
[Before First Gift Videos Watched 75 Percent],
[Before First Gift Videos Finished],
[Before First Gift Video Shares to Facebook],

----- COMBINED CRM + VIDEO EMAILS
[LIFETIME_CRM_INTERACTIONS] + [Lifetime Video Views] + [Lifetime Video Shares to Facebook] AS "Lifetime Combined Interaction",
[Interactions L5Y] + [L5Y Video Views] + [L5Y Video Shares to Facebook] AS "L5Y Combined Interaction",
[Interactions Prior to First Gift] + [Before First Gift Video Views] + [Before First Gift Video Shares to Facebook] AS "Before First Gift Combined Interaction",


[FIRST_CRM_INTERACTION_DATE],
[LAST_CRM_INTERACTION_DATE],
[CAPACITY_ESTIMATE],
[CAPACITY_ESTIMATE_CLEAN],
[LIFETIME_GIVING_BAND],
[LIFETIME_GIVING_BAND_LOW],
[FIVE_YEAR_GIVING_BAND],
[FIVE_YEAR_GIVING_BAND_LOW],
[R_Score],
[F_Score],
[M_Score],
[RFM_Score_Sum],
[RFM_Segment]
FROM [Philanthropy].[Apra].[ConstituentsView]
WHERE
[Interactions L5Y] + [L5Y Video Views] + [L5Y Video Shares to Facebook] >= 1
AND
[CAPACITY_ESTIMATE_CLEAN] >= 50000
AND
[Donor] = 0

ORDER BY
[L5Y Combined Interaction] DESC