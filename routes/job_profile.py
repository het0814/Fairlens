from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.dynamodb_service import get_dynamodb_client, get_all_jobs
import boto3

job_profile_bp = Blueprint('job_profile', __name__)

def get_dynamodb_client():
    return boto3.client(
        'dynamodb',
        region_name='us-east-1',
        aws_access_key_id='AKIAW5WU44QWFRJXFF54',
        aws_secret_access_key='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'
    )

@job_profile_bp.route('/save_job_profile', methods=['POST'])
def save_job_profile():
    dynamodb = get_dynamodb_client()
    
    job_id = request.form.get('jobId')
    job_name = request.form.get('jobName')
    job_description = request.form.get('qualifications')
    
    try:
        dynamodb.put_item(
            TableName='Job_Profile',
            Item={
                'id': {'N': job_id},
                'Job_name': {'S': job_name},
                'Job_description': {'S': job_description}
            }
        )
        flash('Job profile saved successfully!', 'success')
        return redirect(url_for('home.home'))
    except Exception as e:
        flash(f'Error saving job profile: {str(e)}', 'error')
        return redirect(url_for('home.home'))

@job_profile_bp.route('/update_job_profile', methods=['POST'])
def update_job_profile():
    dynamodb = get_dynamodb_client()
    
    job_id = request.form.get('jobId')
    job_name = request.form.get('jobName')
    job_description = request.form.get('qualifications')
    
    try:
        dynamodb.update_item(
            TableName='Job_Profile',
            Key={'id': {'N': job_id}},
            UpdateExpression='SET Job_name = :name, Job_description = :desc',
            ExpressionAttributeValues={
                ':name': {'S': job_name},
                ':desc': {'S': job_description}
            }
        )
        flash('Job profile updated successfully!', 'success')
        return redirect(url_for('home.home'))
    except Exception as e:
        flash(f'Error updating job profile: {str(e)}', 'error')
        return redirect(url_for('home.home'))

@job_profile_bp.route('/delete_job_profile/<job_id>')
def delete_job_profile(job_id):
    dynamodb = get_dynamodb_client()
    
    try:
        dynamodb.delete_item(
            TableName='Job_Profile',
            Key={'id': {'N': job_id}}
        )
        flash('Job profile deleted successfully!', 'success')
        return redirect(url_for('home.home'))
    except Exception as e:
        flash(f'Error deleting job profile: {str(e)}', 'error')
        return redirect(url_for('home.home'))