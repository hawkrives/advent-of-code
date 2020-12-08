SELECT count(*) FROM (
  SELECT pos1
    , pos2
    , char
    , password
    , substr(password, pos1, 1) as c1
    , substr(password, pos2, 1) as c2
  FROM data
) processed
WHERE (char = c1 AND char != c2)
   OR (char = c2 AND char != c1)

