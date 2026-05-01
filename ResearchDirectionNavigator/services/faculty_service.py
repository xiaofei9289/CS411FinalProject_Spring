from dash import html

from utils.common import to_int
from utils.mysql import (
    w04_get_faculty_profile_stats,
    w04_get_faculty_representative_papers,
    w04_get_faculty_top_collaborators,
    w04_get_faculty_top_keywords,
)

# load faculty profile by id
def get_widget04_faculty_profile(faculty_id):
    # if no faculty id is provided, return none
    if faculty_id is None:
        return None
    # convert the id to integer before using it in database query
    faculty_id=int(faculty_id)
    # get the basic profile stats from MySQL
    profile_stats=w04_get_faculty_profile_stats(faculty_id)
    if not profile_stats:
        return None
    # put all faculty data into one profile dictionary
    return {
        "faculty_id": faculty_id,
        "faculty_name": profile_stats.get("faculty_name") or "",
        "university_name": profile_stats.get("university_name") or "",
        "publication_count": to_int(profile_stats.get("publication_count"), default=0),
        "total_citations": to_int(profile_stats.get("total_citations"), default=0),
        "top_keywords": w04_get_faculty_top_keywords(faculty_id, limit=15),
        "top_collaborators": w04_get_faculty_top_collaborators(faculty_id, limit=10),
        "representative_papers": w04_get_faculty_representative_papers(faculty_id, limit=8),
    }

# turn store data into profile card
def build_widget04_profile_response(store_data, renderer):
    # if no faculty is selected
    if not store_data or store_data.get("faculty_id") is None:
        return None
    # get the faculty profile data
    faculty_profile=get_widget04_faculty_profile(store_data["faculty_id"])
    # show an error message if the faculty is not found
    if not faculty_profile:
        return html.P("Failed to find this faculty.", className="text-danger"), True
    return renderer(faculty_profile), True
