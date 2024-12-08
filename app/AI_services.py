from langchain_community.document_loaders import PDFMinerLoader
from huggingface_hub import InferenceClient
import os
import json
from math import pi
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import re 


client = InferenceClient(api_key="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")

def langchain_document_loader(file_path):
    if not file_path.endswith(".pdf"):
        return [], []

    loader = PDFMinerLoader(file_path=file_path)
    documents = loader.load_and_split()

    for i in range(len(documents)):
        documents[i].metadata = {
            "source": documents[i].metadata["source"],
            "doc_number": i,
        }

    gender_words = ['male', 'female', 'transgender', 'lgbtq', 'minority', 'disability']
    gender_found = []
    gender_pattern = r'\b(?:' + '|'.join([re.escape(word) for word in gender_words]) + r')\b'

    for document in documents:
        text = document.page_content.lower()
        matches = re.findall(gender_pattern, text, flags=re.IGNORECASE)

        for gender in gender_words:
            if gender in matches and gender not in gender_found:
                gender_found.append(gender)

    return documents, gender_found

def Model(prompt):
    Model_result = ""
    for message in client.chat_completion(
        model="meta-llama/Llama-3.2-3B-Instruct",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        stream=True
    ):
        Model_result += message.choices[0].delta.content
    return Model_result

def chunk_text(text, max_tokens=4096):
    tokens = text.split()
    chunks = []
    current_chunk = []
    current_token_count = 0

    for token in tokens:
        token_length = len(token.split())
        if current_token_count + token_length > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = [token]
            current_token_count = token_length
        else:
            current_chunk.append(token)
            current_token_count += token_length

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

def process_resume(resume_text, job_description):
    chunks = chunk_text(resume_text)
    final_response = ""

    for chunk in chunks:
        prompt = feature_match_function(chunk, job_description)
        chunk_result = Model(prompt)
        final_response += chunk_result

    return final_response

def feature_match_function(resume_text, job_offer):
    prompt = f"""
    You are an AI assistant specialized in resume analysis and recruitment. Analyze the given resume and compare it with the provided job description. Provide insights, feedback, and recommendations for the recruiter or HR manager. Your response should follow the example structure below.
        Step-1:
        **EXAMPLE RESPONSE STRUCTURE:** 
        **DETAILED ANALYSIS**:
        1. **Overall Match Percentage**: Provide a percentage score that reflects how well the resume aligns with the job description (considering skills, experience, and qualifications).
        2. **Matching Skills**: List the skills mentioned in the job description that are found in the resume.
        3. **Missing Skills**: List the skills from the job description that are not reflected in the resume.
        4. **Experience Relevance**: Analyze how the candidate’s experience aligns with the job description requirements.
        5. **Education/Qualifications Fit**: Evaluate whether the educational background or certifications match the job’s requirements.

        Step-2:
        Provide the output:
        1.**---**: A JSON format detailing the identified matches and their scores in each category using the template below. Ensure that the JSON format is strictly followed to avoid parsing errors:
            {{
            "Soft skills": <soft_skills_score>,
            "Hard skills": <hard_skills_score>,
            "Experience": <experience_score>,
            "Education and certifications": <education_and_certifications_score>,
            "Keywords": <keywords_score>
            }}

    Resume Text: {resume_text}
    Job Description: {job_offer}
    """
    return prompt

def match_report(match_answer):
    def extract_text_analysis(match_answer):
        if "{" not in match_answer or "}" not in match_answer:
            raise ValueError("Parsing error: JSON format not found.")
        json_start = match_answer.index("{")
        json_end = match_answer.rindex("}") + 1
        json_part = match_answer[json_start:json_end]
        text_analysis = match_answer[:json_start].strip()
        scores_dict = json.loads(json_part)
        return text_analysis, scores_dict

    def create_radar_chart(scores_dict):
        fixed_labels = ["Soft skills", "Hard skills", "Experience", "Education and certifications", "Keywords"]
        scores = [scores_dict.get(label, 0) for label in fixed_labels]
        
        num_vars = len(fixed_labels)
        angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
        angles += angles[:1]
        
        scores += scores[:1]
        
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.plot(angles, scores, linewidth=2, linestyle='solid')
        ax.fill(angles, scores, 'r', alpha=0.1)
        plt.xticks(angles[:-1], fixed_labels)
        ax.set_rlabel_position(0)
        plt.yticks([20, 40, 60, 80, 100], ["20", "40", "60", "80", "100"], color="grey", size=7)
        plt.ylim(0, 100)
        return fig

    text_analysis, scores_dict = extract_text_analysis(match_answer)
    fig = create_radar_chart(scores_dict)
    return text_analysis, fig, scores_dict

def resume_screening(resume_text, job_description_text):
    match_answer = process_resume(resume_text, job_description_text)
    try:
        text_analysis, fig, scores_dict = match_report(match_answer)
        buffer = BytesIO()
        fig.savefig(buffer, format="png")
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        buffer.close()
    except Exception as e:
        return {"error": f"Failed to process match report: {str(e)}"}
    return {
        "text_analysis": text_analysis,
        "scores_dict": scores_dict,
        "radar_chart": image_base64
    }

def process_single_resume(resume_file, job_description):
    if resume_file and resume_file.filename.endswith(".pdf"):
        resume_path = os.path.join('uploads', resume_file.filename)
        resume_file.save(resume_path)

        resume_documents, gender_found = langchain_document_loader(resume_path)
        resume_text = " ".join([doc.page_content for doc in resume_documents])

        result = resume_screening(resume_text, job_description)
        result["resume_filename"] = resume_file.filename
        result["gender_found"] = gender_found

        result["total_score"] = sum(result["scores_dict"].values())
        return result
    return None
