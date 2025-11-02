
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


