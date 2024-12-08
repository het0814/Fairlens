from flask import Flask, request, render_template, jsonify
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
import concurrent.futures
import re  

# Initialize Flask app
app = Flask(__name__)

# Initialize Hugging Face Inference Client
client = InferenceClient(api_key="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")

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def langchain_document_loader(file_path):
    """Load and split a PDF file in Langchain."""
    if not file_path.endswith(".pdf"):
        return [], []

    loader = PDFMinerLoader(file_path=file_path)
    documents = loader.load_and_split()

    # Add metadata
    for i in range(len(documents)):
        documents[i].metadata = {
            "source": documents[i].metadata["source"],
            "doc_number": i,
        }

    # Gender-related words to search for
    gender_words = ['male', 'female', 'transgender', 'lgbtq', 'minority', 'disability']
    gender_found = []

    # Define the regex pattern to match any of the gender words
    gender_pattern = r'\b(?:' + '|'.join([re.escape(word) for word in gender_words]) + r')\b'

    # Check each document for gender-related words
    for document in documents:
        text = document.page_content.lower()  # Convert text to lowercase for case-insensitive matching

        # Use re.findall() to find all exact occurrences of the gender words
        matches = re.findall(gender_pattern, text, flags=re.IGNORECASE)

        # If any gender words are found, add them to the gender_found list
        for gender in gender_words:
            if gender in matches and gender not in gender_found:
                gender_found.append(gender)

    return documents, gender_found

# Function to call the AI model
def Model(prompt):
    """Interact with the model to get results."""
    Model_result = ""
    for message in client.chat_completion(
        model="meta-llama/Llama-3.2-3B-Instruct",  # Model name
        messages=[{"role": "user", "content": prompt}],  # User message with prompt
        max_tokens=500,  # Maximum tokens to generate
        stream=True  # Stream the response as it is generated
    ):
        Model_result += message.choices[0].delta.content
    return Model_result

# Chunking function
def chunk_text(text, max_tokens=4096):
    """Split large text into smaller chunks based on the token limit."""
    tokens = text.split()  # Split the text into individual words (tokens)
    chunks = []
    current_chunk = []
    current_token_count = 0

    for token in tokens:
        # Estimate token count (in most cases, 1 word ≈ 1 token)
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

# Function to process a single resume
def process_resume(resume_text, job_description):
    """Process a single resume with the job description."""
    chunks = chunk_text(resume_text)
    final_response = ""

    for chunk in chunks:
        prompt = feature_match_function(chunk, job_description)  # Use the chunk for analysis
        chunk_result = Model(prompt)  # Get the result from the model for the chunk
        final_response += chunk_result  # Combine results from all chunks

    return final_response

# Feature matching function
def feature_match_function(resume_text, job_offer):
    """Feature match function for analysis."""
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

# Match report generation
def match_report(match_answer):
    """Generate match report with analysis and radar chart."""
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
        """Generate radar chart from scores."""
        # Define fixed order of labels
        fixed_labels = ["Soft skills", "Hard skills", "Experience", "Education and certifications", "Keywords"]
        
        # Ensure the order of scores corresponds to the fixed labels
        scores = [scores_dict.get(label, 0) for label in fixed_labels]  # Default to 0 if key is missing
        
        num_vars = len(fixed_labels)
        angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
        angles += angles[:1]  # Complete the circle
        
        # Add the scores for the radar chart (close the circle by repeating the first score)
        scores += scores[:1]
        
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.plot(angles, scores, linewidth=2, linestyle='solid')
        ax.fill(angles, scores, 'r', alpha=0.1)
        plt.xticks(angles[:-1], fixed_labels)  # Use fixed labels here
        ax.set_rlabel_position(0)
        plt.yticks([20, 40, 60, 80, 100], ["20", "40", "60", "80", "100"], color="grey", size=7)
        plt.ylim(0, 100)
        return fig

    text_analysis, scores_dict = extract_text_analysis(match_answer)
    fig = create_radar_chart(scores_dict)
    return text_analysis, fig, scores_dict

# Resume screening logic
def resume_screening(resume_text, job_description_text):
    """Perform resume screening and generate a report."""
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

# Flask route to render the form
@app.route('/')
def index():
    return render_template('index.html')

# Flask route to handle multiple resume screening
@app.route('/screen_resumes', methods=['POST'])
def screen_resumes():
    if 'resumes' not in request.files:
        return jsonify({"error": "No file part"}), 400

    resumes_files = request.files.getlist('resumes')
    job_description = request.form.get('job_description')

    if not resumes_files:
        return jsonify({"error": "No resumes uploaded"}), 400

    if not job_description:
        return jsonify({"error": "Job description is required"}), 400

    all_results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_resume = {
            executor.submit(process_single_resume, resume_file, job_description): resume_file
            for resume_file in resumes_files
        }

        for future in concurrent.futures.as_completed(future_to_resume):
            resume_file = future_to_resume[future]
            try:
                result = future.result()
                if result:
                    all_results.append(result)
            except Exception as e:
                continue

    if not all_results:
        return jsonify({"error": "No valid resumes processed"}), 500

    # Rank resumes based on total score
    all_results.sort(key=lambda x: x["total_score"], reverse=True)

    # Add ranking info to each result
    for idx, result in enumerate(all_results):
        result["rank"] = idx + 1

    return jsonify(all_results)

# Process a single resume file
def process_single_resume(resume_file, job_description):
    """Process a single resume and return the result."""
    if resume_file and resume_file.filename.endswith(".pdf"):
        resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
        resume_file.save(resume_path)

        resume_documents, gender_found = langchain_document_loader(resume_path)
        resume_text = " ".join([doc.page_content for doc in resume_documents])

        result = resume_screening(resume_text, job_description)
        result["resume_filename"] = resume_file.filename
        result["gender_found"] = gender_found  # Include gender found

        # Compute a total score
        result["total_score"] = sum(result["scores_dict"].values())
        return result
    return None

if __name__ == '__main__':
    app.run(debug=True)
