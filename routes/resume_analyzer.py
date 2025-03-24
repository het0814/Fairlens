from flask import Blueprint, render_template, request, redirect, url_for, send_file
from flask import current_app
import os
import io
import ast

from services.dynamodb_service import get_all_jobs, get_job_by_id
from services.openai_service import analyze_resume, score_resume, donut_score_resume
from utils.file_extractors import get_file_text
from services.resume_chart_generator import generate_resume_charts

resume_analyzer_bp = Blueprint('resume_analyzer', __name__)

def calculate_average(donut_analysis_str):
    """
    This function takes in the donut analysis string, parses it into a dictionary,
    and calculates the average score of the values.
    """
    try:
        # Convert the donut_analysis string into a dictionary
        donut_analysis = ast.literal_eval(donut_analysis_str)
        
        # Calculate the average of the values
        average_value = sum(donut_analysis.values()) / len(donut_analysis)
        return average_value
    except Exception as e:
        print(f"Error calculating average: {e}")
        return None

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

        # List to store tuples of (file_name, average_value)
        averages = []

        for resume_file in resume_files:
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], resume_file.filename)
            resume_file.save(file_path)

            resume_text = get_file_text(file_path)
            
            # Perform analysis
            analysis = analyze_resume(resume_text, job_description)
            score = score_resume(resume_text, job_description)
            donut_analysis = donut_score_resume(resume_text, job_description)
            print(f"Donut Analysis: {donut_analysis}")
            average_value = calculate_average(donut_analysis)
            if average_value is not None:
                # Print the calculated average in the console
                print(f"Calculated Average: {average_value}")

            # Store the file name and average value for ranking later
            averages.append((resume_file.filename, average_value))

            # Generate charts
            charts = generate_resume_charts(score, donut_analysis)

            analyses.append({
                "file_name": resume_file.filename, 
                "analysis": analysis, 
                "score": score,
                "donut_analysis": donut_analysis,
                "average_value": average_value,  # Include average value in the analysis result
                "charts": charts
            })

        # If there is more than one resume, sort the averages list based on the average value (descending)
        if len(averages) > 1:
            averages.sort(key=lambda x: x[1], reverse=True)

        # Assign rank to each file and print the file name with rank
        for rank, (file_name, avg) in enumerate(averages, 1):
            print(f"Rank {rank}: {file_name} with Average: {avg}")

        # If there's only one resume, assign it rank 1
        if len(averages) == 1:
            averages = [(averages[0][0], 1, averages[0][1])]  # For single resume, rank is 1
        else:
            # Adding the rank with average score to be passed to the template
            averages = [(file_name, rank, avg) for rank, (file_name, avg) in enumerate(averages, 1)]

        return render_template("resume_analysis_result.html", analyses=analyses, job_info=job_info, averages=averages)
    
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
