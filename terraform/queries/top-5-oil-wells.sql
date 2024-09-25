SELECT      api10,
            cum12moil
FROM        silver.wells
WHERE       welltype = 'OIL'
ORDER BY    cum12moil DESC
LIMIT       5;
