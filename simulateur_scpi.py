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

# MAIN APP
st.markdown("""
    <style>
    [data-testid="stSidebar"] > div:first-child {
        background: radial-gradient(circle, #8DB3C5, #FBFBFB);
        border-right: 2px solid #CBA325;
        box-shadow: 
            0 2px 4px rgba(22, 66, 91, 0.1),
            0 4px 8px rgba(22, 66, 91, 0.1),
            0 8px 16px rgba(22, 66, 91, 0.1),
            0 16px 32px rgba(22, 66, 91, 0.1);
    }
            
    /* StSlider */

    div[data-testid="stSlider"] label[data-testid="stWidgetLabel"] div[data-testid="stMarkdownContainer"] p { /* Label StSlider */
        display: flex;
        justify-content: center;
        text-align: left;
        width: 100%;
        font-size: 13px !important;
        font-weight: 400 !important;
        color:#202021;
        margin-bottom: 0px;
    }

    div[data-testid="stSlider"] {
        background-color: #FBFBFB;
        border: 2px solid #CBA325;
        box-shadow: 0px 4px 8px rgba(251, 251, 251, 0.8);
        border-radius: 10px;
        padding: 15px;
        margin-top: 10px;
        margin-bottom: 10px;
    }
                        
    /* Style for the slider thumb */
    div[data-testid="stSlider"] div[data-baseweb="slider"] div[role="slider"] {
        background-color: #8DB3C5;
        border: 2px solid #16425B;
    }



    /* StNumberInput */
    div[data-testid="stNumberInput"] label[data-testid="stWidgetLabel"] div[data-testid="stMarkdownContainer"] p { /* Label stNumberInput */
        display: flex;
        justify-content: center;
        text-align: left;
        width: 100%;
        font-size: 13px !important;
        font-weight: 400 !important;
        color: #202021;
        margin-bottom: 0px;
    }

    div[data-testid="stNumberInput"] {
        background-color: #FBFBFB;
        border: 2px solid #CBA325;
        border-radius: 10px;
        padding: 15px;
        margin-top: 10px;
        margin-bottom: 10px;
    }
                
    input[type="number"] {
        color: #202021 ;
        border: none ;
        border-radius: none !important;
        padding: 5px 10px !important;
        font-size: 16px !important;
    }
                
    button[data-testid="stNumberInput-StepDown"],
    button[data-testid="stNumberInput-StepUp"] {
        background-color: none;
        color: #16425B;
        border: none !important;
        border-radius: 3px !important;
        padding: 20px 10px !important;
        width: 10px !important;    
        height: 10px !important;   
    }
            

    [role="slider"] {
    background: linear-gradient(to right, #16425b 0%, #8DB3C5 83.3333%, rgba(141, 179, 197, 0.25) 83.3333%, rgba(141, 179, 197, 0.25) 100%);
    height: 12px;
    }

    [data-baseweb="slider"] > div:first-of-type > div:first-child {
    background-color: #8DB3C5 !important; /* après le curseur */
    height: 6px; /* Ajuste la hauteur si nécessaire */
    }       

    
       
    


    /* StRadioGroup */
    div[role="radiogroup"] {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 1rem;
    }  
    div[role="radiogroup"] label {
        background-color: transparent;
        padding: 10px 15px;
        margin: 0 5px;
        border-radius: 15px;
        transition: border-color 0.3s, color 0.3s;
        cursor: pointer;
        display: flex;
        align-items: center;
        border: 2px solid #CBA325;
        min-width: 100px;
    }
        
    div[role="radiogroup"] label:hover {
        border-color: #16425b;
    }  
    div[role="radiogroup"] label div {
        display: flex;
        align-items: center;
    }
    div[role="radiogroup"] label div p {
        font-size: 16px;
        font-weight: 600;
        margin: 0 0 0 10px;
    }



    /* StCheckbox */
    div[data-testid="stCheckbox"] {
        background-color: #FBFBFB;
        border: 2px solid #CBA325;
        border-radius: 10px;
        padding: 15px;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    div[data-testid="stCheckbox"] div[data-testid="stMarkdownContainer"] p {
        font-size: 13px !important;
        font-weight: 400
    }


    /* StSelectbox */
    div[data-testid="stSelectbox"] {
        background-color: #FBFBFB;
        border: 2px solid #CBA325;
        border-radius: 10px;
        padding: 15px;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    div[data-testid="stSelectbox"] label[data-testid="stWidgetLabel"] div[data-testid="stMarkdownContainer"] p {
        display: flex;
        justify-content: left;
        text-align: left;
        width: 100%;
        font-size: 13px !important; #âœ…
        font-weight: 400 !important;
        color: #202021;
        margin-bottom: 5px;
    }
            

    /* StMetric */
    div[data-testid="stMetric"] label[data-testid="stMetricLabel"] {
        display: flex;
        justify-content: center;
        text-align: center;
        width: 100%;
        font-size: 14px !important;
        font-weight: 400 !important;
        color: #202021;
    }    
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        text-align: center;
        font-size: 40px !important;
        font-weight: 700 !important;
        color: #16425B;
    }
    div[data-testid="stMetric"] {
        background-color: #FBFBFB;
        border: 3px solid #CBA325;
        box-shadow: 0px 4px 8px rgba(251, 251, 251, 0.8);
        border-radius: 10px;
        padding: 10px;
    }

    </style>
    """, unsafe_allow_html=True)



# TITLE
st.markdown("""
<style>
    .title-container {
        background: #FBFBFB;
        border-radius: 10px;
        border: 3px solid #16425B;
        padding: 10px 10px;
        margin-bottom: 50px;
        margin-top: -50px;
        text-align: center;
        box-shadow: 
            0 2px 4px rgba(22, 66, 91, 0.1),
            0 4px 8px rgba(22, 66, 91, 0.1),
            0 8px 16px rgba(22, 66, 91, 0.1),
            0 16px 32px rgba(22, 66, 91, 0.1);
    }
            
    .main-title {
        color: #CBA325;
        font-size: 40px;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
            
    .subtitle {
        color: #16425b;
        font-size: 20px;
    }
            
    .update-info {
        color:#202021;
        font-size: 12px;
        font-weight: 500;
        position: absolute;
        bottom: 5px;
        left: 10px;
    }
            
    .author-info {
        color:#202021;
        font-size: 12px;
        font-weight: 500;
        position: absolute;
        bottom: 5px;
        right: 10px;
    }
            
    /* Onglets */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        margin-bottom: 5px;
        border-radius: 10px;
        font-size: 30px;
    }
            
    .stTabs [data-baseweb="tab-list"] p {
        font-size: 14px;
        font-weight: 500;
    }
            
    .stTabs [data-baseweb="tab"] {
        height: auto;
        white-space: normal;
        padding: 10px 10px;
        color: #16425B;
        border: 3px solid #ACADAF;
        border-radius: 10px;
        background-color: #EEEFF1;
    }
            
    .stTabs [aria-selected="true"] {
        color: #16425B;
        border-bottom: 2px solid #202021;
    }
            
    /* StSlider */
    div[data-testid="stSlider"] label[data-testid="stWidgetLabel"] div[data-testid="stMarkdownContainer"] p { /* Label StSlider */
        display: flex;
        justify-content: center;
        text-align: left;
        width: 100%;
        font-size: 13px !important;
        font-weight: 400 !important;
        color:#202021;
        margin-bottom: 0px;
    }

    div[data-testid="stSlider"] {
        background-color: #FBFBFB;
        border: 2px solid #CBA325;
        box-shadow: 0px 4px 8px rgba(251, 251, 251, 0.8);
        border-radius: 10px;
        padding: 15px;
        margin-top: 10px;
        margin-bottom: 10px;
    }
                        
    /* Style for the slider thumb */
    div[data-testid="stSlider"] div[data-baseweb="slider"] div[role="slider"] {
        background-color: #8DB3C5;
        border: 2px solid #16425B;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="title-container">
    <h1 class="main-title">Simulateur SCPI</h1>
    <p class="subtitle">Investissez dans de l'immobilier professionnel à partir de 50 000€</p>
    <div class="update-info">Dernière mise à jour : {date.today().strftime('%d/%m/%Y')}</div>
    <div class="author-info">Par Antoine Berjoan</div>
</div>
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
            frais_courtage = st.number_input("💵 Frais courtage / dossier (€)", 0, 10000, 2250, 250)
            inclus_financement = st.checkbox("Inclus dans le financement ?", help='Les frais de dossiers / courtage sont-ils inclus dans votre financement ?')
        
        with st.container():
            rendement_souhaite = st.slider("📈 Rendement locatif (%)", 1.0, 10.0, 5.0, 0.1) / 100
            delai_jouissance = st.slider("🕒 Délai de jouissance (mois)", 0, 12, 6)
            taux_revalorisation = st.slider("📊 Taux de revalorisation (%)", 0.0, 5.0, 1.0, 0.1) / 100
            frais_souscription = st.slider("💸 Frais de souscription (%)", 0.0, 20.0, 12.0, 0.5) / 100
            taux_imposition = st.selectbox("🧮 Tranche d'imposition (TMI)", [0, 11, 30, 41, 45]) / 100
        
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
    couleur_francais_aire = '#8DB3C5' 
    couleur_etranger = '#CBA325' 
    couleur_etranger_aire = '#F1D87A'

    # Calculer la différence et sa valeur absolue
    df_investissement['Différence'] = df_investissement['Loyer Net Français'] - df_investissement['Loyer Net Étranger']
    df_investissement['Différence_Abs'] = np.abs(df_investissement['Différence'])

    fig = go.Figure()

    # Loyer Français
    fig.add_trace(go.Scatter(
        x=df_investissement['Année'],
        y=df_investissement['Loyer Net Français'],
        name='Loyer Français',
        mode='lines',
        line=dict(color=couleur_francais, width=3),
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
        line=dict(color=couleur_etranger, width=3),
        fill='tozeroy',
        fillcolor=couleur_etranger_aire,
        hovertemplate='<span style="color:' + couleur_etranger + ';">●</span> Loyer Étranger <br> Montant: <b>%{y:.0f} €</b><extra></extra>'
    ))

    # Différence (valeur absolue) avec changement de couleur
    for i in range(len(df_investissement) - 1):
        color = couleur_francais if df_investissement['Différence'].iloc[i] >= 0 else couleur_etranger
        fig.add_trace(go.Scatter(
            x=df_investissement['Année'].iloc[i:i+2],
            y=df_investissement['Différence_Abs'].iloc[i:i+2],
            mode='lines',
            line=dict(color=color, width=2),
            showlegend=False,
            hoverinfo='skip'
        ))

    # Ajouter une trace invisible pour la légende et le hover
    fig.add_trace(go.Scatter(
        x=df_investissement['Année'],
        y=df_investissement['Différence_Abs'],
        name='Différence',
        mode='lines',
        line=dict(color='rgba(0,0,0,0)'),
        hovertemplate='<span style="color:green;">●</span> Différence <br>' +
                    '%{text}: <b>%{y:.0f} €</b><extra></extra>',
        text=[f'Français > Étranger' if d >= 0 else 'Étranger > Français' for d in df_investissement['Différence']]
    ))

    # Calculer le maximum pour l'axe y et arrondir au multiple de 1000 supérieur
    y_max = max(df_investissement['Loyer Net Français'].max(),
                df_investissement['Loyer Net Étranger'].max(),
                df_investissement['Différence_Abs'].max())
    y_max_rounded = np.ceil(y_max / 1000) * 1000

    fig.update_layout(
        title=dict(
            text='<b>Évolution des revenus nets (Français vs Étranger)</b>',
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
            range=[0, y_max_rounded]
        ),
        font=dict(family="Inter", size=14),
        height=500,
        width=1000,
        margin=dict(t=100, b=60, l=60, r=60),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
        ),
        hovermode="x unified",
    )

    # Afficher le graphique avec des paramètres supplémentaires
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


    # Créer les boutons radio
    _, col, _ = st.columns([1,2,1])
    with col:
        option = st.radio(
            label="",
            options=('Avant', 'Après'),
            key="graph_option",
            horizontal=True
        )

    # Créer la figure en fonction de l'option sélectionnée
    fig = go.Figure()

    if option == 'Avant':
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
        
        fig.update_layout(
            xaxis=dict(range=[1, duree_max]),
            yaxis=dict(range=[0, max(df_amortissement_annuel['Capital Restant'].max(), df_investissement['Valeur de Revente'].max()) + 20000])
        )
    else:
        x_range = np.arange(duree_pret // 12 + 1, 51)
        
        fig.add_trace(go.Scatter(
            x=x_range, 
            y=df_amortissement_annuel['Capital Restant'][duree_pret // 12:50], 
            mode='lines+markers', 
            name='Capital Restant', 
            line=dict(color=couleur_capital_restant, width=3), 
            marker=dict(size=6, color='white', line=dict(color=couleur_capital_restant, width=2)),
            hovertemplate='<span style="color:' + couleur_capital_restant + ';">●</span> Capital Restant <br>Montant: <b>%{y:.0f} €</b><extra></extra>'
        ))
        fig.add_trace(go.Scatter(
            x=x_range, 
            y=df_investissement['Valeur de Revente'][duree_pret // 12:50], 
            mode='lines+markers', 
            name='Valeur de Revente', 
            line=dict(dash='dash', color=couleur_valeur_revente, width=3), 
            marker=dict(size=6, color='white', line=dict(color=couleur_valeur_revente, width=2)),
            hovertemplate='<span style="color:' + couleur_valeur_revente + ';">●</span> Valeur de Revente <br>Montant: <b>%{y:.0f} €</b><extra></extra>'
        ))
        fig.add_trace(go.Scatter(
            x=x_range, 
            y=df_investissement['Effort Net Cumulé'][duree_pret // 12:50], 
            mode='lines+markers', 
            name='Effort Net Cumulé', 
            line=dict(color=couleur_effort_annuel, width=3), 
            marker=dict(size=6, color='white', line=dict(color=couleur_effort_annuel, width=2)),
            hovertemplate='<span style="color:' + couleur_effort_annuel + ';">●</span> Effort Net Cumulé <br>Montant: <b>%{y:.0f} €</b><extra></extra>'
        ))
        
        fig.update_layout(
            xaxis=dict(range=[duree_pret // 12 + 1, 50]),
            yaxis=dict(range=[0, max(df_amortissement_annuel['Capital Restant'].max(), df_investissement['Valeur de Revente'].max()) + 20000])
        )

    if annee_sortie:
        # Ligne verticale pour le point de sortie
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
        
        # Point de sortie
        fig.add_trace(go.Scatter(
            x=[annee_sortie],
            y=[df_investissement.loc[df_investissement['Année'] == annee_sortie, 'Valeur de Revente'].values[0]],
            mode='markers',
            marker=dict(symbol='star', size=16, color=couleur_point_sortie, line=dict(width=2, color='#16425B')),
            name='Point de sortie',
            hoverinfo='skip'
        ))
        
        # Annotation pour le point de sortie (ajustée avec survol)
        fig.add_annotation(
            x=annee_sortie,
            y=df_investissement.loc[df_investissement['Année'] == annee_sortie, 'Valeur de Revente'].values[0],
            text=f"Point de sortie sans perte<br>(Année {annee_sortie})",
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
            opacity=0.8,
            hovertext=f"À l'année {annee_sortie}, la valeur de revente dépasse le coût total de l'investissement.<br>Vous pouvez revendre sans perte.",
            hoverlabel=dict(
                bgcolor="#FBFBFB",
                font_size=14,
                font_family="Inter"
            )
        )

    fig.update_layout(
        title=dict(
            text='<b>Évolution de votre investissement</b>',
            font=dict(family="Inter", size=24, color="#16425B"),
            x=0.5,
            xanchor='center',
            y=1,
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
        margin=dict(t=80, b=60, l=60, r=60),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor="#CBA325",
            borderwidth=3,
            traceorder="normal",
            font=dict(size=10),
            itemsizing="constant",
            itemwidth=40,
        ),
        shapes=[
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(
                    color="#16425B",
                    width=2,
                    dash="solid",
                ),
                fillcolor="rgba(0,0,0,0)"
            ),
        ]
    )

    # Afficher le graphique
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    return option


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


        graphique_loyers_francais_vs_etrangers(df_investissement)


        plot_amortissement(df_amortissement, df_investissement, duree_pret, params['apport'])
        

            
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
