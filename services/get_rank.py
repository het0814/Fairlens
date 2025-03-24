from openai_service import *
from openai import OpenAI
from flask import current_app
import json

def get_openai_client():
    return OpenAI(api_key=current_app.config['OPENAI_API_KEY'])

def rank_resumes(resume_scores):
    """
    Rank resumes based on their scores across different evaluation criteria.
    
    Args:
    resume_scores (list): A list of dictionaries containing resume scores 
                          from the score_resume function.
    
    Returns:
    dict: A ranked list of resumes with their overall score and ranking.
    """
    client = get_openai_client()
    
    prompt = f"""
    ### Task:
    Analyze and rank the provided resume scores based on a comprehensive evaluation.

    ### Ranking Methodology:
    1. Calculate an overall score by:
       - Weighting each scoring parameter
       - Considering the holistic performance across all dimensions
    
    2. Provide a detailed ranking with:
       - Overall score out of 100
       - Ranking position
       - Brief justification for the ranking
    
    ### Resume Scores:
    {json.dumps(resume_scores, indent=2)}
    """
    
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
                "role": "system",
                "content": "Analyze and rank the resume scores comprehensively."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "resume_ranking",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "ranked_resumes": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "resume_id": {
                                        "type": "string",
                                        "description": "Unique identifier for the resume"
                                    },
                                    "overall_score": {
                                        "type": "number",
                                        "description": "Calculated overall score out of 100"
                                    },
                                    "ranking": {
                                        "type": "number",
                                        "description": "Ranking position (1 being the highest)"
                                    },
                                    "ranking_justification": {
                                        "type": "string",
                                        "description": "Explanation for the ranking"
                                    }
                                },
                                "required": [
                                    "resume_id", 
                                    "overall_score", 
                                    "ranking", 
                                    "ranking_justification"
                                ]
                            }
                        }
                    },
                    "required": ["ranked_resumes"]
                }
            }
        },
        temperature=1,
        max_completion_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    
    return response.choices[0].message.content