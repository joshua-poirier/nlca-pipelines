CREATE EXTERNAL TABLE IF NOT EXISTS `silver`.`wells` (
    `id` string,
    `api10` string,
    `direction` string,
    `wellname` string,
    `welltype` string,
    `operator` string,
    `basin` string,
    `subbasin` string,
    `state` string,
    `county` string,
    `spuddate` date,
    `cum12moil` float,
    `cum12mgas` float,
    `cum12mwater` float
)
COMMENT "silver wells"
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
    'field.delim' = '|'
)
STORED AS 
    INPUTFORMAT 'org.apache.hadoop.mapred.TextInputFormat' 
    OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION 's3://nlca-silver/data/'
TBLPROPERTIES (
    'classification' = 'csv',
    'skip.header.line.count'='1'
);
