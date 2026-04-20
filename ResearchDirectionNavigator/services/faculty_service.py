"""Faculty-facing service layer used by W4."""

from dash import html

from utils.mysql import (
    w04_get_faculty_profile_stats,
    w04_get_faculty_representative_papers,
    w04_get_faculty_top_collaborators,
    w04_get_faculty_top_keywords,
)


def get_widget04_faculty_profile(faculty_id):
    if faculty_id is None:
        return None

    faculty_id=int(faculty_id)
    profile_stats=w04_get_faculty_profile_stats(faculty_id)
    if not profile_stats:
        return None

    return {
        "faculty_id": faculty_id,
        "faculty_name": profile_stats.get("faculty_name") or "",
        "university_name": profile_stats.get("university_name") or "",
        "publication_count": int(profile_stats.get("publication_count") or 0),
        "total_citations": _safe_int(profile_stats.get("total_citations")),
        "top_keywords": w04_get_faculty_top_keywords(faculty_id, limit=15),
        "top_collaborators": w04_get_faculty_top_collaborators(faculty_id, limit=10),
        "representative_papers": w04_get_faculty_representative_papers(faculty_id, limit=8),
    }


def build_widget04_profile_response(store_data, renderer):
    if not store_data or store_data.get("faculty_id") is None:
        return None

    profile_payload=get_widget04_faculty_profile(store_data["faculty_id"])
    if not profile_payload:
        return html.P("fail to find this faculty", className="text-danger"), True
    return renderer(profile_payload), True


def _safe_int(value):
    try:
        return int(value) if value is not None else 0
    except (TypeError, ValueError):
        return 0
