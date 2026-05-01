use academicworld;

-- -----------------------------------------------------------------
-- part 1: create indexes
-- these indexes help speed up common queries in the project.
-- idempotent: drop index if exists, then create index (safe to re-run).
-- requires mysql 8.0+ (drop index if exists).
-- -----------------------------------------------------------------
drop index if exists idx_keyword_name on keyword;
create index idx_keyword_name on keyword(name);

drop index if exists idx_publication_year on publication;
create index idx_publication_year on publication(year);

drop index if exists idx_faculty_pub_faculty on faculty_publication;
create index idx_faculty_pub_faculty on faculty_publication(faculty_id);

drop index if exists idx_pub_kw_pub on publication_keyword;
create index idx_pub_kw_pub on publication_keyword(publication_id, keyword_id);

-- -----------------------------------------------------------------
-- part 2: create a view for university keyword statistics
-- this view shows how many publications are related to each keyword
-- in each university.
-- -----------------------------------------------------------------
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

-- -----------------------------------------------------------------
-- part 3: create tables for widget 9
-- favorite_professors stores the current favorite professors
-- favorite_log stores add/remove history
-- -----------------------------------------------------------------
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
