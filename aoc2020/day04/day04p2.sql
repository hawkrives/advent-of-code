SELECT *
FROM passports
WHERE byr IS NOT NULL
  AND byr >= '1920'
  AND byr <= '2002'
  AND iyr IS NOT NULL
  AND iyr >= '2010'
  AND iyr <= '2020'
  AND eyr IS NOT NULL
  AND eyr >= '2020'
  AND eyr <= '2030'
  -- height
  AND hgt IS NOT NULL
  -- ends in IN or CM and matches the constraints
  and case
          when hgt LIKE '%in' then substr(hgt, 1, 2) >= '59' and
                                   substr(hgt, 1, 2) <= '76' and
                                   substr(hgt, 3, 2) = 'in'
          when hgt LIKE '%cm' then substr(hgt, 1, 3) >= '150' and
                                   substr(hgt, 1, 3) <= '193' and
                                   substr(hgt, 4, 2) = 'cm'
          else false
    end
  -- hair color
  AND hcl IS NOT NULL
  -- AOC only gave me valid hex digits, if the string started with a hash
  AND hcl like '#%'
  and length(hcl) = 7
  -- eye color
  AND ecl IS NOT NULL
  AND ecl IN ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')
  -- check that PID exists
  AND pid IS NOT NULL
  -- check that they are length 9
  AND length(pid) == 9
  -- check that they are integers
  AND cast(pid as int) is not null
