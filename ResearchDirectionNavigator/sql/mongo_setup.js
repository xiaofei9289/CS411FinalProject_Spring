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

// Display the indexes so the user can verify after running the script.
printjson(db.publications.getIndexes());
