SELECT count(*) as categoriesBidGreater100
FROM (
	SELECT category, max(b.amount)
	FROM CATEGORIES c , BIDS b
	WHERE  c.itemID = b.itemID
	GROUP BY category
	HAVING max(b.amount) > 100
)