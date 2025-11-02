# Widgets d'entrée
input_classe = widgets.Dropdown(options=['G', 'F', 'E', 'D', 'C'], value='F', description='DPE Actuel :')
input_surface = widgets.IntSlider(min=20, max=200, step=10, value=80, description='Surface (m²) :')
input_prix = widgets.FloatText(value=250000.0, description='Prix actuel (€) :', step=10000.0)

# Bouton de validation
bouton_analyser = widgets.Button(description="Analyser", button_style='success')

# Widget de sortie pour afficher le résultat
output_resultat = widgets.Output()

# Fonction de rappel (callback) pour le bouton
def on_button_clicked(b):
    with output_resultat:
        clear_output()
        display(analyser_renovation(
            input_classe.value,
            input_surface.value,
            input_prix.value
        ))

# Lier le bouton à la fonction de rappel
bouton_analyser.on_click(on_button_clicked)

# Affichage des widgets dans un VBox (conteneur vertical)
widgets_entree = widgets.VBox([
    widgets.HBox([input_classe, input_surface, input_prix]),
    bouton_analyser,
    output_resultat
])

display(widgets_entree)
