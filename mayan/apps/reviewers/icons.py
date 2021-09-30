from mayan.apps.appearance.classes import Icon
from mayan.apps.documents.icons import icon_document_list

icon_document_multiple_reviewer_multiple_attach = Icon(
    driver_name='fontawesome-dual', primary_symbol='tag',
    secondary_symbol='arrow-right'
)
icon_document_multiple_tag_multiple_remove = Icon(
    driver_name='fontawesome-dual', primary_symbol='tag',
    secondary_symbol='minus'
)
icon_document_reviewer_multiple_attach = Icon(
    driver_name='fontawesome-dual', primary_symbol='tag',
    secondary_symbol='arrow-right'
)
icon_document_reviewer_multiple_remove = Icon(
    driver_name='fontawesome-dual', primary_symbol='tag',
    secondary_symbol='minus'
)

icon_document_reviewer_remove_submit = Icon(
    driver_name='fontawesome', symbol='minus'
)
icon_document_reviewer_list = Icon(driver_name='fontawesome', symbol='tags')

icon_menu_reviewers = Icon(driver_name='fontawesome', symbol='tags')

icon_reviewer_create = Icon(
    driver_name='fontawesome-dual', primary_symbol='tag',
    secondary_symbol='plus'
)
icon_reviewer_delete = Icon(driver_name='fontawesome', symbol='times')
icon_reviewer_delete_submit = Icon(driver_name='fontawesome', symbol='times')
icon_reviewer_edit = Icon(driver_name='fontawesome', symbol='pen')
icon_reviewer_document_list = icon_document_list
icon_reviewer_list = Icon(driver_name='fontawesome', symbol='tag')
