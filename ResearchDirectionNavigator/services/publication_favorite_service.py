from utils.mongodb import (
    w08_add_favorite_publication_by_id,
    w08_list_favorite_publications,
    w08_remove_favorite_publication,
    w08_search_publications,
    w08_update_favorite_publication,
)


def search_publications_for_favorites(query_text, limit=10):
    return w08_search_publications(query_text, limit=limit)


def list_favorite_publications():
    return w08_list_favorite_publications()


def add_favorite_publication(publication_id):
    return w08_add_favorite_publication_by_id(publication_id)


def remove_favorite_publication(publication_id):
    return w08_remove_favorite_publication(publication_id)


def update_favorite_publication(publication_id, status, note):
    return w08_update_favorite_publication(publication_id, status, note)
