SELECT a.value * b.value * c.value AS product
     , a.value as a
     , b.value as b
     , c.value as c
FROM data a, data b, data c
WHERE a.rowid NOT IN (b.rowid, c.rowid)
  AND b.rowid NOT IN (a.rowid, c.rowid)
  AND a.value + b.value + c.value = 2020
LIMIT 1
