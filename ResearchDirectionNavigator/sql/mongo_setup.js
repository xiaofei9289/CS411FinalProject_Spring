// this file creates indexes for the publications collection.
// these indexes help MongoDB search data faster in Widget 5.

// create an index for keyword names in publications.
// this helps when we search papers by keyword.
db.publications.createIndex(
    { "keywords.name": 1 },
    { name: "keyword_name_index" }
);

// create an index for the year field.
// this helps when we count papers by year.
db.publications.createIndex(
    { year: 1 },
    { name: "year_index" }
);

// Create a compound index for keyword name and year.
// This helps when we first search by keyword and then group the matched papers by year.
db.publications.createIndex(
    { "keywords.name": 1, year: 1 },
    { name: "keyword_year_index" }
);

// Widget 8 stores saved papers in a separate collection.
// One publication should appear only once in the favorite list.
db.favorite_publications.createIndex(
    { publication_id: 1 },
    { name: "favorite_publication_unique", unique: true }
);

// This helps the favorite list load in most-recently-edited order.
db.favorite_publications.createIndex(
    { updated_at: -1, created_at: -1 },
    { name: "favorite_publication_recent_index" }
);

// Display the indexes so the user can verify after running the script.
printjson(db.publications.getIndexes());
printjson(db.favorite_publications.getIndexes());
