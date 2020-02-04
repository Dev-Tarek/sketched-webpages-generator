if __package__ is None or __package__ == '':
    from COMPONENT_COLORS import *
else:
    from .COMPONENT_COLORS import *

COMPONENT_LEVELS = [
    {
        'button': BUTTON,
        'text': TEXT,
        'nav-brand': NAVBAR_BRAND,
        'nav-link': NAV_LINK,
        'large-title': LARGE_TITLE,
        'med-title': MED_TITLE,
        'list-group-item_0': LIST_GROUP_ITEM_0,
        'list-group-item_1': LIST_GROUP_ITEM_1,
        'list-group-item-text': LIST_GROUP_ITEM_TEXT,
        'hr': HR,
    },
    {
         'img': IMAGE,
         'card-header': CARD_HEADER,
         'card-body': CARD_BODY,
         'card-footer': CARD_FOOTER,
    },
    {
        'carousel': CAROUSEL,
        'card-div': CARD_LAYOUT,
        'list-group': LIST_GROUP,
        'header': HEADER,
        'jumbotron': JUMBOTRON,
        'navbar': NAVBAR,
        'footer': FOOTER,
    },
]