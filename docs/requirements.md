# Requirements

Fill this in before writing code. Keep each requirement short and testable: if you can't imagine a test for it, rewrite it.

## Problem statement

Data Analysts normally rewrite the same code in different variations to load new datasets. duckpipe is mean to solve that, duckpipe can load any type of dataset that DuckDB can read, then checks the data, cleans it with SQL and exports the results, while all being driven by one config file and SQL rather than new Python.

The first project built on duckpipe analyses how Airbnb in New York City changed after Local Law 18, which began enforcement in Sept. 2023

## Users

| ID | User | What they need |
| --- | --- | --- |
| U1 | A Data Analysis setting up a dataset | Load, check and clean new data without writing new Python |
| U2 | A reviewer or hiring manager | Read the code, rebuild the results with one command, trust the findings |
| U3 | a future user of duckpipe | Add a file format, check or output with editing the existing classes |

## Business questions (Airbnb project)

<!-- The questions your analysis must answer. You listed five at the start; refine them here. -->

1. Did listings change from short stays to 30+ night minimums after Sept. 2023?
2. Did entire home listings lower compared to private rooms?
3. Did hosts with several listings leave the market, or adapt?
4. Which boroughs and neighbourhoods change the most?
5. What drives today's prices: area, type, size or ratings

## Functional requirements

<!-- What the system must do. Number them so issues and pull requests can refer to them. -->

| ID | Requirement | Covered by |
| --- | --- | --- |
| FR1 | | |

## Non-functional requirements

<!-- Qualities: security, reproducibility, testability, performance, privacy. -->

| ID | Requirement | Covered by |
| --- | --- | --- |
| NFR1 | | |

## Out of scope

<!-- What this project deliberately does NOT do, e.g. scheduling, a web UI. -->

-
