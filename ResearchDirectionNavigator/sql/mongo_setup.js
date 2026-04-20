// MongoDB setup for Research Direction Navigator (academicworld).
// Run with:  mongosh academicworld sql/mongo_setup.js
// (The database is passed on the command line, so no `use academicworld;`
// helper is needed here — that helper is only valid in interactive mongosh.)
// All indexes below are non-_id indexes and count toward the "Indexing" database technique.

// W5 matches publications by keyword name (regex / $in on "keywords.name")
// and aggregates by year. These two indexes cover both steps.
db.publications.createIndex(
    { "keywords.name": 1 },
    { name: "idx_pub_keywords_name" }
);

db.publications.createIndex(
    { "year": 1 },
    { name: "idx_pub_year" }
);

// Compound index used when matching by keyword name first, then grouping by year.
db.publications.createIndex(
    { "keywords.name": 1, "year": 1 },
    { name: "idx_pub_keywords_name_year" }
);

// Display the indexes so the user can verify after running the script.
printjson(db.publications.getIndexes());
