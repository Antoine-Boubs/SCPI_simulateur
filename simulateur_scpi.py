import streamlit as st
import pandas as pd
import numpy_financial as npf
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import uuid
from datetime import date


st.set_page_config(
    layout="centered", 
    page_title="Simulateur SCPI", 
    page_icon="📊", 
    initial_sidebar_state="expanded", 
)

with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown(f"""
<div class="title-container">
    <h1 class="main-title">Simulateur SCPI</h1>
    <div class="separator"></div>
    <p class="subtitle">Investissez dans de l'immobilier professionnel à partir de 50 000€</p>
    <div class="info-container">
        <div class="update-info">Dernière mise à jour : 09/10/2024</div>
        <div class="author-info">Par Antoine Berjoan</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
         div[data-baseweb="tab"] > button {
            font-size: 8px; /* Taille du texte */
            font-weight: bold;
            color: #16425B; /* Couleur du texte */
            background-color: rgba(241, 216, 122, 0.3); /* Fond de couleur similaire */
            border-radius: 10px;
            padding: 10px 20px; /* Ajouter du padding pour l'espacement */
            border: 2px solid #16425B;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            margin: 5px; /* Espace entre les onglets */
        }

            
        div [data-baseweb="tab"] {
            background-color: #E8F0F2;
            border-radius: 10px;
            padding: 10px 15px;
            font-weight: bold;
            font-size: 18px;
            color: #16425B;
            margin-right: 5px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transition: background-color 0.3s ease;
        }

        [data-baseweb="tab"]:not([aria-selected="true"]) {
            background-color: #FBFBFB; 
            color: #202021; 
            box-shadow: 0px 4px 8px rgba(251, 251, 251, 0.8);;
            font-weight: 400; 
        }

        [data-baseweb="tab"]:hover {
            background-color: rgba(141, 179, 197, 0.2); 
            color: #202021;
            cursor: pointer;
        }

        [data-baseweb="tab-highlight"] {
            background-color: #16425b;
            height: 3px;
            border-radius: 2px;
        }
            
        div[data-baseweb="tab-border"][role="presentation"] {
            border: 1px solid #CBA325; 
            border-radius: 5px;
            margin: 10px;
        }
            
            
        .stSidebar .stHeading h2 {
            color: #16425B; 
            font-size: 20px; 
            font-weight: 700; 
            margin-top: -30px; /* Espace au-dessus */
            margin-bottom: 20px; /* Espace en dessous */
            text-align: center; 
            background-color: #'rgba(241, 216, 122)'; 
            padding: 10px 15px; /* Ajouter du padding pour l'espacement */
            border-radius: 10px; 
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
            
        .stMarkdown .stHeading h2 {
            color: #16425B; 
            font-size: 20px; 
            font-weight: 700; 
            margin-top: -30px; /* Espace au-dessus */
            margin-bottom: 20px; /* Espace en dessous */
            text-align: center; 
            background-color: #'rgba(241, 216, 122)'; 
            padding: 10px 15px; /* Ajouter du padding pour l'espacement */
            border-radius: 10px; 
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
    </style>
""", unsafe_allow_html=True)


def input_simulateur():
    with st.sidebar:
        st.header("📊 Paramètres d'investissement")
        
        with st.container():
            montant_investissement = st.number_input("💰 Montant investissement (€)", 0, 1000000, 100000, 1000)
            apport = st.number_input("💶 Apport (€)", min_value=0, max_value=montant_investissement, value=0, step=100)
            duree_pret = st.slider("🕒 Durée prêt (mois)", 0, 360, 300, 12)
            taux_interet = st.number_input("📈 Taux intérêt (%)", 0.0, 10.0, 4.96, 0.01) / 100
            taux_assurance = st.slider("🔒 Taux assurance (%)", 0.00, 1.0, 0.10, 0.01) / 100
        
        with st.container():
            type_differe = st.selectbox("⏳ Modalité du différé", ['Sans différé', 'Différé partiel', 'Différé total'])
            duree_differe = st.slider("⏲️ Durée différé (mois)", 0, 12, 9) if type_differe != 'Sans différé' else 0
        
        with st.container():
            frais_courtage = st.number_input("💵 Frais courtage / dossier (€)", 0, 10000, 0, 250)
            if frais_courtage > 0:
                inclus_financement = st.checkbox("Inclus dans le financement ?", help='Les frais de dossiers / courtage sont-ils inclus dans votre financement ?')
            else:
                inclus_financement = False
        
        with st.container():
            rendement_souhaite = st.slider("📈 Rendement locatif (%)", 1.0, 10.0, 5.0, 0.1) / 100
            delai_jouissance = st.slider("🕒 Délai de jouissance (mois)", 0, 12, 6)
            taux_revalorisation = st.slider("📊 Taux de revalorisation (%)", 0.0, 5.0, 1.0, 0.1) / 100
            frais_souscription = st.slider("💸 Frais de souscription (%)", 0.0, 20.0, 12.0, 0.5) / 100
            taux_imposition = st.select_slider("🚥 Taux d'imposition (TMI)",options=[0, 11, 30, 41, 45],value=30)/100
        
        with st.container():
            investissement_etranger = st.checkbox("Investissement en SCPI étrangères ?")
            pourcentage_etranger = st.slider("% SCPI étrangère", 0, 100, 50, 1) if investissement_etranger else 0
        
    return {
        "montant_investissement": montant_investissement,
        "apport": apport,
        "duree_pret": duree_pret,
        "taux_interet": taux_interet,
        "taux_assurance": taux_assurance,
        "type_differe": type_differe,
        "duree_differe": duree_differe,
        "frais_courtage": frais_courtage,
        "frais_inclus": inclus_financement,
        "rendement_souhaite": rendement_souhaite,
        "delai_jouissance": delai_jouissance,
        "taux_revalorisation": taux_revalorisation,
        "frais_souscription": frais_souscription,
        "taux_imposition": taux_imposition,
        "investissement_etranger": investissement_etranger,
        "pourcentage_etranger": pourcentage_etranger,
    }

def tab_amortissement(params):
    # Calcul du montant du prêt
    montant_pret = params["montant_investissement"] - params["apport"] + params["frais_courtage"] if params["frais_inclus"] else params["montant_investissement"] - params["apport"]
    capital_restant = montant_pret

    # Calcul de la mensualité initiale
    if params["type_differe"] == 'Sans différé' or params["duree_differe"] == 0:
        mensualite = -npf.pmt(params["taux_interet"] / 12, params["duree_pret"], montant_pret)
    else:
        mensualite = None  # Calcul de la mensualité post différé

    amortissement = []

    for mois in range(1, params["duree_pret"] + 1):
        interet = capital_restant * (params["taux_interet"] / 12)
        assurance = montant_pret * (params["taux_assurance"] / 12)
        
        if mois <= params["duree_differe"]:
            if params["type_differe"] == 'Différé total':
                remboursement_capital = 0
                mensualite_hors_assurance = 0
                mensualite_avec_assurance = assurance
                capital_restant += interet
            elif params["type_differe"] == 'Différé partiel':
                remboursement_capital = 0
                mensualite_hors_assurance = interet
                mensualite_avec_assurance = interet + assurance
            else:
                remboursement_capital = mensualite - interet
                mensualite_hors_assurance = mensualite
                mensualite_avec_assurance = mensualite + assurance
        else:
            if mois == params["duree_differe"] + 1:
                mensualite = -npf.pmt(params["taux_interet"] / 12, params["duree_pret"] - params["duree_differe"], capital_restant)
            
            remboursement_capital = mensualite - interet
            mensualite_hors_assurance = mensualite
            mensualite_avec_assurance = mensualite + assurance

        capital_restant -= remboursement_capital
        
        amortissement.append([mois, mensualite_hors_assurance, mensualite_avec_assurance, interet, assurance, remboursement_capital, capital_restant])

    df_amortissement = pd.DataFrame(amortissement, columns=["Mois", "Mensualité sans assurance", "Mensualité avec assurance", "Intérêts", "Assurance", "Remboursement Capital", "Capital Restant"])
    capital_restant_annuel = df_amortissement.groupby(df_amortissement.index // 12)["Capital Restant"].last()
    
    return df_amortissement, capital_restant_annuel

def tab_investissement(params, df_amortissement):

    resultats = []
    deductible_cumule = 0

    taux_imposition_europe = 20

    for annee in range(1, 51):
        if annee == 1:
            loyer_brut = params["montant_investissement"] * params["rendement_souhaite"] * (12 - params["delai_jouissance"]) / 12
        else:
            loyer_brut = params["montant_investissement"] * params["rendement_souhaite"] * (1 + params["taux_revalorisation"])**(annee - 1)

        loyer_francais = loyer_brut * (1 - params["pourcentage_etranger"] / 100)
        loyer_etranger = loyer_brut * (params["pourcentage_etranger"] / 100)

        if annee <= params["duree_pret"] // 12:
            effort_annuel = df_amortissement["Mensualité avec assurance"][(annee-1)*12:annee*12].sum() - loyer_brut
            if annee == 1 and not params["frais_inclus"]:
                effort_annuel += params["frais_courtage"]
         
            if annee == 1:
                if params["type_differe"] == 'Différé total':
                    montant_deductible =df_amortissement["Assurance"][:12].sum() + \
                                        df_amortissement["Intérêts"][params["duree_differe"]:12].sum() + \
                                        params["frais_courtage"]
                else:  
                    montant_deductible =df_amortissement["Assurance"][:12].sum() + \
                                        df_amortissement["Intérêts"][:12].sum() + \
                                        params["frais_courtage"]
            else:
                montant_deductible =df_amortissement["Intérêts"][(annee-1)*12:annee*12].sum() + \
                                    df_amortissement["Assurance"][(annee-1)*12:annee*12].sum() 
        else:
            effort_annuel = -loyer_brut
            montant_deductible = 0

        imposable_francais = loyer_francais - (montant_deductible * (1 - params["pourcentage_etranger"] / 100))
        imposable_etranger = loyer_etranger

        if imposable_francais < 0:
            deductible_cumule += abs(imposable_francais)
            impot_francais = 0
        else:
            if deductible_cumule > 0:
                if deductible_cumule < imposable_francais:
                    net_imposable = imposable_francais - deductible_cumule
                    impot_francais = net_imposable * (params["taux_imposition"] + 0.172)
                    deductible_cumule = 0
                else:
                    deductible_cumule -= imposable_francais
                    impot_francais = 0
            else:
                impot_francais = imposable_francais * (params["taux_imposition"] + 0.172)

        impot_etranger = imposable_etranger * max(params["taux_imposition"], taux_imposition_europe / 100)
        impot_total = impot_francais + impot_etranger

        effort_net = effort_annuel + impot_total
        valeur_revente = params["montant_investissement"] * (1 - params["frais_souscription"]) * (1 + params["taux_revalorisation"])**annee

        resultats.append({
            "Année": annee,
            "Loyer Brut": loyer_brut,
            "Loyer Français": loyer_francais,
            "Loyer Étranger": loyer_etranger,
            "Effort Annuel": effort_annuel,
            "Montant Déductible": montant_deductible,
            "Imposable Français": imposable_francais,
            "Imposable Étranger": imposable_etranger,
            "Impôt Français": impot_francais,
            "Impôt Étranger": impot_etranger,
            "Impôt Total": impot_total,
            "Report Déductible": deductible_cumule,
            "Effort Annuel Net": effort_net,
            "Effort Mensuel Net": effort_net / 12,
            "Valeur de Revente": valeur_revente,
            "Loyer Net Français": loyer_francais - impot_francais,
            "Loyer Net Étranger": loyer_etranger - impot_etranger
        })

    return pd.DataFrame(resultats)

def color_alternating_rows(s):
    return ['background-color: #EEEFF1' if i % 2 == 0 else 'background-color: #FBFBFB' for i in range(len(s))]

def create_line_segments(x, y, color):
    segments = []
    for i in range(len(x) - 1):
        segments.append(go.Scatter(
            x=x[i:i+2],
            y=y[i:i+2],
            mode='lines',
            line=dict(color=color[i], width=2),
            showlegend=False,
            hoverinfo='skip'
        ))
    return segments

def graphique_loyers_francais_vs_etrangers(df_investissement): 
    couleur_francais = '#16425B' 
    couleur_francais_aire = 'rgba(141, 179, 197, 0.5)' 
    couleur_etranger = '#CBA325' 
    couleur_etranger_aire = 'rgba(241, 216, 122, 0.5)'
    couleur_total = '#ACADAF'
    couleur_total_aire = 'rgba(208, 209, 211, 0.2)'

    # Calculer la différence et sa valeur absolue
    df_investissement['Différence'] = df_investissement['Loyer Net Français'] - df_investissement['Loyer Net Étranger']
    df_investissement['Différence_Abs'] = np.abs(df_investissement['Différence'])

    # Calculer la somme des deux loyers
    df_investissement['Revenus Totaux'] = df_investissement['Loyer Net Français'] + df_investissement['Loyer Net Étranger']

    fig = go.Figure()

    # Loyer Français
    fig.add_trace(go.Scatter(
        x=df_investissement['Année'],
        y=df_investissement['Loyer Net Français'],
        name='Loyer Français',
        mode='lines',
        line=dict(color=couleur_francais, width=4),  # Augmentation de l'épaisseur de la ligne
        fill='tozeroy',
        fillcolor=couleur_francais_aire,
        hovertemplate='<span style="color:' + couleur_francais + ';">●</span> Loyer Français <br>Montant: <b>%{y:.0f} €</b><extra></extra>'
    ))

    # Loyer Étranger
    fig.add_trace(go.Scatter(
        x=df_investissement['Année'],
        y=df_investissement['Loyer Net Étranger'],
        name='Loyer Étranger',
        mode='lines',
        line=dict(color=couleur_etranger, width=4),  # Augmentation de l'épaisseur de la ligne
        fill='tozeroy',
        fillcolor=couleur_etranger_aire,
        hovertemplate='<span style="color:' + couleur_etranger + ';">●</span> Loyer Étranger <br> Montant: <b>%{y:.0f} €</b><extra></extra>'
    ))

    # Revenus Totaux
    fig.add_trace(go.Scatter(
        x=df_investissement['Année'],
        y=df_investissement['Revenus Totaux'],
        name='Revenus Totaux',
        mode='lines',
        line=dict(color=couleur_total, width=2, dash='dash'),
        fill='tozeroy',
        fillcolor=couleur_total_aire,
        hovertemplate='<span style="color:' + couleur_total + ';">●</span> Revenus Totaux <br>Montant: <b>%{y:.0f} €</b><extra></extra>'
    ))

    # Supprimer le titre du graphique Plotly
    fig.update_layout(
        title=None,
        xaxis=dict(
            title="<b>Années</b>",
            tickmode='linear',
            dtick=5,
            ticksuffix=" ",
            showgrid=False,
            zeroline=False,
            showline=True,
            linewidth=3,
            linecolor='#CBA325',
        ),
        yaxis=dict(
            title="<b>Montant des Loyers (€)</b>",
            tickmode='linear',
            dtick=1000,
            ticksuffix=" €",
            tickformat=",",
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(200,200,200,0.2)',
            zeroline=False,
            showline=True,
            linewidth=3,
            linecolor='#CBA325',
        ),
        font=dict(family="Inter", size=14),
        height=500,
        width=1000,
        margin=dict(t=60, b=60, l=60, r=60),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=12),
        ),
        hovermode="x unified",
    )

    # Ajouter le titre en tant qu'élément séparé
    st.markdown("<h2 style='text-align: center; color: #16425B;'>Vos revenus nets (Français vs Étranger)</h2>", unsafe_allow_html=True)

    # Afficher le graphique
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})



def plot_amortissement(df_amortissement, df_investissement, duree_pret, apport):
    # Définition des couleurs
    couleur_capital_restant = '#A33432'
    couleur_valeur_revente = '#10505B'
    couleur_effort_annuel = '#D56844'
    couleur_point_sortie = '#CBA325'

    df_amortissement_annuel = df_amortissement.groupby(df_amortissement.index // 12).last()
    df_amortissement_annuel.index = np.arange(1, len(df_amortissement_annuel) + 1)

    df_investissement['Effort Net Cumulé'] = df_investissement['Effort Annuel Net'].cumsum()

    # Calcul du point de sortie sans perte (intégration de l'apport)
    df_investissement['Cout Total'] = df_investissement['Effort Net Cumulé'] + df_amortissement_annuel['Capital Restant'].reindex(df_investissement['Année']).fillna(0)
    df_investissement['Cout Total'].iloc[0] += apport
    df_investissement['Difference'] = df_investissement['Valeur de Revente'] - df_investissement['Cout Total']
    point_sortie = df_investissement[df_investissement['Difference'] >= 0].head(1)
    annee_sortie = point_sortie['Année'].values[0] if not point_sortie.empty else None

    # Créer la figure pour la période "avant"
    fig = go.Figure()

    duree_max = duree_pret // 12
    x_range = np.arange(1, duree_max + 1)

    fig.add_trace(go.Scatter(
        x=x_range, 
        y=df_amortissement_annuel['Capital Restant'][:duree_max], 
        mode='lines+markers', 
        name='Capital Restant', 
        line=dict(color=couleur_capital_restant, width=3), 
        marker=dict(size=6, color='white', line=dict(color=couleur_capital_restant, width=2)),
        hovertemplate='<span style="color:' + couleur_capital_restant + ';">●</span> Capital Restant <br>Montant: <b>%{y:.0f} €</b><extra></extra>',
        fill='tozeroy',
        fillcolor="#E8B0AA"
    ))
    fig.add_trace(go.Scatter(
        x=x_range, 
        y=df_investissement['Valeur de Revente'][:duree_max], 
        mode='lines+markers', 
        name='Valeur de Revente', 
        line=dict(dash='dash', color=couleur_valeur_revente, width=3), 
        marker=dict(size=6, color='white', line=dict(color=couleur_valeur_revente, width=2)),
        hovertemplate='<span style="color:' + couleur_valeur_revente + ';">●</span> Valeur de Revente <br>Montant: <b>%{y:.0f} €</b><extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=x_range, 
        y=df_investissement['Effort Net Cumulé'][:duree_max], 
        mode='lines+markers', 
        name='Effort Net Cumulé', 
        line=dict(color=couleur_effort_annuel, width=3), 
        marker=dict(size=6, color='white', line=dict(color=couleur_effort_annuel, width=2)),
        hovertemplate='<span style="color:' + couleur_effort_annuel + ';">●</span> Effort Net Cumulé <br>Montant: <b>%{y:.0f} €</b><extra></extra>'
    ))

    # Ajustement des limites des axes
    fig.update_layout(
        xaxis=dict(range=[1, duree_max]),
        yaxis=dict(range=[0, max(df_amortissement_annuel['Capital Restant'].max(), df_investissement['Valeur de Revente'].max()) + 20000])
    )

    # Ajouter la ligne et le point de sortie s'il y a un point de sortie
    if annee_sortie:
        fig.add_shape(
            type="line",
            x0=annee_sortie,
            x1=annee_sortie,
            y0=0,
            y1=1,
            xref='x',
            yref='paper',
            line=dict(color=couleur_point_sortie, width=3, dash="solid")
        )
        
        fig.add_trace(go.Scatter(
            x=[annee_sortie],
            y=[df_investissement.loc[df_investissement['Année'] == annee_sortie, 'Valeur de Revente'].values[0]],
            mode='markers',
            marker=dict(symbol='star', size=16, color=couleur_point_sortie, line=dict(width=2, color='#16425B')),
            name='Point de sortie',
            hoverinfo='skip'
        ))

        fig.add_annotation(
            x=annee_sortie,
            y=df_investissement.loc[df_investissement['Année'] == annee_sortie, 'Valeur de Revente'].values[0],
            text=f"Sortie neutre<br>(Année {annee_sortie})",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor=couleur_point_sortie,
            ax=0,
            ay=-40,
            bgcolor='#16425B',
            font=dict(color="#FBFBFB", size=12),
            bordercolor=couleur_point_sortie,
            borderwidth=2,
            borderpad=4,
            opacity=0.8
        )

        # Mettre à jour la mise en page
        fig.update_layout(
        title=dict(
            text='<b>La vie de votre investissement</b>',
            font=dict(family="Inter", size=24, color="#16425B"),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title="<b>Années</b>",
            tickmode='linear',
            dtick=5,
            ticksuffix=" ",
            showgrid=False,
            zeroline=False,
            showline=True,
            linewidth=3,
            linecolor="#CBA325",
        ),
        yaxis=dict(
            title="<b>Montant (€)</b>",
            tickmode='linear',
            dtick=20000,
            ticksuffix=" €",
            tickformat=",",
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(200,200,200,0.2)',
            zeroline=False,
            showline=True,
            linewidth=3,
            linecolor="#CBA325",
        ),
        hovermode="x unified",
        font=dict(family="Inter", size=14),
        height=600,
        width=1000,
        margin=dict(t=60, b=60, l=60, r=60),  # Gardez les marges symétriques pour centrer le graphique
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,  # Déplacer la légende un peu plus bas si nécessaire
            xanchor="center",
            x=0.5,
            bgcolor='rgba(0,0,0,0)',
            traceorder="normal",
            font=dict(size=10),
            itemsizing="constant",
            itemwidth=40,
        )
    )


    # Afficher le graphique
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})



def main():    
    params = input_simulateur()
    df_amortissement, capital_restant_annuel = tab_amortissement(params)
    df_investissement = tab_investissement(params, df_amortissement)

    duree_pret = int(params["duree_pret"])

    onglet1, onglet2, onglet3 = st.tabs(["Vue d'ensemble", "Tableau d'amortissement", "Tableau d'investissement"])
    
    with onglet1:            
        col1, col2, col3, col4 = st.columns(4)

        # Calcul pour St.Metric
        effort_net_total = sum(df_investissement["Effort Annuel Net"][:params["duree_pret"] // 12])+ (params["apport"])
        loyer_apres_pret = params["montant_investissement"] * params["rendement_souhaite"] * (1 + params["taux_revalorisation"])**(params["duree_pret"] // 12)
        rendement_brut = (loyer_apres_pret / effort_net_total) * 100
        revenu_mensuel = loyer_apres_pret / 12
        effort_mensuel_moyen = sum(df_investissement["Effort Mensuel Net"][:params["duree_pret"] // 12]) / (params["duree_pret"] // 12)
        impot_apres_pret = loyer_apres_pret * (params["taux_imposition"] + 0.172)
        loyer_net_apres_pret = loyer_apres_pret - impot_apres_pret
        rendement_net = (loyer_net_apres_pret / effort_net_total) * 100

        
        with col1:
            st.metric("Loyer Mensuel", f"{revenu_mensuel:.0f}€")

        with col2:
             st.metric("Effort Mensuel", f"{effort_mensuel_moyen:.0f}€", help='Apport non inclus dans le calcul')
                
        with col3:
            st.metric("Rendement Brut", f"{rendement_brut:.2f}%")

        with col4:
            st.metric("Rendement Net", f"{rendement_net:.2f}%")

        st.markdown(
            """
            <style>
            .custom-box {
                background-color: rgba(141, 179, 197, 0.3); /* Couleur de fond rose clair */
                color: #16425B; /* Couleur du texte */
                padding: 15px; /* Espacement interne */
                border-radius: 15px; /* Coins arrondis */
                margin-bottom: 20px; /* Espace en dessous */
                box-shadow: 0px 4px 8px rgba(251, 251, 251, 0.8);
            }
            </style>
            <div class="custom-box">
                L'investissement en SCPI a pour fonction première la <strong>distribution de revenus complémentaires</strong> à une échéance donnée. <strong>L'objectif n'est pas la revente</strong> à court, moyen ou moyen-long terme.
            </div>
            """,
            unsafe_allow_html=True
        )

        
        plot_amortissement(df_amortissement, df_investissement, duree_pret, params['apport'])

        graphique_loyers_francais_vs_etrangers(df_investissement)
        

            
    with onglet2:
        df_amortissement.set_index('Mois', inplace=True)

        styled_df_amortissement = df_amortissement.style.format("{:,.0f}") \
    .set_properties(**{
        'color': '#202021',
    }) \
    .apply(color_alternating_rows) \
    .set_table_styles([
        {'selector': 'th',
         'props': [('font-weight', 'bold'),
                   ('background-color', '#284264'),
                   ('color', 'white')]},
        # Assurer que la table occupe toute la largeur disponible
        {'selector': 'table',
         'props': [('width', '100%'),
                   ('table-layout', 'fixed')]},
    ])
        st.dataframe(styled_df_amortissement, use_container_width=True)  

        # Bouton de téléchargement
        csv = df_amortissement.to_csv(index=True)  # index=True pour inclure la colonne 'Année'
        st.download_button(label="Télécharger les résultats (CSV)", 
                        data=csv, 
                        file_name="tableau_amortissement.csv", 
                        mime="text/csv")
             

    with onglet3:
        df_investissement.set_index('Année', inplace=True)

        df_to_display_investissement = df_investissement[['Loyer Brut', 'Impôt Total', 'Effort Annuel Net', 'Effort Mensuel Net', 'Valeur de Revente']]
        
        styled_df_investissement = df_to_display_investissement.style.format("{:,.0f}") \
        .set_properties(**{
            'color': '#202021',
        }) \
        .apply(color_alternating_rows) \
        .set_table_styles([
            {'selector': 'th',
            'props': [('font-weight', 'bold'),
                    ('background-color', '#284264'),
                    ('color', 'white')]},
            # Assurer que la table occupe toute la largeur disponible
            {'selector': 'table',
            'props': [('width', '100%'),
                    ('table-layout', 'fixed')]},
        ]) \

        st.dataframe(styled_df_investissement, use_container_width=True)

        # Bouton de téléchargement
        csv = df_investissement.to_csv(index=True)  # index=True pour inclure la colonne 'Année'
        st.download_button(label="Télécharger les résultats (CSV)", 
                        data=csv, 
                        file_name="resultats_simulation_scpi.csv", 
                        mime="text/csv") # Comment changer le fichier de téléchargement ?
    
    if rendement_net > 10:
        st.balloons()

if __name__ == "__main__":
    main()
