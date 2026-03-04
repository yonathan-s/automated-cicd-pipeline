"""
Deployment Metrics Platform - Backend API
Flask application for collecting and analyzing deployment metrics
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

from models import db, Deployment, DeploymentError, DeploymentMetric
from database import init_db, seed_initial_data, get_deployment_statistics

# Create Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///deployments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
init_db(app)

# Seed initial data on first run
with app.app_context():
    seed_initial_data()



# API ENDPOINTS


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'deployment-metrics-platform',
        'timestamp': datetime.utcnow().isoformat()
    })


@app.route('/api/deployments', methods=['GET'])
def get_deployments():
    """Get all deployments with optional filtering"""
    
    # Query parameters
    deployment_type = request.args.get('type')  # 'manual' or 'automated'
    limit = request.args.get('limit', type=int, default=50)
    
    # Build query
    query = Deployment.query
    
    if deployment_type:
        query = query.filter_by(deployment_type=deployment_type)
    
    # Order by most recent first
    deployments = query.order_by(Deployment.timestamp.desc()).limit(limit).all()
    
    return jsonify({
        'deployments': [d.to_dict() for d in deployments],
        'count': len(deployments)
    })


@app.route('/api/deployments', methods=['POST'])
def create_deployment():
    """Create a new deployment record"""
    
    data = request.json
    
    # Validate required fields
    required_fields = ['deployment_type', 'duration_seconds', 'status']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Create deployment
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
    
    # Add errors if provided
    if 'errors' in data and isinstance(data['errors'], list):
        for error_data in data['errors']:
            error = DeploymentError(
                deployment_id=deployment.id,
                error_type=error_data.get('error_type', 'unknown'),
                step_name=error_data.get('step_name'),
                error_message=error_data.get('error_message'),
                time_lost_seconds=error_data.get('time_lost_seconds', 0)
            )
            db.session.add(error)
    
    # Add custom metrics if provided
    if 'metrics' in data and isinstance(data['metrics'], dict):
        for metric_name, value in data['metrics'].items():
            metric = DeploymentMetric(
                deployment_id=deployment.id,
                metric_name=metric_name,
                value=float(value)
            )
            db.session.add(metric)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Deployment recorded successfully',
        'deployment': deployment.to_dict()
    }), 201


@app.route('/api/deployments/<int:deployment_id>', methods=['GET'])
def get_deployment(deployment_id):
    """Get a specific deployment by ID"""
    
    deployment = Deployment.query.get_or_404(deployment_id)
    return jsonify(deployment.to_dict())


@app.route('/api/deployments/<int:deployment_id>', methods=['DELETE'])
def delete_deployment(deployment_id):
    """Delete a deployment"""
    
    deployment = Deployment.query.get_or_404(deployment_id)
    db.session.delete(deployment)
    db.session.commit()
    
    return jsonify({'message': 'Deployment deleted successfully'})


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get deployment statistics"""
    
    stats = get_deployment_statistics()
    
    # Calculate comparison if both types exist
    comparison = None
    if stats['manual'] and stats['automated']:
        manual_avg = stats['manual']['avg_duration']
        auto_avg = stats['automated']['avg_duration']
        
        comparison = {
            'time_improvement_percent': ((manual_avg - auto_avg) / manual_avg) * 100,
            'time_improvement_absolute': manual_avg - auto_avg,
            'error_reduction_percent': ((stats['manual']['avg_errors'] - stats['automated']['avg_errors']) / stats['manual']['avg_errors']) * 100 if stats['manual']['avg_errors'] > 0 else 0,
            'success_rate_improvement': stats['automated']['success_rate'] - stats['manual']['success_rate']
        }
    
    return jsonify({
        'statistics': stats,
        'comparison': comparison
    })


@app.route('/api/statistics/summary', methods=['GET'])
def get_summary():
    """Get summary statistics for dashboard"""
    
    total_deployments = Deployment.query.count()
    manual_count = Deployment.query.filter_by(deployment_type='manual').count()
    automated_count = Deployment.query.filter_by(deployment_type='automated').count()
    
    # Latest deployment
    latest = Deployment.query.order_by(Deployment.timestamp.desc()).first()
    
    # Success rates
    total_success = Deployment.query.filter_by(status='success').count()
    success_rate = (total_success / total_deployments * 100) if total_deployments > 0 else 0
    
    return jsonify({
        'total_deployments': total_deployments,
        'manual_deployments': manual_count,
        'automated_deployments': automated_count,
        'overall_success_rate': success_rate,
        'latest_deployment': latest.to_dict() if latest else None
    })


if __name__ == '__main__':
    print("Starting Deployment Metrics Platform Backend...")
    print("Running on http://localhost:5001")
    print("API Documentation: http://localhost:5001/api/health")
    app.run(debug=True, host='0.0.0.0', port=5001)