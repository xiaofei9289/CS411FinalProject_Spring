"""MySQL utilities: shared `core` plus per-widget modules (W1/W2/W3/W4/W5/W9).

Existing imports keep working: ``from utils.mysql import w01_search_papers_based_on_keywords`` etc.
"""

from .core import check_mysql_connection, get_mysql_config
from .w01 import w01_search_papers_based_on_keywords
from .w02 import (
    w02_get_all_information_about_selected_university,
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
from .w09 import (
    w09_add_favorite_with_transaction,
    w09_list_favorites,
    w09_remove_favorite_with_transaction,
    w09_search_faculty_by_name,
)

__all__ = [
    "check_mysql_connection",
    "get_mysql_config",
    "w01_search_papers_based_on_keywords",
    "w02_get_all_information_about_selected_university",
    "w02_get_all_university_names",
    "w02_get_university_w2_dashboard",
    "w03_get_comparision_information_among_universities",
    "w04_get_faculty_profile_stats",
    "w04_get_faculty_representative_papers",
    "w04_get_faculty_top_collaborators",
    "w04_get_faculty_top_keywords",
    "w05_mysql_get_faculty_ids_by_keyword",
    "w09_add_favorite_with_transaction",
    "w09_list_favorites",
    "w09_remove_favorite_with_transaction",
    "w09_search_faculty_by_name",
]
