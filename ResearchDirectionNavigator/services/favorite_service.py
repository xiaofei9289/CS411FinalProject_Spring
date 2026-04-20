from utils.mysql import (
    w09_add_favorite_with_transaction,
    w09_list_favorites,
    w09_remove_favorite_with_transaction,
    w09_search_faculty_by_name,
)

# define a function to search faculty by name for Widget 9
def search_faculty_by_name(name, limit=15):
    faculty_rows = w09_search_faculty_by_name(name, limit=limit)
    return faculty_rows

# define a function to get all favorite faculty
def list_favorites():
    favorite_rows = w09_list_favorites()
    return favorite_rows

# define a function to add one faculty to the favorite list
def add_favorite(faculty_id):
    w09_add_favorite_with_transaction(faculty_id)

# rdefine a fuction to emove one faculty from the favorite list
def remove_favorite(faculty_id):
    w09_remove_favorite_with_transaction(faculty_id)
