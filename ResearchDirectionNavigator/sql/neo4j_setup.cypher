// Neo4j setup for Research Direction Navigator (academicworld).
// Run with:
//   cat sql/neo4j_setup.cypher | cypher-shell -u neo4j -p <your_password> -d academicworld
// These statements contribute to BOTH "Indexing" and "Constraint" database techniques.

// --- Constraints (also create a backing index on the property) ---
// W5 filters graph nodes by FACULTY.id coming from MySQL; uniqueness also prevents duplicates.
CREATE CONSTRAINT faculty_id_unique IF NOT EXISTS
    FOR (f:FACULTY) REQUIRE f.id IS UNIQUE;

// KEYWORD.name is used in W5 overlap ranking; enforcing uniqueness guards the graph.
CREATE CONSTRAINT keyword_name_unique IF NOT EXISTS
    FOR (k:KEYWORD) REQUIRE k.name IS UNIQUE;

// --- Plain indexes for frequent lookups ---
// Range index on FACULTY.name (W7 collaboration network will look up by name).
CREATE INDEX faculty_name_idx IF NOT EXISTS
    FOR (f:FACULTY) ON (f.name);

// Range index on PUBLICATION.id (used when traversing faculty-publication edges).
CREATE INDEX publication_id_idx IF NOT EXISTS
    FOR (p:PUBLICATION) ON (p.id);

// Show all constraints and indexes so the user can verify.
SHOW CONSTRAINTS;
SHOW INDEXES;
