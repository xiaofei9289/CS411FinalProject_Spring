"""Favorite professors: thin MySQL-backed helpers for W9."""

from utils.mysql import (
    w09_add_favorite_with_transaction,
    w09_list_favorites,
    w09_remove_favorite_with_transaction,
    w09_search_faculty_by_name,
)


def search_faculty_by_name(name, limit=15):
    return w09_search_faculty_by_name(name, limit=limit)


def list_favorites():
    return w09_list_favorites()


def add_favorite(faculty_id):
    w09_add_favorite_with_transaction(faculty_id)


def remove_favorite(faculty_id):
    w09_remove_favorite_with_transaction(faculty_id)
