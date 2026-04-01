"""
Deployment Metrics Platform - Backend API
Flask application for collecting and analyzing deployment metrics
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
import numpy as np
from flask.json.provider import DefaultJSONProvider

from models import db, Deployment, DeploymentError, DeploymentMetric
from database import init_db, seed_initial_data, get_deployment_statistics

from simulator import simulate_manual_deployment, simulate_multiple_deployments, get_simulation_summary


from statistics import perform_full_analysis, calculate_descriptive_stats

from metrics_queue import process_queued_deployments

class NumpyJSONProvider(DefaultJSONProvider):
    """Custom JSON provider to handle NumPy types"""
    def default(self, o):
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        if isinstance(o, np.bool_):  
            return bool(o)           
        if isinstance(o, np.ndarray):
            return o.tolist()
        return super().default(o)

# Create Flask app
app = Flask(__name__)
app.json = NumpyJSONProvider(app)
CORS(app)


# Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, 'deployments.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
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
    
        # Parse optional timestamp from request
    deployment_timestamp = None
    if data.get('timestamp'):
        try:
            deployment_timestamp = datetime.fromisoformat(
                data['timestamp'].replace('Z', '+00:00')
            )
        except ValueError:
            return jsonify({'error': 'Invalid timestamp format. Use ISO 8601 format.'}), 400

    # Create deployment
    deployment = Deployment(
        deployment_type=data['deployment_type'],
        commit_sha=data.get('commit_sha'),
        duration_seconds=data['duration_seconds'],
        status=data['status'],
        timestamp=deployment_timestamp if deployment_timestamp else datetime.utcnow(),
        triggered_by=data.get('triggered_by', 'Unknown'),
        tests_passed=data.get('tests_passed', 0),
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

        # Prevent division by zero
        time_improvement = 0
        if manual_avg > 0:
            time_improvement = ((manual_avg - auto_avg) / manual_avg) * 100

        error_reduction = 0
        if stats['manual']['avg_errors'] > 0:
            error_reduction = (
                (stats['manual']['avg_errors'] - stats['automated']['avg_errors'])
                / stats['manual']['avg_errors']
            ) * 100

        comparison = {
            'time_improvement_percent': time_improvement,
            'time_improvement_absolute': manual_avg - auto_avg,
            'error_reduction_percent': error_reduction,
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

@app.route('/api/analysis/full', methods=['GET'])
def get_full_analysis():
    """Get complete statistical analysis"""
    
    analysis = perform_full_analysis()
    return jsonify(analysis)

@app.route('/api/queue/process', methods=['POST'])
def process_queue():
    """Process queued deployment metrics"""
    result = process_queued_deployments()
    return jsonify(result)


# SIMULATOR ENDPOINTS


@app.route('/api/simulate/manual', methods=['POST'])
def simulate_single_manual():
    """Simulate a single manual deployment"""
    
    deployment = simulate_manual_deployment()
    
    return jsonify({
        'message': 'Manual deployment simulated',
        'deployment': deployment.to_dict()
    }), 201


@app.route('/api/simulate/manual/batch', methods=['POST'])
def simulate_batch_manual():
    """Simulate multiple manual deployments"""
    
    data = request.json or {}
    count = data.get('count', 10)
    spread_days = data.get('spread_days', 30)
    
    deployments = simulate_multiple_deployments(count=count, spread_days=spread_days)
    
    return jsonify({
        'message': f'Simulated {count} manual deployments',
        'count': len(deployments),
        'deployments': [d.to_dict() for d in deployments]
    }), 201


@app.route('/api/simulate/summary', methods=['GET'])
def get_sim_summary():
    """Get summary of simulated deployments"""
    
    summary = get_simulation_summary()
    return jsonify(summary)





if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    print("Starting Deployment Metrics Platform Backend...")
    print(f"Running on http://0.0.0.0:{port}")
    print(f"API Documentation: http://0.0.0.0:{port}/api/health")
    app.run(debug=True, host='0.0.0.0', port=port)