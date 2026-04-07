from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Deployment(db.Model):
    __tablename__ = 'deployments'

    id = db.Column(db.Integer, primary_key=True)
    deployment_type = db.Column(db.String(50))
    commit_sha = db.Column(db.String(40))
    duration_seconds = db.Column(db.Integer)
    status = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime)
    triggered_by = db.Column(db.String(100))
    tests_passed = db.Column(db.Integer, default=0)
    tests_total = db.Column(db.Integer, default=0)
    tests_failed = db.Column(db.Integer, default=0)
    errors_count = db.Column(db.Integer, default=0)

    errors = db.relationship('DeploymentError', backref='deployment')
    metrics = db.relationship('DeploymentMetric', backref='deployment')

 

    def to_dict(self):
        data = {
            'id': self.id,
            'deployment_type': self.deployment_type,
            'commit_sha': self.commit_sha,
            'duration_seconds': self.duration_seconds,
            'status': self.status,
            'timestamp': self.timestamp.isoformat(),
            'triggered_by': self.triggered_by,
            'tests_passed': self.tests_passed,
            'tests_total': self.tests_total,
            'tests_failed': self.tests_failed,
            'errors_count': self.errors_count,

            #'security_scan_passed': self.security_scan_passed,
            #'security_vulnerabilities': self.security_vulnerabilities,
        }
        data['errors'] = [e.to_dict() for e in self.errors]
        data['metrics'] = {m.metric_name: m.value for m in self.metrics}
        return data


class DeploymentError(db.Model):
    __tablename__ = 'deployment_errors'

    id = db.Column(db.Integer, primary_key=True)
    deployment_id = db.Column(db.Integer, db.ForeignKey('deployments.id'), nullable=False)
    error_type = db.Column(db.String(50))
    step_name = db.Column(db.String(100))
    error_message = db.Column(db.Text)
    time_lost_seconds = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'error_type': self.error_type,
            'step_name': self.step_name,
            'error_message': self.error_message,
            'time_lost_seconds': self.time_lost_seconds
        }


class DeploymentMetric(db.Model):
    __tablename__ = 'deployment_metrics'

    id = db.Column(db.Integer, primary_key=True)
    deployment_id = db.Column(db.Integer, db.ForeignKey('deployments.id'), nullable=False)
    metric_name = db.Column(db.String(50))
    value = db.Column(db.Float)

    def to_dict(self):
        return {
            'metric_name': self.metric_name,
            'value': self.value
        }
    