WITH distinct_questions AS (
    SELECT group_id, count(distinct question) as questions
    FROM answer
    GROUP BY group_id
)
SELECT sum(questions)
FROM distinct_questions
;

-- drop index a;