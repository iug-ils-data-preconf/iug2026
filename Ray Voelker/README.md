Resources related to two presentations featured in the Great ILS-Data Pre-Conference at IUG 2026\
Held April 12, 2026 in Chicago

Ray Voelker\
Integrated Library Systems Administrator\
Cincinnati & Hamilton County Public Library\
ray.voelker@chpl.org

Slides for all presentations: [rayvoelker.github.io/iug2026](https://rayvoelker.github.io/iug2026/)

---

# I ❤️ Datasette: A Tool for Exploring and Publishing (Library) Data

Datasette is a free and open-source platform designed by Simon Willison to make it easier to share and publish data. At CHPL, we use Datasette to power collection analysis tools and to preserve a century of newspaper indexing history (the Newsdex project). This session demos both and shows how you can go from ILS data to a browsable, queryable web tool for about $5/month.

**Slides:** [I ❤️ Datasette: Collection Analysis & the Newsdex Project](https://rayvoelker.github.io/iug2026/talk-combined-datasette-at-the-library.html)

## Resources

* [collection-analysis.cincy.pl](https://collection-analysis.cincy.pl/) — CHPL Collection Analysis (live)
* [newsdex.chpl.org](https://newsdex.chpl.org/) — Newsdex newspaper index (live search)
* [chpl.org/blogs/post/newsdex-upgrade](https://chpl.org/blogs/post/newsdex-upgrade/) — The Full Newsdex Story (blog post)
* [datasette.io](https://datasette.io/) — Datasette
* [github.com/cincinnatilibrary/collection-analysis](https://github.com/cincinnatilibrary/collection-analysis) — Collection Analysis source code
* [github.com/cincinnatilibrary/newsdex](https://github.com/cincinnatilibrary/newsdex) — Newsdex source code
* [github.com/cincinnatilibrary](https://github.com/cincinnatilibrary) — CHPL on GitHub

---

# Data Lakes/Warehouses and Storing Data Extracts

Library data never sits still — and it lives in more places than you think. This session introduces the data lake concept for libraries: using DuckDB, DuckLake, and Apache Parquet to build an inexpensive, versioned repository of your library data. We look at early experiments at CHPL including an open-source Sierra MARC harvester and an OverDrive checkout ETL.

**Slides:** [Building a Data Lake for Your Library](https://rayvoelker.github.io/iug2026/talk-datalake-building-a-data-lake.html)

## Resources

* [github.com/chimpy-me/ils-lake](https://github.com/chimpy-me/ils-lake) — sierra-marc-harvest (open source Sierra MARC extraction CLI)
* [github.com/cincinnatilibrary/chpl-etl-overdrive-checkouts](https://github.com/cincinnatilibrary/chpl-etl-overdrive-checkouts) — OverDrive checkout ETL
* [duckdb.org](https://duckdb.org/) — DuckDB
* [ducklake.select](https://ducklake.select/) — DuckLake (open data lake format)
* [parquet.apache.org](https://parquet.apache.org/) — Apache Parquet
