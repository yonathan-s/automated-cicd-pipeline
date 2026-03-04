"""
Database models for deployment metrics platform
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Deployment(db.Model):
    """Represents a single deployment (manual or automated)"""
    
    __tablename__ = 'deployments'
    
    id = db.Column(db.Integer, primary_key=True)
    deployment_type = db.Column(db.String(50), nullable=False)  # 'manual', 'automated'
    commit_sha = db.Column(db.String(40))
    duration_seconds = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'success', 'failed'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    triggered_by = db.Column(db.String(100))
    
    # Test and security info
    tests_passed = db.Column(db.Boolean, default=True)
    tests_total = db.Column(db.Integer, default=0)
    tests_failed = db.Column(db.Integer, default=0)
    security_scan_passed = db.Column(db.Boolean, default=True)
    security_vulnerabilities = db.Column(db.Integer, default=0)
    
    # Error tracking
    errors_count = db.Column(db.Integer, default=0)
    
    # Relationships
    errors = db.relationship('DeploymentError', backref='deployment', lazy=True, cascade='all, delete-orphan')
    metrics = db.relationship('DeploymentMetric', backref='deployment', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert deployment to dictionary"""
        return {
            'id': self.id,
            'deployment_type': self.deployment_type,
            'commit_sha': self.commit_sha,
            'duration_seconds': self.duration_seconds,
            'duration_formatted': self.format_duration(),
            'status': self.status,
            'timestamp': self.timestamp.isoformat(),
            'triggered_by': self.triggered_by,
            'tests_passed': self.tests_passed,
            'tests_total': self.tests_total,
            'tests_failed': self.tests_failed,
            'security_scan_passed': self.security_scan_passed,
            'security_vulnerabilities': self.security_vulnerabilities,
            'errors_count': self.errors_count,
            'errors': [e.to_dict() for e in self.errors],
            'metrics': {m.metric_name: m.value for m in self.metrics}
        }
    
    def format_duration(self):
        """Format duration as human-readable string"""
        seconds = self.duration_seconds
        
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            minutes = seconds // 60
            secs = seconds % 60
            return f"{minutes}m {secs}s"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours}h {minutes}m"


class DeploymentError(db.Model):
    """Represents an error that occurred during deployment"""
    
    __tablename__ = 'deployment_errors'
    
    id = db.Column(db.Integer, primary_key=True)
    deployment_id = db.Column(db.Integer, db.ForeignKey('deployments.id'), nullable=False)
    error_type = db.Column(db.String(50), nullable=False)
    step_name = db.Column(db.String(100))
    error_message = db.Column(db.Text)
    time_lost_seconds = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        """Convert error to dictionary"""
        return {
            'id': self.id,
            'error_type': self.error_type,
            'step_name': self.step_name,
            'error_message': self.error_message,
            'time_lost_seconds': self.time_lost_seconds
        }


class DeploymentMetric(db.Model):
    """Represents a custom metric for a deployment"""
    
    __tablename__ = 'deployment_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    deployment_id = db.Column(db.Integer, db.ForeignKey('deployments.id'), nullable=False)
    metric_name = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20))
    
    def to_dict(self):
        """Convert metric to dictionary"""
        return {
            'id': self.id,
            'metric_name': self.metric_name,
            'value': self.value,
            'unit': self.unit
        }