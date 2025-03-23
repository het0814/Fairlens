import json
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

def parse_resume_score(score_json_str):
    try:
        # Parse the JSON string into a Python dictionary
        score_dict = json.loads(score_json_str)
        return score_dict
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

def create_radar_chart(scores, title):
    # Extract categories and values
    categories = list(scores.keys())
    values = list(scores.values())

    # Number of variables
    N = len(categories)

    # What will be the angle of each axis in the plot?
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    values += values[:1]
    angles += angles[:1]

    # Plot
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
    
    # Customize the chart
    plt.xticks(angles[:-1], categories, color='grey', size=10)
    ax.plot(angles, values, linewidth=2, linestyle='solid', color='blue')
    ax.fill(angles, values, alpha=0.25, color='skyblue')
    
    plt.title(title, size=15, color='darkblue')

    # Ensure the radar chart is a circle and not an ellipse
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # Set the limits of the plot to [0, 100]
    ax.set_ylim(0, 100)

    # Add value labels
    for angle, value in zip(angles[:-1], values[:-1]):
        ax.text(angle, value, f'{value:.0f}', 
                horizontalalignment='center', 
                verticalalignment='center')

    # Convert plot to base64 for embedding in HTML
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=300)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    return image_base64

def create_individual_donut_charts(scores):
    # Initialize dictionary to store individual donut charts
    individual_charts = {}

    # Color palettes
    color_palettes = [
        plt.cm.Pastel1,
        plt.cm.Pastel2,
        plt.cm.Set3,
        plt.cm.Set2,
        plt.cm.Set1
    ]

    # Create a donut chart for each skill category
    skill_categories = [
        'Technical_Skills_Proficiency',
        'Experience_Level_Distribution',
        'Work_Location_Flexibility',
        'Keywords_and_Phrases_Match',
        'Location_Test'
    ]

    for idx, category in enumerate(skill_categories):
        # Create donut chart for the specific category
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Get the score for this category
        score = scores.get(category, 0)
        
        # Create color palette
        colors = color_palettes[idx](np.linspace(0, 1, 2))
        
        # Create donut chart
        wedges, texts, autotexts = ax.pie(
            [score, 100 - score],  # Score vs Remaining
            labels=['Achieved', 'Remaining'],
            colors=colors,
            autopct='%1.1f%%',
            pctdistance=0.85,
            wedgeprops=dict(width=0.5, edgecolor='white')
        )

        # Customize appearance
        plt.setp(autotexts, size=8, weight="bold", color="white")
        plt.setp(texts, size=10)
        
        plt.title(f"{category} Evaluation", size=12, color='darkblue')

        # Convert plot to base64 for embedding in HTML
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=300)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plt.close()

        # Store the chart
        individual_charts[category] = image_base64

    return individual_charts

def generate_resume_charts(score, donut_score):
    # Parse the scores
    score_dict = parse_resume_score(score)
    donut_dict = parse_resume_score(donut_score)

    # Initialize chart storage
    charts = {
        'scoring_radar_chart': None,
        'individual_donut_charts': None
    }

    # Generate charts if parsing is successful
    if score_dict:
        charts['scoring_radar_chart'] = create_radar_chart(
            score_dict, 
            "Resume Scoring Radar Analysis"
        )

    if donut_dict:
        charts['individual_donut_charts'] = create_individual_donut_charts(donut_dict)

    return charts