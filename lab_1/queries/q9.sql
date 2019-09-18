--replace this with your query
SELECT
	INDIV_CONTRIB.STATE,
	SUM(TRANSACTION_AMT),
	SUM(TRANSACTION_AMT) / total_population as per_capita_indiv

FROM
	INDIV_CONTRIB,
	( SELECT
		state,
		SUM(population) AS total_population
	FROM 
		DIST_POP
	GROUP BY
		state
	) AS state_pop

WHERE
	INDIV_CONTRIB.STATE =state_pop.state 
	AND ENTITY_TP = 'IND'
	AND TRANSACTION_TP = '10'

GROUP BY
	INDIV_CONTRIB.STATE
	
ORDER BY
	per_capita_indiv DESC

LIMIT 
	5;
