// this file is used to prepare neo4j for our project
// we create some constraints and indexes here
// constraints help keep data correct
// indexes help make query faster
//

// create a unique constraint for faculty id
// each faculty should have only one id
CREATE CONSTRAINT faculty_id_unique IF NOT EXISTS
    FOR (f:FACULTY) REQUIRE f.id IS UNIQUE;

// create a unique constraint for keyword name
// each keyword name should appear only once
CREATE CONSTRAINT keyword_name_unique IF NOT EXISTS
    FOR (k:KEYWORD) REQUIRE k.name IS UNIQUE;

// create an index for faculty name
// this is useful when searching professor names
CREATE INDEX faculty_name_idx IF NOT EXISTS
    FOR (f:FACULTY) ON (f.name);

// create an index for publication id
// this is useful when locating a publication node
CREATE INDEX publication_id_idx IF NOT EXISTS
    FOR (p:PUBLICATION) ON (p.id);

// Show all constraints and indexes so the user can verify.
SHOW CONSTRAINTS;
SHOW INDEXES;
