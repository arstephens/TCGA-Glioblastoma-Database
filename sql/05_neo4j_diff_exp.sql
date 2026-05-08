SELECT
    g.gene_id,
    g.hugo_symbol,
    g.entrez_gene_id,

    AVG(CASE 
            WHEN s.expression_subtype = 'Classical' 
            THEN me.expression_value_mrna 
        END) AS mean_classical_expression,

    AVG(CASE 
            WHEN s.expression_subtype = 'Proneural' 
            THEN me.expression_value_mrna 
        END) AS mean_proneural_expression,

    COUNT(CASE 
            WHEN s.expression_subtype = 'Classical' 
            THEN 1 
        END) AS classical_sample_count,

    COUNT(CASE 
            WHEN s.expression_subtype = 'Proneural' 
            THEN 1 
        END) AS proneural_sample_count,

    LOG2(
        (AVG(CASE 
                WHEN s.expression_subtype = 'Classical' 
                THEN me.expression_value_mrna 
             END) + 1)
        /
        (AVG(CASE 
                WHEN s.expression_subtype = 'Proneural' 
                THEN me.expression_value_mrna 
             END) + 1)
    ) AS log2_fold_change,

    CASE
        WHEN LOG2(
            (AVG(CASE 
                    WHEN s.expression_subtype = 'Classical' 
                    THEN me.expression_value_mrna 
                 END) + 1)
            /
            (AVG(CASE 
                    WHEN s.expression_subtype = 'Proneural' 
                    THEN me.expression_value_mrna 
                 END) + 1)
        ) > 0
        THEN 'Higher in Classical'

        WHEN LOG2(
            (AVG(CASE 
                    WHEN s.expression_subtype = 'Classical' 
                    THEN me.expression_value_mrna 
                 END) + 1)
            /
            (AVG(CASE 
                    WHEN s.expression_subtype = 'Proneural' 
                    THEN me.expression_value_mrna 
                 END) + 1)
        ) < 0
        THEN 'Higher in Proneural'

        ELSE 'No difference'
    END AS expression_direction

FROM mrna_expression me
JOIN sample s
    ON me.sample_id = s.sample_id
JOIN gene g
    ON me.gene_id = g.gene_id

WHERE s.expression_subtype IN ('Classical', 'Proneural')

GROUP BY
    g.gene_id,
    g.hugo_symbol,
    g.entrez_gene_id

HAVING
    classical_sample_count >= 3
    AND proneural_sample_count >= 3
    AND ABS(log2_fold_change) >= 1

ORDER BY ABS(log2_fold_change) DESC

LIMIT 100;