SELECT      basin,
            SUM(cum12moil) AS cum12moil,
            SUM(cum12mgas) AS cum12mgas,
            SUM(cum12mwater) AS cum12mwater
FROM        silver.wells
GROUP BY    basin;
