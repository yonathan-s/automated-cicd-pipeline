"""
Manual Deployment Simulator
Generates realistic manual deployment data based on manual deployment baseline
"""

import random
from datetime import datetime, timedelta
from models import db, Deployment, DeploymentError

# Manual deployment steps from Week 4
MANUAL_STEPS = [
    {'name': 'Create VPC', 'base_duration': 180, 'error_rate': 0.05},
    {'name': 'Create Subnets', 'base_duration': 240, 'error_rate': 0.10},
    {'name': 'Create Internet Gateway', 'base_duration': 120, 'error_rate': 0.03},
    {'name': 'Create NAT Gateway', 'base_duration': 600, 'error_rate': 0.08},
    {'name': 'Configure Route Tables', 'base_duration': 300, 'error_rate': 0.12},
    {'name': 'Associate Subnets', 'base_duration': 180, 'error_rate': 0.10},
    {'name': 'Create Security Groups', 'base_duration': 420, 'error_rate': 0.15},
    {'name': 'Create IAM Roles', 'base_duration': 480, 'error_rate': 0.08},
    {'name': 'Create ECR Repository', 'base_duration': 120, 'error_rate': 0.05},
    {'name': 'Build Docker Image', 'base_duration': 240, 'error_rate': 0.02},
    {'name': 'Push to ECR', 'base_duration': 300, 'error_rate': 0.05},
    {'name': 'Create ECS Cluster', 'base_duration': 180, 'error_rate': 0.05},
    {'name': 'Create CloudWatch Log Group', 'base_duration': 90, 'error_rate': 0.02},
    {'name': 'Create Task Definition', 'base_duration': 900, 'error_rate': 0.20},
    {'name': 'Create Target Group', 'base_duration': 240, 'error_rate': 0.12},
    {'name': 'Create Application Load Balancer', 'base_duration': 600, 'error_rate': 0.15},
    {'name': 'Create ALB Listener', 'base_duration': 180, 'error_rate': 0.05},
    {'name': 'Create ECS Service', 'base_duration': 720, 'error_rate': 0.18},
    {'name': 'Wait for Service Stabilization', 'base_duration': 420, 'error_rate': 0.03},
    {'name': 'Test Application', 'base_duration': 300, 'error_rate': 0.08}
]

ERROR_TYPES = ['typo', 'wrong_selection', 'missing_step', 'wrong_source', 'wrong_subnet', 'missing_permission', 'configuration_error']

ERROR_MESSAGES = {
    'typo': 'Typing error in configuration',
    'wrong_selection': 'Selected wrong option from dropdown',
    'missing_step': 'Forgot to complete required step',
    'wrong_source': 'Incorrect source/destination specified',
    'wrong_subnet': 'Wrong subnet type selected',
    'missing_permission': 'Forgot to attach required permission',
    'configuration_error': 'Incorrect configuration value'
}


def simulate_manual_deployment(timestamp=None):
    """
    Simulate a single manual deployment based on Week 4 data
    
    Args:
        timestamp: Optional datetime for when deployment occurred
    
    Returns:
        Deployment object
    """
    
    # Base duration from Week 4 (12 hours = 43200 seconds)
    base_duration = 43200
    
    # Add human variability (±30 minutes)
    variance = random.gauss(0, 1800)
    total_duration = int(base_duration + variance)
    
    # Determine if deployment succeeds (75% success rate from Week 4)
    success = random.random() < 0.75
    status = 'success' if success else 'failed'
    
    # Create deployment record
    deployment = Deployment(
        deployment_type='manual',
        duration_seconds=max(total_duration, 3600),  # Minimum 1 hour
        status=status,
        timestamp=timestamp or datetime.utcnow(),
        triggered_by='Manual Simulation',
        tests_passed=success,
        tests_total=5,
        tests_failed=0 if success else random.randint(1, 3),
        security_scan_passed=success,
        security_vulnerabilities=0 if success else random.randint(1, 5),
        errors_count=0
    )
    
    db.session.add(deployment)
    db.session.flush()  # Get deployment ID
    
    # Simulate errors based on error rates
    errors = []
    total_time_lost = 0
    
    for step in MANUAL_STEPS:
        if random.random() < step['error_rate']:
            # Error occurred in this step
            error_type = random.choice(ERROR_TYPES)
            time_lost = random.randint(300, 1800)  # 5-30 minutes
            
            error = DeploymentError(
                deployment_id=deployment.id,
                error_type=error_type,
                step_name=step['name'],
                error_message=ERROR_MESSAGES.get(error_type, 'Unknown error'),
                time_lost_seconds=time_lost
            )
            
            errors.append(error)
            total_time_lost += time_lost
            db.session.add(error)
    
    # Update deployment with error count and adjusted duration
    deployment.errors_count = len(errors)
    deployment.duration_seconds += total_time_lost
    
    db.session.commit()
    
    print(f"Simulated manual deployment: {deployment.format_duration()}, {len(errors)} errors, {status}")
    
    return deployment


def simulate_multiple_deployments(count=10, spread_days=30):
    """
    Simulate multiple manual deployments spread over time
    
    Args:
        count: Number of deployments to simulate
        spread_days: Number of days to spread deployments across
    
    Returns:
        List of Deployment objects
    """
    
    deployments = []
    
    # Calculate time between deployments
    time_delta = timedelta(days=spread_days) / count
    current_time = datetime.utcnow() - timedelta(days=spread_days)
    
    for i in range(count):
        deployment = simulate_manual_deployment(timestamp=current_time)
        deployments.append(deployment)
        
        # Move time forward
        current_time += time_delta
    
    print(f"\nSimulated {count} manual deployments")
    print(f"Success rate: {sum(1 for d in deployments if d.status == 'success') / count * 100:.1f}%")
    print(f"Average duration: {sum(d.duration_seconds for d in deployments) / count / 3600:.1f} hours")
    print(f"Average errors: {sum(d.errors_count for d in deployments) / count:.1f}")
    
    return deployments


def get_simulation_summary():
    """Get summary of simulated deployments"""
    
    manual_sims = Deployment.query.filter_by(
        deployment_type='manual',
        triggered_by='Manual Simulation'
    ).all()
    
    if not manual_sims:
        return {'message': 'No simulated deployments found'}
    
    return {
        'count': len(manual_sims),
        'average_duration_hours': sum(d.duration_seconds for d in manual_sims) / len(manual_sims) / 3600,
        'success_rate': sum(1 for d in manual_sims if d.status == 'success') / len(manual_sims) * 100,
        'average_errors': sum(d.errors_count for d in manual_sims) / len(manual_sims),
        'total_errors': sum(d.errors_count for d in manual_sims)
    }