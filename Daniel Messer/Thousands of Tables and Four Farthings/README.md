Resources related to two presentations featured in the Great ILS-Data Pre-Conference at IUG 2026

Held April 12, 2026 in Chicago

---

Daniel Messer\
Integrated Library Systems Administrator\
Library Systems & Services

daniel.messer@lsslibraries.com

# Thousands of Tables and Four Farthings

## Hacking Your Way to a Better Report

In the midst of building a centralized data server, we ran into an issue with a report that the Finance Department had been running for years. Nothing was wrong with the report, the problem came about from the *way* they were running it. This new data server is going to need that report, but they're not going to be able to run it the same way. Okay, so we'll rebuild it. But first things first... where does the data come from, how is it pulled from the database, where is the report file, and how does it work?

Time for a little old school tracking and hacking.

### Resources

**[How to trace SQL queries with MSSQL Profiler](https://support.docuware.com/en-US/knowledgebase/article/KBA-36926)** - A quick and easy walkthrough to guide you through setting up and using SQL Server Profiler to create traces.

**[Quickstart: Extended Events](https://learn.microsoft.com/en-us/sql/relational-databases/extended-events/quick-start-extended-events-in-sql-server?view=sql-server-ver17)** - An overview of what Extended Events does and how to use it.

* **Create Lss.Rpt_InvoicePrinting Sproc.sql** - The query used to create a stored procedure that leverages three other stored procedures in the Polaris database to power a modified vouchers report.
* **Vouchers1.rdl** - A modified version of the original vouchers report that works with our custom query.
* **VourcherLines.rdl** - A necessary subreport for Vouchers1.rdl