SELECT count(*) FROM (
  SELECT min
    , max
    , char
    , password
    , replace(password, char, '') as replaced
  FROM data
) processed
WHERE password != replaced
  AND length(password) - length(replaced) >= min
  AND length(password) - length(replaced) <= max

