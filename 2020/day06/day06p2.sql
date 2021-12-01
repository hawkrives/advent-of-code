WITH group_sizes AS (
    SELECT group_id, group_concat(DISTINCT person_id) as people
    FROM answer
    GROUP BY group_id
),
     group_answers AS (
         SELECT group_id, question, group_concat(DISTINCT person_id) as people_answered
         FROM answer
         GROUP BY group_id, question
     )
SELECT count(*)
FROM group_answers a
         LEFT JOIN group_sizes s USING (group_id)
WHERE people_answered = people
