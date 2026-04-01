"""
Database configuration and initialization
"""

from models import db, Deployment, DeploymentError, DeploymentMetric

def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database initialized successfully")

def seed_initial_data():
    """Seed database with initial manual deployment data from Week 4"""
    
    # Check if data already exists
    if Deployment.query.count() > 0:
        print("Database already has data, skipping seed")
        return
    
    print("Seeding initial manual deployment data...")
    
    # My manual deployment (baseline)
    manual_deployment = Deployment(
        deployment_type='manual',
        duration_seconds=43200,  # 12 hours
        status='success',
        triggered_by='Manual process (Week 4)',
        tests_passed=True,
        tests_total=5,
        tests_failed=0,
        security_scan_passed=True,
        security_vulnerabilities=0,
        errors_count=15
    )
    
    db.session.add(manual_deployment)
    db.session.commit()
    
    # Add the 15 errors from Week 4
    week4_errors = [
        {'step': 'VPC Creation', 'type': 'typo', 'message': 'Wrong CIDR block entered', 'time_lost': 300},
        {'step': 'Subnet Creation', 'type': 'wrong_selection', 'message': 'Selected wrong availability zone', 'time_lost': 600},
        {'step': 'Security Group', 'type': 'wrong_source', 'message': 'Wrong security group source', 'time_lost': 900},
        {'step': 'NAT Gateway', 'type': 'wrong_subnet', 'message': 'Created in private subnet instead of public', 'time_lost': 1800},
        {'step': 'Route Table', 'type': 'missing_association', 'message': 'Forgot to associate subnets', 'time_lost': 1200},
        {'step': 'IAM Role', 'type': 'missing_permission', 'message': 'Forgot to attach policy', 'time_lost': 900},
        {'step': 'ECR Repository', 'type': 'typo', 'message': 'Wrong repository name', 'time_lost': 300},
        {'step': 'ECS Cluster', 'type': 'wrong_setting', 'message': 'Enabled Container Insights (cost)', 'time_lost': 600},
        {'step': 'Task Definition', 'type': 'missing_port', 'message': 'Forgot port mapping', 'time_lost': 1800},
        {'step': 'Task Definition', 'type': 'typo', 'message': 'Wrong ECR image URI', 'time_lost': 900},
        {'step': 'Task Definition', 'type': 'missing_role', 'message': 'Forgot task execution role', 'time_lost': 1200},
        {'step': 'Target Group', 'type': 'wrong_type', 'message': 'Selected Instances instead of IP', 'time_lost': 1800},
        {'step': 'ALB Creation', 'type': 'wrong_subnet', 'message': 'Selected private subnets', 'time_lost': 2700},
        {'step': 'ECS Service', 'type': 'wrong_subnet', 'message': 'Selected public subnets for tasks', 'time_lost': 1800},
        {'step': 'ECS Service', 'type': 'typo', 'message': 'Wrong container name in load balancer config', 'time_lost': 1200}
    ]
    
    for error_data in week4_errors:
        error = DeploymentError(
            deployment_id=manual_deployment.id,
            error_type=error_data['type'],
            step_name=error_data['step'],
            error_message=error_data['message'],
            time_lost_seconds=error_data['time_lost']
        )
        db.session.add(error)
    
    db.session.commit()
    
    print(f"Seeded 1 manual deployment with {len(week4_errors)} errors")

def get_deployment_statistics():
    """Calculate deployment statistics"""
    
    manual_deployments = Deployment.query.filter_by(deployment_type='manual').all()
    automated_deployments = Deployment.query.filter_by(deployment_type='automated').all()
    
    def calculate_stats(deployments):
        if not deployments or len(deployments) == 0:
            return {
                'count': 0,
                'avg_duration': 0,
                'min_duration': 0,
                'max_duration': 0,
                'avg_errors': 0,
                'success_rate': 0
            }

        durations = [d.duration_seconds for d in deployments if d.duration_seconds is not None]
        errors = [d.errors_count for d in deployments if d.errors_count is not None]
        success_count = sum(1 for d in deployments if d.status == 'success')

        return {
            'count': len(deployments),
            'avg_duration': sum(durations) / len(durations) if durations else 0,
            'min_duration': min(durations) if durations else 0,
            'max_duration': max(durations) if durations else 0,
            'avg_errors': sum(errors) / len(errors) if errors else 0,
            'success_rate': (success_count / len(deployments)) * 100 if deployments else 0
        }
    
    return {
        'manual': calculate_stats(manual_deployments),
        'automated': calculate_stats(automated_deployments)
    }