# IUG 2026 - The Great ILS-Data Pre-Conference

## Out Here in the Fields

### Quick Introduction

* Hi, I'm Dan.
  * 30 years in libraries
  * Polaris ILS admin for Library Systems & Services
  * SQL Hacker

### MARC Sucks, I Know

- So look, if you know anything about me, you'll know that I loathe MARC
  - I mean, it was fine, for the late 1960s
  - Yeah, keep in mind that MARC, as a protocol, is over 60 years old
  - And while old ≠ broken, MARC remains a weird, obfuscated, obtuse, and otherwise difficult format to deal with
- Disclaimer, I'm one of those weirdos who believe that all aspects of the discovery tools, methods, and categorizations should be open and understandable to the reader
  - So it shouldn't be much of a surprise that I think the DDCS can strap an engine block around its waist and Wylie Coyote itself off a desert cliff
- But before I continue complaining about this stuff, I need to point out something to our Polaris users in the audience, that Bill Schickling and his original team of nerds did something incredibly profound, in that they figured out a way to “database-ize” a MARC record. 
  - Every time you open up a MARC record in Polaris, you are pulling data from multiple tables to build it. That MARC record doesn't exist as a singular entity in Polaris, it's scattered all over the place.
  - Turns out, you can build the basic MARC record with less than 30 lines of SQL.
- So yeah, that's great and everything, but MARC is still horrible. Don't even get me started on BIBFRAME
  - But surely there are other ways to catalogue bibliographic information? 
  - Yes, there are, and don't call me Shirley.

### A Better Way

- We're going to look at a database that handles bibliographic data. In other words, books.
  - But this could work for pretty much any other media as well.
- Instead of numbered tags, we're going to use descriptive identifiers.
  - So rather than declaring an ISBN in the 020 tag, subfield a, we're going to put it in a table and identify it as… ISBN.
  - We can do the same with the OCLC number. 
  - We can even use numbers not normally found in MARC records like Google IDs or ASINs. 
  - We could tag movies and TV shows with a TMDB or IMDB identifier and we'd call it out as such.
  - Rather than putting titles in a 240 or 245 tag, we'll put it under… Title.
  - Authors go under Author, not 100
- And while I've never found a specific name that everyone agrees on for this style of cataloguing, of the names I found, the one I liked the most was “pragmatic cataloguing.”

- We're still using a relational database, so yeah, things are still scattered all over the place, but you can still write the SQL that brings all of that together
  - With all that in mind, I'm going to talk about a bibliographic database system that has been in use for 19 years. The database itself is wide open, because the project is free and open source.

### Calibre

- Let's talk about Calibre.
- If you're not familiar, Calibre is a free and open source eBook management system. Created in 2006 by Kovid Goyal.
  - Calibre has become a sort of standard for eBook management for people who are really into collecting eBooks.
  - Now, fun fact, I've heard this name pronounced a few different ways, but the creator himself calls it Calibre.
    - I believe the name is kind of a portmanteau of catalogue and libre, which is a word that turns up in the free and open source community to me free as in speech, kinda like LibreOffice.
- Anyway, here's what it looks like, and yeah, it sure is a catalogue and you might be surprised how much it has in common with an ILS and we'll get into that

#### SQLite

- See, the database that powers Calbre is SQLite, which, as its name implies, is a lightweight SQL database. 
  - SQLite is everywhere, from your web browser to video games.
  - It's a good bet that almost every app on your phone uses some kind of SQLite database. 
  - The syntax for SQLite is a little different that T-SQL or Postgres, but if you can work in either of those, you'll pick up SQLite extremely quickly

#### Surprise! It's just copy cataloguing!

- But before we get into that, let's take a quick look at Calibre and how you add a record to it.
- Now, I've got my cyberpunk collection here and I'm gonna add a new book, in this case, a Shadowrun RPG sourcebook. Adding it easy, just drag it in, and there ya go.
  - But as you can see, Calibre doesn't really know anything about this book. It's got some basic metadata that it picked up from the PDF, but look at this item. It's got tags and IDs and all kinds of metadata. Thankfully there's an easy way to get this for our Shadowrun book too.
  - I'm going to tell Calibre to search for metadata on a couple of different external catalogues and bring in what it finds. Now, any cataloguers in the audience will recognize this immediately for what it is.
- It's copy cataloguing.
  - Instead of reaching out to the Library of Congress or OCLC, I'm reaching out to Amazon and OpenLibrary. I'm bringing in the data it finds and I can make adjustments as I see fit. 
  - Literally, this is copy cataloguing.
- Great. Now I've got all that delicious metadata. So… what's that look like in the database?

#### Turning Tables

- books - PK for the system
- authors - Notice that there isn't exactly an authority record, but it kinda works the same way
- comments - OMG ARE YOU KIDDING ME HTML FORMATTED CONTENT MARC WOULD FREAKIN' DIE
- series - Yes, this is still a pain, but not quite as big a pain as it is in MARC because in pragmatic cataloguing, it's easer to catalogue a series

*Note: Touch on custom columns*

 