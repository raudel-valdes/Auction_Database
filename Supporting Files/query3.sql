SELECT count(*) as numberAuctions
FROM (
  SELECT itemID
  FROM CATEGORIES
  GROUP BY itemID
  HAVING count(itemID) = 4
)