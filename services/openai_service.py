from openai import OpenAI
from flask import current_app

def get_openai_client():
    return OpenAI(api_key=current_app.config['OPENAI_API_KEY'])
def analyze_resume(resume_text, job_description):
    client = get_openai_client()
    prompt = f"""  
    **Job Description:**
    {job_description}

    **Resume:**
    {resume_text}
    """
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": "Evaluate a given resume against specific criteria to analyze its strengths and weaknesses.\n\nEnsure accurate assessment by reviewing the resume content in detail, comparing it against the defined criteria to identify key areas such as work experience, skills, achievements, and relevant qualifications.\n\n# Steps\n\n1. **Read the Resume:**\n   - Carefully review each section of the resume, including work experience, education, skills, achievements, and any other relevant sections.\n   \n2. **Compare with Criteria:**\n   - Measure each part of the resume against the provided criteria. Focus on finding matches in experience, skills, and accomplishments that align with the desired qualifications."
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": prompt}
            ]
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
            "name": "resume_analysis",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                "skills_match": {
                    "type": "object",
                    "properties": {
                    "technical_skills": {
                        "type": "array",
                        "description": "Provide the summary of technical skills. How well they allign with the job description.",
                        "items": {
                        "type": "string"
                        }
                    },
                    "soft_skills": {
                        "type": "array",
                        "description": "Provide the summary of soft skills. How well they allign with the job description.",
                        "items": {
                        "type": "string"
                        }
                    }
                    },
                    "required": [
                    "technical_skills",
                    "soft_skills"
                    ],
                    "additionalProperties": False
                },
                "experience_and_career_progression": {
                    "type": "object",
                    "properties": {
                    "total_years_experience": {
                        "type": "number",
                        "description": "Summary of Total years of experience in relevant fields and also will it be usefull for this job description."
                    },
                    "career_growth": {
                        "type": "boolean",
                        "description": "Indicates if the candidate has demonstrated career growth."
                    }
                    },
                    "required": [
                    "total_years_experience",
                    "career_growth"
                    ],
                    "additionalProperties": False
                },
                "cultural_fit_and_personality_traits": {
                    "type": "object",
                    "properties": {
                    "alignment_with_company_values": {
                        "type": "boolean",
                        "description": "Summary of whether the candidate's personality traits align with the company's culture."
                    },
                    "leadership_potential": {
                        "type": "boolean",
                        "description": "Indicates if there are indications of leadership potential in the candidate."
                    }
                    },
                    "required": [
                    "alignment_with_company_values",
                    "leadership_potential"
                    ],
                    "additionalProperties": False
                },
                "quantifiable_achievements_and_results": {
                    "type": "array",
                    "description": "Summary of quantifiable achievements that demonstrate candidate's impact.",
                    "items": {
                    "type": "string"
                    }
                },
                "education_and_certifications": {
                    "type": "object",
                    "properties": {
                    "highest_degree": {
                        "type": "string",
                        "description": "The highest educational qualification of the candidate."
                    },
                    "certifications": {
                        "type": "array",
                        "description": "Summary of relevant certifications obtained by the candidate that match with the job description.",
                        "items": {
                        "type": "string"
                        }
                    }
                    },
                    "required": [
                    "highest_degree",
                    "certifications"
                    ],
                    "additionalProperties": False
                }
                },
                "required": [
                "skills_match",
                "experience_and_career_progression",
                "cultural_fit_and_personality_traits",
                "quantifiable_achievements_and_results",
                "education_and_certifications"
                ],
                "additionalProperties": False
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

def score_resume(resume_text,job_description):
    client = get_openai_client()
    prompt = f"""  
    **Job Description:**
    {job_description}

    **Resume:**
    {resume_text}
    """
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": "Analyze the following resume analyisis and provide scores out of 100"           
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": prompt}
            ]
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
            "name": "resume_score",
            "strict": True,
            "schema": {
                "type": "object",
            "properties": {
                "skills_and_qualifications": {
                    "type": "number",
                    "description": "Score (out of 100) assessing technical skills, certifications, and educational background."
                },
                "experience_and_past_performance": {
                    "type": "number",
                    "description": "Score (out of 100) evaluating work history, industry experience, and achievements."
                },
                "cultural_fit_and_soft_skills": {
                    "type": "number",
                    "description": "Score (out of 100) analyzing communication, teamwork, problem-solving, and alignment with company values."
                },
                "adaptability_and_learning_ability": {
                    "type": "number",
                    "description": "Score (out of 100) measuring ability to handle change, learn new skills, and adapt to new environments or technologies."
                }
            },
            "required": [
                "skills_and_qualifications",
                "experience_and_past_performance",
                "cultural_fit_and_soft_skills",
                "adaptability_and_learning_ability"
            ],
            "additionalProperties": False
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

def donut_score_resume(resume_text,job_description):
    client = get_openai_client()
    prompt =f"""  
    **Job Description:**
    {job_description}

    **Resume:**
    {resume_text}
    """
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": "Analyze the following resume analyisis and provide scores out of 100"           
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": prompt}
            ]
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
            "name": "resume_score",
            "strict": True,
            "schema": {
                "type": "object",
            "properties": {
                "Technical_Skills_Proficiency": {
                    "type": "number",
                    "description": "Score (out of 100) assessing technical skills, certifications, and educational background."
                },
                "Experience_Level_Distribution": {
                    "type": "number",
                    "description": "Score (out of 100) evaluating work history, industry experience, and achievements."
                },
                "Work_Location_Flexibility": {
                    "type": "number",
                    "description": "Score (out of 100) analyzing communication, teamwork, problem-solving, and alignment with company values."
                },
                "Keywords_and_Phrases_Match": {
                    "type": "number",
                    "description": "Score (out of 100) measuring ability to handle change, learn new skills, and adapt to new environments or technologies."
                },
                "Location_Test": {
                    "type": "number",
                    "description": "Score (out of 100) measuring ability to handle change, learn new skills, and adapt to new environments or technologies."
                },
            },
            "required": [
                "Technical_Skills_Proficiency",
                "Experience_Level_Distribution",
                "Work_Location_Flexibility",
                "Keywords_and_Phrases_Match",
                "Location_Test"
            ],
            "additionalProperties": False
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
