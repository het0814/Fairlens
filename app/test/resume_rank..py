from openai import OpenAI
import json

OPENAI_API_KEY = "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"

def rank_resumes(resume_scores):
    client = OpenAI(api_key=OPENAI_API_KEY)
    total_resumes = len(resume_scores)  
    prompt = f"""
    ### Task:
    You are ranking a total of {total_resumes} resumes. 
    Analyze and rank all resumes based on their scores.
    
    1. For each resume, provide:
       - Ranking position (1 to {total_resumes})
       - Brief justification for the ranking
    
    ### Resumes:
    {resume_scores}
    """
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
                "role": "system",
                "content": "Analyze and rank all resumes comprehensively."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={  # Corrected the schema for additionalProperties and overall object
            "type": "json_schema",
            "json_schema": {
                "name": "resume_ranking",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "rankings": {  # Define the rankings field as an array
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "file_name": {
                                        "type": "string",
                                        "description": "Name of the resume file."
                                    },
                                    "rank": {
                                        "type": "number",
                                        "description": "Rank of the resume out of the total resumes."
                                    },
                                    "justification": {
                                        "type": "string",
                                        "description": "Reasoning behind the ranking."
                                    }
                                },
                                "required": ["file_name", "rank", "justification"],
                                "additionalProperties": False  # Corrected this placement
                            }
                        }
                    },
                    "required": ["rankings"],
                    "additionalProperties": False  # Correct placement of this
                }
            }
        },
        temperature=1,
        max_completion_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    
    # Parse and return the results
    return response.choices[0].message.content

# Demo scores
demo_scores = [
    {'file_name': 'IT_Resume.pdf', 'score': '{"skills_and_qualifications":90,"experience_and_past_performance":85,"cultural_fit_and_soft_skills":80,"adaptability_and_learning_ability":95}', 'donut_analysis': '{"Technical_Skills_Proficiency":85,"Experience_Level_Distribution":80,"Work_Location_Flexibility":75,"Keywords_and_Phrases_Match":90,"Location_Test":70}'}, 
    {'file_name': 'Resume_F.pdf', 'score': '{"skills_and_qualifications":60,"experience_and_past_performance":70,"cultural_fit_and_soft_skills":75,"adaptability_and_learning_ability":80}', 'donut_analysis': '{"Technical_Skills_Proficiency":65,"Experience_Level_Distribution":75,"Work_Location_Flexibility":70,"Keywords_and_Phrases_Match":60,"Location_Test":50}'}
]

# Get ranking results
results = rank_resumes(demo_scores)
print(results)
