SELECT count(userID) as numberNewYorkers
FROM (
	SELECT userID
	FROM SELLERS
	WHERE user_location = 'New York'
	UNION
	SELECT userID
	FROM BIDDERS
	WHERE  user_location = 'New York'
)