import pandas as pd
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output

#sources : https://france-renov.gouv.fr/ https://www.statistiques.developpement-durable.gouv.fr/
#pas de dataset massif public qui donne ces infos donc estimations prises des sites ci-dessus

G_F_vers_D = 275; G_F_vers_C = 425; G_F_vers_B = 575; G_F_vers_A = 1000
E_D_vers_C = 225; E_D_vers_B = 400; E_D_vers_A = 750
C_vers_B = 175; C_B_vers_A = 650

PV_G_F_vers_D = 350; PV_G_F_vers_C = 600; PV_G_F_vers_B = 800; PV_G_F_vers_A = 1100
PV_E_D_vers_C = 200; PV_E_D_vers_B = 400; PV_E_D_vers_A = 600
PV_C_B_vers_A = 300; PV_C_vers_B = 100

COUTS_PV_MAP = {
    'G': {'D': (G_F_vers_D, PV_G_F_vers_D), 'C': (G_F_vers_C, G_F_vers_C), 'B': (G_F_vers_B, PV_G_F_vers_B), 'A': (G_F_vers_A, PV_G_F_vers_A)},
    'F': {'D': (G_F_vers_D, PV_G_F_vers_D), 'C': (G_F_vers_C, PV_G_F_vers_C), 'B': (G_F_vers_B, PV_G_F_vers_B), 'A': (G_F_vers_A, PV_G_F_vers_A)},
    'E': {'C': (E_D_vers_C, PV_E_D_vers_C), 'B': (E_D_vers_B, PV_E_D_vers_B), 'A': (E_D_vers_A, PV_E_D_vers_A)},
    'D': {'C': (E_D_vers_C, PV_E_D_vers_C), 'B': (E_D_vers_B, PV_E_D_vers_B), 'A': (C_B_vers_A, PV_C_B_vers_A)},
    'C': {'B': (C_vers_B, PV_C_vers_B), 'A': (C_B_vers_A, PV_C_B_vers_A)},
    'B': {'A': (C_B_vers_A, PV_C_B_vers_A)},
}



def analyser_renovation(classe_actuelle, surface_m2, prix_actuel):
    if classe_actuelle not in COUTS_PV_MAP:
        return HTML(f"<p style='color:red;'>Classe DPE '{classe_actuelle}' non supportée pour l'analyse des sauts.</p>")

    if surface_m2 <= 10 or prix_actuel <= 1000:
        return HTML("<p style='color:red;'>Veuillez saisir des valeurs réalistes pour la surface et le prix.</p>")

    resultats = []
    classes_cibles = COUTS_PV_MAP[classe_actuelle].keys()

    for cible in sorted(classes_cibles):
        # Correction d'une erreur dans le COUTS_PV_MAP (F->C)
        if classe_actuelle == 'F' and cible == 'C':
            cout_m2, pv_m2 = COUTS_PV_MAP['F']['C']
        else:
            cout_m2, pv_m2 = COUTS_PV_MAP[classe_actuelle][cible]

        cout_total_renovation = cout_m2 * surface_m2
        plus_value_totale = pv_m2 * surface_m2
        marge_nette = plus_value_totale - cout_total_renovation
        prix_apres_renovation = prix_actuel + plus_value_totale

        resultats.append({
            'Classe CIBLE': cible,
            'Coût Rénovation (€)': f"{cout_total_renovation:,.0f}".replace(',', ' '),
            'Plus-value Potentielle (€)': f"{plus_value_totale:,.0f}".replace(',', ' '),
            'Marge Nette Théorique (€)': f"{marge_nette:,.0f}".replace(',', ' '),
            'Prix Estimé post-travaux (€)': f"{prix_apres_renovation:,.0f}".replace(',', ' ')
        })

    df_resultat = pd.DataFrame(resultats)
    df_resultat.set_index('Classe CIBLE', inplace=True)

    conseil = ""
    df_marge_float = df_resultat['Marge Nette Théorique (€)'].str.replace(' ', '').astype(float)
    if df_marge_float.max() > 0:
        meilleure_marge = df_marge_float.max()
        meilleure_cible = df_marge_float.idxmax()
        conseil = f"Le meilleur conseil financier est de viser la classe **{meilleure_cible}** pour une marge nette théorique maximale de **{meilleure_marge:,.0f} €**."
    else:
        conseil = "Les plus-values estimées ne couvrent pas directement les coûts de rénovation. La rentabilité sera assurée par les économies d'énergie et l'amélioration du confort."

    html_output = f"<h3>Analyse Rénovation : {classe_actuelle} ({surface_m2} m²)</h3>"
    html_output += df_resultat.to_html(classes='table table-striped')
    html_output += f"<p style='margin-top: 15px;'>{conseil}</p>"
    return HTML(html_output)



input_classe = widgets.Dropdown(options=['G', 'F', 'E', 'D', 'C'], value='F', description='DPE Actuel :')
input_surface = widgets.IntSlider(min=20, max=200, step=10, value=80, description='Surface (m²) :')
input_prix = widgets.FloatText(value=250000.0, description='Prix actuel (€) :', step=10000.0)

bouton_analyser = widgets.Button(description="Analyser", button_style='success')
output_resultat = widgets.Output()
def on_button_clicked(b):
    with output_resultat:
        clear_output()
        display(analyser_renovation(
            input_classe.value,
            input_surface.value,
            input_prix.value
        ))
bouton_analyser.on_click(on_button_clicked)

widgets_entree_renovation = widgets.VBox([
    widgets.HBox([input_classe, input_surface, input_prix]),
    bouton_analyser,
    output_resultat
])

display(widgets_entree_renovation)
