Resources related to two presentations featured in the Great ILS-Data Pre-Conference at IUG 2026

Held April 12, 2026 in Chicago

---

Daniel Messer\
Integrated Library Systems Administrator\
Library Systems & Services

daniel.messer@lsslibraries.com

# Out Here in the Fields
## Lessons Learned from a Different Database

You may not believe this, but there is an entire world of  library management systems outside of professional librarianship, each with their own databases and schemas that bring their own pros and cons. And get this: None of them use MARC. I mean, *can you imagine?!* Let’s take a quick walk through a project that manages bibliographic data in a  completely different way, and what we can take away from that.

### Resources

**[Calibre](https://calibre-ebook.com/)** - Free and open source eBook management software.

**[dbBrowser for SQLite](https://sqlitebrowser.org/)** - Free and open source SQLite database management.

**[SQLPro for SQLite](https://www.sqlitepro.com/)** - My preferred app for SQLite database management on macOS. Also available through [Setapp](https://setapp.com/apps/sqlpro-for-sqlite).

This repo includes a SQLite file called ```metadata.db```. This is the same database used during the talk and contains the metadata for the files discussed.

* **Pull Basic Record Through SQLite** - A SQLite query that pulls the basic metadata for a single bibliographic record within the Calibre database
* **View Basic MARC Record** - A T-SQL query you can run on the Polaris database to pull the basic MARC record straight from the database itself.
