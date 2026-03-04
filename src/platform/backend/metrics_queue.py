"""
Metrics queue for storing deployments when platform might be offline
This is a simple file-based queue for development
"""

import json
import os
from datetime import datetime
from pathlib import Path

QUEUE_DIR = Path(__file__).parent / 'queued_metrics'

def ensure_queue_dir():
    """Ensure queue directory exists"""
    QUEUE_DIR.mkdir(exist_ok=True)

def queue_deployment(deployment_data):
    """Save deployment data to queue"""
    ensure_queue_dir()
    
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    filename = f"deployment_{timestamp}_{deployment_data.get('commit_sha', 'unknown')[:7]}.json"
    filepath = QUEUE_DIR / filename
    
    with open(filepath, 'w') as f:
        json.dump(deployment_data, f, indent=2)
    
    print(f"Queued deployment: {filename}")
    return str(filepath)

def process_queued_deployments():
    """Process all queued deployments"""
    from models import db, Deployment, DeploymentError
    from app import app
    
    ensure_queue_dir()
    queued_files = list(QUEUE_DIR.glob('*.json'))
    
    if not queued_files:
        return {'processed': 0, 'message': 'No queued deployments'}
    
    processed = 0
    errors = []
    
    with app.app_context():
        for filepath in queued_files:
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                # Create deployment from queued data
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
                
                db.session.add(deployment)
                db.session.commit()
                
                # Delete processed file
                filepath.unlink()
                processed += 1
                
            except Exception as e:
                errors.append(str(e))
    
    return {
        'processed': processed,
        'errors': errors,
        'message': f'Processed {processed} queued deployments'
    } 