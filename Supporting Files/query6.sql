SELECT count(*) as sellerAndBidder
FROM SELLERS s, BIDDERS b
WHERE s.userID == b.userID