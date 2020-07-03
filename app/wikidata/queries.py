correct_answer_query = """
    SELECT
      ?entity (SAMPLE(?description) AS ?entityDescription) (SAMPLE(?label) AS  ?entityLabel)
    WHERE {{
      wd:{entity} wdt:{property} ?entity.
      ?entity rdfs:label ?label . 
      OPTIONAL {{?entity schema:description ?description.}}
      FILTER (langMatches( lang(?label), "{language}" ))
      FILTER (langMatches( lang(?description), "{language}" ))
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "{language}". }}
    }}
    GROUP BY ?entity
"""

distractors_query = """
    SELECT DISTINCT ?entity ?entityLabel ?entityDescription
    WHERE {{
      ?subject wdt:{property} ?entity.
      FILTER NOT EXISTS {{
        wd:{entity} wdt:{property} ?entity.
      }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "{language}".}}
    }}
    LIMIT 3
"""

additional_info_query = """
SELECT ?entityType ?entityImage
WHERE {
  wd:%s wdt:P31 ?entityType.
  wd:%s wdt:P18 ?entityImage.
}
LIMIT 5
"""

label_query = """
    SELECT DISTINCT * WHERE {
      wd:%s rdfs:label ?label . 
      FILTER (langMatches( lang(?label), "%s" ) )  
    }
"""