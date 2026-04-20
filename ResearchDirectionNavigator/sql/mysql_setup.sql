use academicworld;

-- non-primary-key indexes; counted under the "Indexing" database technique.
-- note: MySQL does not support "create index if not exists", so this block
-- is meant to be run **once** on a fresh database. If the indexes already
-- exist, you can safely skip re-running this file (or drop the four indexes
-- manually first).
create index idx_keyword_name on keyword(name);
create index idx_publication_year on publication(year);
create index idx_faculty_pub_faculty on faculty_publication(faculty_id);
create index idx_pub_kw_pub on publication_keyword(publication_id, keyword_id);


drop view if exists university_keyword_stats;
create view university_keyword_stats as
select
    u.name as university_name,
    k.name as keyword_name,
    count(distinct p.id) as pub_count
from university u
join faculty f on f.university_id = u.id
join faculty_publication fp on fp.faculty_id = f.id
join publication p on p.id = fp.publication_id
join publication_keyword pk on pk.publication_id = p.id
join keyword k on k.id = pk.keyword_id
group by u.id, u.name, k.id, k.name;


-- widget 9: favorite professors manager
-- the first table stores the current favorites (one row per professor).
-- the second table is an append-only audit log used together with the
-- first table inside an explicit MySQL transaction (ADD / REMOVE).
create table if not exists favorite_professors (
    id int auto_increment primary key,
    faculty_id int not null,
    created_at timestamp default current_timestamp,
    constraint uq_fav_faculty unique (faculty_id),
    constraint fk_fav_faculty foreign key (faculty_id)
        references faculty(id) on delete cascade
);

create table if not exists favorite_log (
    id int auto_increment primary key,
    faculty_id int not null,
    action enum('ADD','REMOVE') not null,
    ts timestamp default current_timestamp
);
