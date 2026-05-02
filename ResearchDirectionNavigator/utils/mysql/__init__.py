# mysql helpers for each widget

from .connection_config import get_mysql_config
from .w01 import w01_search_papers_based_on_keywords
from .w02 import (
    w02_get_all_university_names,
    w02_get_university_w2_dashboard,
)
from .w03 import w03_get_comparision_information_among_universities
from .w04 import (
    w04_get_faculty_profile_stats,
    w04_get_faculty_representative_papers,
    w04_get_faculty_top_collaborators,
    w04_get_faculty_top_keywords,
)
from .w05 import w05_mysql_get_faculty_ids_by_keyword
from .w06 import w06_get_faculty_candidates_by_topic
from .w09 import (
    w09_add_favorite_with_transaction,
    w09_list_favorites,
    w09_remove_favorite_with_transaction,
    w09_search_faculty_by_name,
)
