
from models import db, Deployment, DeploymentError, DeploymentMetric

def init_db(app):
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        print("Database initialized successfully")

def get_deployment_statistics():
    
    manual_deployments = Deployment.query.filter_by(deployment_type='manual').all()
    automated_deployments = Deployment.query.filter_by(deployment_type='automated').all() 
    
    def calculate_stats(deployments):
        if len(deployments) == 0:
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
            'avg_duration': sum(durations) / len(durations),
            'min_duration': min(durations),
            'max_duration': max(durations),
            'avg_errors': sum(errors) / len(errors),
            'success_rate': (success_count / len(deployments)) * 100 
        }
    
    
    return {
        'manual': calculate_stats(manual_deployments),
        'automated': calculate_stats(automated_deployments)
    }