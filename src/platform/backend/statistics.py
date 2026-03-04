"""
Statistical Analysis Module
Performs statistical tests on deployment data
"""

import numpy as np
from scipy import stats
from models import Deployment

def calculate_descriptive_stats(deployments):
    """Calculate descriptive statistics for a list of deployments"""
    
    if not deployments:
        return None
    
    durations = [d.duration_seconds for d in deployments]
    errors = [d.errors_count for d in deployments]
    success_count = sum(1 for d in deployments if d.status == 'success')
    
    return {
        'count': len(deployments),
        'mean_duration': np.mean(durations),
        'median_duration': np.median(durations),
        'std_duration': np.std(durations),
        'min_duration': np.min(durations),
        'max_duration': np.max(durations),
        'mean_errors': np.mean(errors),
        'median_errors': np.median(errors),
        'total_errors': np.sum(errors),
        'success_count': success_count,
        'success_rate': (success_count / len(deployments)) * 100
    }


def perform_t_test(manual_deployments, automated_deployments):
    """
    Perform independent samples t-test comparing deployment durations
    
    Returns t-statistic, p-value, and interpretation
    """
    
    if not manual_deployments or not automated_deployments:
        return None
    
    manual_durations = [d.duration_seconds for d in manual_deployments]
    auto_durations = [d.duration_seconds for d in automated_deployments]
    
    # Perform independent samples t-test
    t_stat, p_value = stats.ttest_ind(manual_durations, auto_durations)
    
    # Calculate effect size (Cohen's d)
    mean_diff = np.mean(manual_durations) - np.mean(auto_durations)
    pooled_std = np.sqrt(
        ((len(manual_durations) - 1) * np.std(manual_durations, ddof=1)**2 + 
         (len(auto_durations) - 1) * np.std(auto_durations, ddof=1)**2) / 
        (len(manual_durations) + len(auto_durations) - 2)
    )
    cohens_d = mean_diff / pooled_std if pooled_std > 0 else 0
    
    # Interpret results
    significant = p_value < 0.05
    effect_size_interpretation = interpret_cohens_d(cohens_d)
    
    return {
        't_statistic': float(t_stat),
        'p_value': float(p_value),
        'degrees_of_freedom': len(manual_durations) + len(auto_durations) - 2,
        'significant': significant,
        'cohens_d': float(cohens_d),
        'effect_size': effect_size_interpretation,
        'interpretation': get_t_test_interpretation(significant, cohens_d)
    }


def perform_chi_square_test(manual_deployments, automated_deployments):
    """
    Perform chi-square test for success rates
    
    Returns chi-square statistic, p-value, and interpretation
    """
    
    if not manual_deployments or not automated_deployments:
        return None
    
    # Count successes and failures
    manual_success = sum(1 for d in manual_deployments if d.status == 'success')
    manual_failure = len(manual_deployments) - manual_success
    
    auto_success = sum(1 for d in automated_deployments if d.status == 'success')
    auto_failure = len(automated_deployments) - auto_success
    
    # Create contingency table
    observed = np.array([
        [manual_success, manual_failure],
        [auto_success, auto_failure]
    ])
    
    # Perform chi-square test
    chi2, p_value, dof, expected = stats.chi2_contingency(observed)
    
    significant = p_value < 0.05
    
    return {
        'chi_square': float(chi2),
        'p_value': float(p_value),
        'degrees_of_freedom': int(dof),
        'significant': significant,
        'manual_success_rate': (manual_success / len(manual_deployments)) * 100,
        'automated_success_rate': (auto_success / len(automated_deployments)) * 100,
        'interpretation': get_chi_square_interpretation(significant)
    }


def calculate_confidence_interval(deployments, confidence=0.95):
    """Calculate confidence interval for mean deployment duration"""
    
    if not deployments:
        return None
    
    durations = [d.duration_seconds for d in deployments]
    
    mean = np.mean(durations)
    std_error = stats.sem(durations)
    interval = std_error * stats.t.ppf((1 + confidence) / 2, len(durations) - 1)
    
    return {
        'mean': float(mean),
        'confidence_level': confidence,
        'lower_bound': float(mean - interval),
        'upper_bound': float(mean + interval),
        'margin_of_error': float(interval)
    }


def perform_full_analysis():
    """Perform complete statistical analysis on all deployments"""
    
    manual_deployments = Deployment.query.filter_by(deployment_type='manual').all()
    automated_deployments = Deployment.query.filter_by(deployment_type='automated').all()
    
    # Descriptive statistics
    manual_stats = calculate_descriptive_stats(manual_deployments)
    automated_stats = calculate_descriptive_stats(automated_deployments)
    
    # Inferential statistics
    t_test_results = perform_t_test(manual_deployments, automated_deployments)
    chi_square_results = perform_chi_square_test(manual_deployments, automated_deployments)
    
    # Confidence intervals
    manual_ci = calculate_confidence_interval(manual_deployments)
    automated_ci = calculate_confidence_interval(automated_deployments)
    
    # Calculate improvement metrics
    improvement = None
    if manual_stats and automated_stats:
        improvement = {
            'time_reduction_percent': ((manual_stats['mean_duration'] - automated_stats['mean_duration']) / manual_stats['mean_duration']) * 100,
            'time_reduction_seconds': manual_stats['mean_duration'] - automated_stats['mean_duration'],
            'error_reduction_percent': ((manual_stats['mean_errors'] - automated_stats['mean_errors']) / manual_stats['mean_errors'] * 100) if manual_stats['mean_errors'] > 0 else 0,
            'success_rate_improvement': automated_stats['success_rate'] - manual_stats['success_rate']
        }
    
    return {
        'descriptive_statistics': {
            'manual': manual_stats,
            'automated': automated_stats
        },
        'inferential_statistics': {
            't_test': t_test_results,
            'chi_square': chi_square_results
        },
        'confidence_intervals': {
            'manual': manual_ci,
            'automated': automated_ci
        },
        'improvement_metrics': improvement
    }


def interpret_cohens_d(d):
    """Interpret Cohen's d effect size"""
    abs_d = abs(d)
    if abs_d < 0.2:
        return 'negligible'
    elif abs_d < 0.5:
        return 'small'
    elif abs_d < 0.8:
        return 'medium'
    else:
        return 'large'


def get_t_test_interpretation(significant, cohens_d):
    """Get human-readable interpretation of t-test results"""
    if significant:
        effect_size = interpret_cohens_d(cohens_d)
        return f"The difference in deployment times is statistically significant (p < 0.05) with a {effect_size} effect size. Automated deployments are significantly faster than manual deployments."
    else:
        return "The difference in deployment times is not statistically significant (p >= 0.05). There is insufficient evidence to conclude that automated deployments are faster."


def get_chi_square_interpretation(significant):
    """Get human-readable interpretation of chi-square test results"""
    if significant:
        return "The difference in success rates is statistically significant (p < 0.05). Automated deployments have a significantly different success rate compared to manual deployments."
    else:
        return "The difference in success rates is not statistically significant (p >= 0.05)."