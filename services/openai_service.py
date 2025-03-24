from openai import OpenAI
from flask import current_app
import json

def get_openai_client():
    return OpenAI(api_key=current_app.config['OPENAI_API_KEY'])
def analyze_resume(resume_text, job_description):
    client = get_openai_client()
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


def score_resume(resume_text, job_description):
    client = get_openai_client()
    prompt = f"""  
    ### Task:
Analyze the provided candidate resume against the given job description and evaluate the candidate’s suitability based on the following five key parameters. Assign a **score out of 100** for each parameter based on relevance, depth, and alignment with the job description.  

Provide a structured evaluation by considering skills, experience, adaptability, education, and overall impact.  

---

### **Evaluation Criteria & Scoring Parameters**:  

--**Technical Compatibility (0-100)**  
   - Assess how well the candidate’s **technical skills, tools, and technologies** align with the job description.  
   - Consider **hands-on experience**, **certifications**, **software proficiency**, **coding languages**, **technical frameworks**, or any other job-specific technical expertise.  
   - Evaluate the depth of experience in using these technologies and the candidate’s ability to apply them in real-world scenarios.  

-- **Industry Experience (0-100)**  
   - Determine if the candidate has **experience within the same industry** as the job posting.  
   - Consider factors such as **previous companies, industry-specific projects, sector knowledge, and regulatory familiarity** (if applicable).  
   - Evaluate whether the candidate understands industry best practices, challenges, and trends.  

--**Workplace Adaptability (0-100)**  
   - Assess the candidate’s ability to **adapt to different work environments, company cultures, and team dynamics**.  
   - Look at previous roles, job transitions, remote/hybrid work experience, or ability to work under pressure.  
   - Identify mentions of **collaboration, problem-solving, leadership adaptability, or working in fast-paced environments**.  

--**Educational Strength (0-100)**  
   - Analyze whether the candidate’s **academic background aligns with the job requirements**.  
   - Consider **degree level (Bachelor’s, Master’s, Ph.D.), major or specialization, and additional relevant certifications**.  
   - Evaluate whether the candidate possesses specialized education **directly related to the job role**.  

--**Performance Impact (0-100)**  
   - Evaluate how much measurable **impact** the candidate has made in previous roles.  
   - Look at contributions in terms of **efficiency improvements, revenue growth, project success, leadership influence, or innovative solutions**.  
   - Identify **quantifiable achievements**.  

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
                        "text": "Analyze the following resume analysis and provide scores out of 100"
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
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
                        "technical_compatibility": {
                            "type": "number",
                            "description": "Score (0-100) for how well the candidate’s technical skills, tools, and technologies align with the job."
                        },
                        "industry_experience": {
                            "type": "number",
                            "description": "Score (0-100) evaluating the candidate’s experience in the relevant industry."
                        },
                        "workplace_adaptability": {
                            "type": "number",
                            "description": "Score (0-100) for the candidate’s ability to adapt to different work environments and cultures."
                        },
                        "educational_strength": {
                            "type": "number",
                            "description": "Score (0-100) evaluating how well the candidate’s academic background aligns with the role."
                        },
                        "performance_impact": {
                            "type": "number",
                            "description": "Score (0-100) reflecting the candidate’s past measurable contributions and achievements."
                        }
                    },
                    "required": [
                        "technical_compatibility",
                        "industry_experience",
                        "workplace_adaptability",
                        "educational_strength",
                        "performance_impact"
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


def donut_score_resume(resume_text, job_description):
    client = get_openai_client()
    prompt = f""" 
    ### Task:
Analyze the provided candidate resume against the given job description and evaluate the candidate based on the following five key parameters. Assign a **score out of 100** for each parameter based on relevance, depth, and alignment with professional growth.

The final output should be structured to generate a **donut chart visualization**, where each parameter is assigned a score.

---

### **Evaluation Criteria & Scoring Parameters**:  

-- **Career Stability & Progression (0-100)**  
   - Assess how **consistent** and **progressive** the candidate’s career has been.  
   - Look at **job transitions, promotions, tenure at each company, and career growth over time**.  

-- **Continuous Learning & Upskilling (0-100)**  
   - Evaluate the candidate’s commitment to **ongoing education, certifications, and skill enhancements**.  

-- **Diversity of Experience (0-100)**  
   - Assess the **variety** in the candidate’s work experience across **industries, roles, or domains**.  

-- **Project Experience (0-100)**  
   - Evaluate **practical exposure to academic, professional, or personal projects**, including impact and leadership.  

-- **Extracurricular & Volunteering (0-100)**  
   - Review **non-work activities** like volunteering, mentoring, or leadership in extracurriculars.  

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
                        "text": "Analyze the following resume analysis and provide scores out of 100"
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "resume_score_donut",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "career_stability_and_progression": {
                            "type": "number",
                            "description": "Score (0-100) evaluating consistency, tenure, and upward mobility in career."
                        },
                        "continuous_learning_and_upskilling": {
                            "type": "number",
                            "description": "Score (0-100) reflecting ongoing education, certifications, and personal development."
                        },
                        "diversity_of_experience": {
                            "type": "number",
                            "description": "Score (0-100) assessing the variety of industries, roles, or job functions."
                        },
                        "project_experience": {
                            "type": "number",
                            "description": "Score (0-100) evaluating practical and leadership involvement in projects."
                        },
                        "extracurricular_and_volunteering": {
                            "type": "number",
                            "description": "Score (0-100) reflecting community engagement, mentoring, or extracurricular leadership."
                        }
                    },
                    "required": [
                        "career_stability_and_progression",
                        "continuous_learning_and_upskilling",
                        "diversity_of_experience",
                        "project_experience",
                        "extracurricular_and_volunteering"
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
