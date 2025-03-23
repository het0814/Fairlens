import json
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import matplotlib
import os
matplotlib.use('Agg')  # Use non-GUI backend
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"



def parse_resume_score(score_json_str):
    try:
        return json.loads(score_json_str)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

def create_radar_chart(scores, title):
    categories = [
        'technical_compatibility',
        'industry_experience',
        'workplace_adaptability',
        'educational_strength',
        'performance_impact'
    ]
    values = [scores.get(cat, 0) for cat in categories]

    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    plt.xticks(angles[:-1], categories, color='grey', size=10)
    ax.plot(angles, values, linewidth=2, linestyle='solid', color='blue')
    ax.fill(angles, values, alpha=0.25, color='skyblue')
    plt.title(title, size=15, color='darkblue')
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 100)

    for angle, value in zip(angles[:-1], values[:-1]):
        ax.text(angle, value, f'{value:.0f}', ha='center', va='center')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=300)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    return image_base64

def create_individual_donut_charts(scores):
    individual_charts = {}
    color_palettes = [plt.cm.Pastel1, plt.cm.Pastel2, plt.cm.Set3, plt.cm.Set2, plt.cm.Set1]

    donut_categories = [
        'career_stability_and_progression',
        'continuous_learning_and_upskilling',
        'diversity_of_experience',
        'project_experience',
        'extracurricular_and_volunteering'
    ]

    for idx, category in enumerate(donut_categories):
        fig, ax = plt.subplots(figsize=(8, 6))
        score = scores.get(category, 0)
        colors = color_palettes[idx](np.linspace(0, 1, 2))

        wedges, texts, autotexts = ax.pie(
            [score, 100 - score],
            labels=['Achieved', 'Remaining'],
            colors=colors,
            autopct='%1.1f%%',
            pctdistance=0.85,
            wedgeprops=dict(width=0.5, edgecolor='white')
        )

        plt.setp(autotexts, size=8, weight="bold", color="white")
        plt.setp(texts, size=10)
        plt.title(f"{category.replace('_', ' ').title()} Evaluation", size=12, color='darkblue')

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=300)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plt.close()
        individual_charts[category] = image_base64

    return individual_charts

def generate_resume_charts(score, donut_score):
    score_dict = parse_resume_score(score)
    donut_dict = parse_resume_score(donut_score)

    charts = {
        'scoring_radar_chart': None,
        'individual_donut_charts': None
    }

    if score_dict:
        charts['scoring_radar_chart'] = create_radar_chart(
            score_dict, 
            "Resume Scoring Radar Analysis"
        )

    if donut_dict:
        charts['individual_donut_charts'] = create_individual_donut_charts(donut_dict)

    return charts
