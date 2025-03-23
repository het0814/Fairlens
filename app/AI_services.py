import fitz
import docx
from openai import OpenAI


OPENAI_API_KEY = "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"

# Function to extract text from PDF and DOCX
def extract_text(file_path,file_name):
    if file_name.endswith(".pdf"):
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    elif file_name.endswith(".docx"):
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

# def model_inference(messages):
#     response = openai.ChatCompletion.create(
#         model="gpt-4o-mini",
#         messages=messages,
#         api_key=OPENAI_API_KEY
#     )
#     return response
    
# def analyze_resume_service(resume_text, job_description):
#     prompt = f"""
#     Your Role is to Compare the following resume against the job description and provide feedback:
    
#     **Job Description:**
#     {job_description}
    
#     **Resume:**
#     {resume_text}
    
#     Identify missing skills, relevant experience, and suggestions for improvement.
#     """
#     messages=[{"role": "system", "content": "You are a professional resume evaluator.Provide missing skills, relevant experience, and suggestions for improvement"},
#                   {"role": "user", "content": prompt}]
#     response=model_inference(messages)
#     return response["choices"][0]["message"]["content"]

def analyze_resume_service(resume_text, job_description):
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = f"""  
    Always print output in provided json schema format only.
    ### Task:
    Analyze the provided candidate resume against the given job description. Extract key insights and generate a structured report with the following details:

    Here are the Candidate Information and Job Description:
    **Job Description:**
    {job_description}

    **Resume:**
    {resume_text}
    ---

    ### **1. Candidate Summary**
    Provide a concise summary of the candidate’s professional background, highlighting:
    - Primary industry or domain of expertise.
    - Years of experience.
    - Key competencies and strengths.
    - Notable achievements or recognitions.
    - Overall career trajectory.

    ---

    ### **2. Skills Matching**
    Evaluate how well the candidate’s skills align with the job description by identifying and categorizing:
    - **Hard Skills**: Technical or specialized skills required for the role.
    - **Soft Skills**: Interpersonal, communication, leadership, and teamwork abilities.
    - **Skill Relevance**: Compare the required skills in the job description with the candidate's skills.
    - **Skill Proficiency**: Assess the candidate’s level of expertise based on certifications, endorsements, or experience.

    ---

    ### **3. Job History & Experience**
    Extract and analyze the candidate’s work experience:
    - **Job Titles & Experience**: List job titles held, along with years of experience in each role.
    - **Responsibilities & Achievements**: Provide an overview of responsibilities, accomplishments, and major contributions in previous roles.
    - **Company Information**: Extract details about previous employers, including industry, company size, and market reputation.

    ---

    ### **4. Education & Qualifications**
    Assess the candidate’s educational background and certifications:
    - **Degrees & Institutions**: Extract the highest level of education attained, major field of study, and university attended.
    - **Relevant Certifications**: Identify any professional certifications or training that align with job requirements.
    - **Level of Study Relevance**: Determine whether the candidate’s education matches the required qualification level.

    ---

    ### **5. Keyword Matching**
    Perform keyword extraction and relevance analysis:
    - Identify key terms from the **job description** (skills, tools, qualifications, required experience).
    - Extract matching terms from the **candidate’s resume**.
    - Highlight any **gaps** in required vs. existing skills.

    ---

    ### **6. Strengths & Weaknesses Analysis**
    Provide a structured assessment of the candidate’s strengths and potential weaknesses:
    - **Strengths**: Key areas where the candidate excels based on qualifications, skills, or experience.
    - **Weaknesses**: Any missing skills, gaps in experience, or areas where improvement is needed.

    ---

    ### **7. AI’s Perspective on Job Fit**
    Deliver an AI-driven assessment of how well the candidate matches the job description:
    - Provide a **suitability rating** (e.g., Strong Fit, Moderate Fit, Weak Fit).
    - Justify the rating based on identified strengths, weaknesses, and overall alignment with the job requirements.
    - Suggest whether the candidate should be shortlisted for further review.
    ---
    Ensure that the analysis is **accurate, structured, and relevant** to the job description.
    """
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
                "role": "system",
                "content": "Analyze the resume based on the following criteria."
            },
            {
                "role": "user",
                "content": prompt
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
                        "candidate_summary": {
                            "type": "string",
                            "description": "Provide a concise summary of the candidate’s professional background."
                        },
                        "skills_matching": {
                            "type": "string",
                            "description": "Evaluate how well the candidate’s skills align with the job description by identifying and categorizing."
                        },
                        "job_history_experience": {
                            "type": "string",
                            "description": "Extract and analyze the candidate’s work experience."
                        },
                        "education_qualification": {
                            "type": "string",
                            "description": "Assess the candidate’s educational background and certifications."
                        },
                        "keyword_matching": {
                            "type": "string",
                            "description": "Perform keyword extraction and relevance analysis."
                        },
                        "strength_weakness": {
                            "type": "string",
                            "description": "Provide a structured assessment of the candidate’s strengths and potential weaknesses."
                        },
                        "ai_view": {
                            "type": "string",
                            "description": "Deliver an AI-driven assessment of how well the candidate matches the job description."
                        }
                    },
                    "required": [
                        "candidate_summary",
                        "skills_matching",
                        "job_history_experience",
                        "education_qualification",
                        "keyword_matching",
                        "strength_weakness",
                        "ai_view"
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
    client = OpenAI(api_key=OPENAI_API_KEY)
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
    client = OpenAI(api_key=OPENAI_API_KEY)
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

