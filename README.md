# nlca-pipelines
[![python](https://img.shields.io/badge/Python-3.10-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-blue)](https://github.com/pylint-dev/pylint)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat)](https://pycqa.github.io/isort/)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Coding Assignment
This coding assignment is an application that processes and validates an input file and
outputs a processed file according to the rules specified. There are three parts.

**Requirements**
- The input file includes tabular data in CSV format
- All columns will be of format number, string, categorical, or date
- Date columns will always be in _YYYY-MM-DD_ format
- Data may be missing or invalid
- The assignment is to identify and/or clean potentially problematic data
- Use any frameworks or libraries you prefer

### Part 1
- When called, process the input file and return a path to the processed output file
  - Processing may vary depending on data type
  - Eliminate invalid rows
    - Rows must have an **API10** column. If missing, filter out the entire row.
  - Eliminate invalid values
    - If a value is not the correct type, replace it with a null value
  - Replace missing values
    - Number or date: Replace each missing value with the mean value
    - Categorical: Replace each missing value with the most common value
    - String: Leave blank
  - Sort Output
    - Output normalized data in sorted order by **API10**
- The program should take arguments for input and output paths

### Part 2
Load the transformed data from **Part 1** into a database of your choice. For guidance,
this can be a local database like _sqlite_ or _duckdb_, or you can extend **Part 3**
below and either:
- Add a DB like postgres or mysql to a new _docker-compose_ file alongside your task
from **Part 1**
- An AWS managed resource like Athena

Query the new table to discover:
- The top 5 oil wells by _cum12moil_, sorted in descending order
- The sum of each of _cum12moil_, _cum12mgas_, and _cum12mwater_, by _basin_

### Part 3
Create a _Dockerfile_ and **IaC** source using the program from **Part 1** that would
create resources necessary to run an ECS Task or Batch Job. Use S3 for the input and
output files.
- Dockerize the Python code
- Using either Terraform, Pulumi, or AWS CDK, present source code that will deploy the
necessary resources in order to run the ECS Task or Batch Job
- Create a resource of your choice that will monitor and notify on potential issues with
running the job
- Show AWS cli command necessary to run the task or job with the input and output path
- Bonus points for demonstrating **IaC** resource creation and actually running the Task
or job
