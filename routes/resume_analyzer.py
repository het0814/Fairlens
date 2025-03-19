# routes/resume_analyze.py
from flask import Blueprint, render_template, request, redirect, url_for, send_file
from flask import current_app
import os
import io

from services.dynamodb_service import get_all_jobs, get_job_by_id
from services.openai_service import analyze_resume, score_resume, donut_score_resume
from utils.file_extractors import get_file_text
from services.resume_chart_generator import generate_resume_charts

resume_analyzer_bp = Blueprint('resume_analyzer', __name__)

@resume_analyzer_bp.route('/', methods=['GET', 'POST'])
def resume_analyzer():
    jobs = get_all_jobs()
    if request.method == 'POST':
        job_id = request.form.get("job_id")
        resume_files = request.files.getlist("resume")
        
        job_info = get_job_by_id(job_id)
        if not job_info:
            return redirect(url_for("home.home", message="Job not found"))

        job_description = job_info.get("Job_description", {}).get("S", "")
        analyses = []

        for resume_file in resume_files:
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], resume_file.filename)
            resume_file.save(file_path)

            resume_text = get_file_text(file_path)
            
            # Perform analysis
            analysis = analyze_resume(resume_text, job_description)
            score = score_resume(resume_text,job_description)
            donut_analysis = donut_score_resume(resume_text,job_description)

            # Generate charts
            charts = generate_resume_charts(score, donut_analysis)

            analyses.append({
                "file_name": resume_file.filename, 
                "analysis": analysis, 
                "score": score,
                "donut_analysis": donut_analysis,
                "charts": charts
            })

        return render_template("resume_analysis_result.html", analyses=analyses, job_info=job_info)
    
    return render_template("resume_analyzer.html", jobs=jobs)

@resume_analyzer_bp.route('/download_chart', methods=['POST'])
def download_chart():
    import base64
    chart_data = request.form.get('chart_data')
    chart_type = request.form.get('chart_type')
    
    # Decode base64 image
    image_data = base64.b64decode(chart_data)
    
    # Create a file-like object
    image_stream = io.BytesIO(image_data)
    
    # Send the file for download
    return send_file(
        image_stream, 
        mimetype='image/png', 
        as_attachment=True, 
        download_name=f'{chart_type}_chart.png'
    )