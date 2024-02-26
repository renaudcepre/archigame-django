from django import template

register = template.Library()


@register.filter(name='get_button_color')
def get_button_color(value):
    """Retourne les classes de couleur Tailwind en fonction de la valeur donnée."""
    colors = {
        'transparent': 'bg-blue-600 hover:bg-blue-700 focus:ring-blue-500',
        'validation': 'bg-green-600 hover:bg-green-700 focus:ring-green-500',
        'delete': 'bg-red-600 hover:bg-red-700 focus:ring-red-500',
    }
    return colors.get(value, 'bg-blue-600 hover:bg-blue-700 focus:ring-blue-500')
