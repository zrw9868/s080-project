--replace this with your query
SELECT 
	CMTE_NM,
	cast(TTL_RECEIPTS as float) as TTL_RECEIPTS
FROM
	PAC_SUMMARY
WHERE
	CMTE_TP = 'O'
ORDER BY
	TTL_RECEIPTS
	desc
LIMIT 10;
