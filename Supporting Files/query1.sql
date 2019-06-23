SELECT count(USERS.userID) as totalNumberUsers
FROM (
		SELECT userID
		FROM SELLERS
		UNION
		SELECT userID
		FROM  BIDDERS
) as USERS
