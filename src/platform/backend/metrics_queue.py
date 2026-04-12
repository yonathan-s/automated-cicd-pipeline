# This is a prototype in case I add automatic sending of metrics to my backend platform 
# provides a simple file-based queue for deployment metrics.

import json
import os
from datetime import datetime
from pathlib import Path

#AI was used to generate a large part of this file
"""Start of AI code generation"""
# Define the directory where queued deployment files will be stored
QUEUE_DIR = Path(__file__).parent / 'queued_metrics'

def ensure_queue_dir():
    # Create the queued_metrics directory if it doesn't already exist
    # exist_ok=True means don't error if directory already exists
    QUEUE_DIR.mkdir(exist_ok=True)

def queue_deployment(deployment_data):
    # Make sure the queue directory exists before saving files to it
    ensure_queue_dir()
    
    # Create a timestamp string in format: YYYYMMDD_HHMMSS
    # Example: 20260406_143052
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    
    # Get the commit SHA from deployment data, default to 'unknown' if not provided
    # [:7] takes only the first 7 characters (short commit hash format)
    commit_sha = deployment_data.get('commit_sha', 'unknown')[:7]
    
    # Create filename with timestamp and shortened commit SHA
    # Example: deployment_20260406_143052_abc1234.json
    filename = f"deployment_{timestamp}_{commit_sha}.json"
    filepath = QUEUE_DIR / filename
    
    # Write the deployment data to a JSON file
    with open(filepath, 'w') as f:
        json.dump(deployment_data, f, indent=2)
    
    print(f"Queued deployment: {filename}")
    return str(filepath)



def process_queued_deployments():
    # Import database models and Flask app from other modules
    from models import db, Deployment, DeploymentError
    from app import app
    
    # Make sure queue directory exists
    ensure_queue_dir()
    
    # Find all JSON files in the queue directory
    queued_files = list(QUEUE_DIR.glob('*.json'))
    
    # If no files are waiting, return early
    if not queued_files:
        return {'processed': 0, 'message': 'No queued deployments'}
    
    # Initialize counters
    processed = 0
    errors = []
    
    # Process each queued file within the Flask application context
    # (needed to access the database)
    with app.app_context():
        for filepath in queued_files:
            try:
                # Read the JSON file
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                # Create a new Deployment object from the queued data
                deployment = Deployment(
                    deployment_type=data['deployment_type'],
                    commit_sha=data.get('commit_sha'),
                    duration_seconds=data['duration_seconds'],
                    status=data['status'],
                    triggered_by=data.get('triggered_by', 'Unknown'),
                    tests_passed=data.get('tests_passed', True),
                    tests_total=data.get('tests_total', 0),
                    tests_failed=data.get('tests_failed', 0),
                    security_scan_passed=data.get('security_scan_passed', True),
                    security_vulnerabilities=data.get('security_vulnerabilities', 0),
                    errors_count=data.get('errors_count', 0)
                )
                
                # Add deployment to database and save it
                db.session.add(deployment)
                db.session.commit()
                
                # Delete the processed JSON file from disk using unlink()
                # (unlink removes/deletes the file)
                filepath.unlink()
                
                # Increment counter for successfully processed deployments
                processed += 1
                
            except Exception as e:
                # If something goes wrong, record the error message
                errors.append(str(e))
    
    # Return summary of what was processed
    return {
        'processed': processed,
        'errors': errors,
        'message': f'Processed {processed} queued deployments'
    } 

"""End of AI code generation"""