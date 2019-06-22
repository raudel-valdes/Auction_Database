SELECT itemID as acutionWithHighestPrice
FROM (
	SELECT itemID, MAX(current_price)
	FROM AUCTIONS
)