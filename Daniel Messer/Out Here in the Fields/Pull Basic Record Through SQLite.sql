SELECT
    b.title AS [Title],
    a.name AS [Author],
    s.name AS [Series],
    b.series_index AS [Series Position],
    p.name AS [Publisher],
	DATE(b.pubdate) AS [Pub Date],
    GROUP_CONCAT(i.type || ': ' || i.val, ' | ') AS [Identifiers],
    c.text AS [Summary]
FROM
    books b
LEFT JOIN -- Pull the standard author name
    authors a ON (a.sort = b.author_sort)
LEFT JOIN -- Pull the ID to get the series
    books_series_link bsl ON (bsl.book = b.id)
LEFT JOIN -- Use the above ID to pull the series name
    series s ON (s.id = bsl.series)
LEFT JOIN -- Pull the ID to get the publisher
    books_publishers_link bpl ON (bpl.book = b.id)
LEFT JOIN -- Pull the ID to get the publisher's name
    publishers p ON (p.id = bpl.publisher)
LEFT JOIN -- Pull the summary and comments
    comments c ON (c.book = b.id)
LEFT JOIN -- Pull the IDs to get any identifiers
    identifiers i ON (i.book = b.id)
WHERE -- Enter the book id below (from the books table)
    b.id = 137
GROUP BY
    b.id,
	b.title, 
	a.name, 
	s.name, 
	b.series_index, 
	p.name,
	c.text
