/* This query pulls a fairly complete MARC record from the Polaris database. The data
that it doesn't pull includes calculated fields like the LDR and the 005 tag. */

DECLARE @BibID INT = 1863375

SELECT
    bt.TagNumber,
    bt.IndicatorOne,
    bt.IndicatorTwo,
    -- e.g.  $a Title of the work $b subtitle $c responsibility
    STRING_AGG('$' + bs.SubField + ' ' + bs.Data, ' ')
        WITHIN GROUP (ORDER BY bs.BibliographicSubfieldID) AS SubfieldData
FROM
    Polaris.Polaris.BibliographicRecords br WITH (NOLOCK)
LEFT JOIN
    Polaris.Polaris.BibliographicTags bt WITH (NOLOCK)
    ON bt.BibliographicRecordID = br.BibliographicRecordID
LEFT JOIN
    Polaris.Polaris.BibliographicSubfields bs WITH (NOLOCK)
    ON bs.BibliographicTagID = bt.BibliographicTagID
WHERE
    br.BibliographicRecordID = @BibID
GROUP BY
    bt.BibliographicTagID,
    bt.TagNumber,
    bt.IndicatorOne,
    bt.IndicatorTwo
ORDER BY
    bt.BibliographicTagID;