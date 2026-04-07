import numpy as np
from scipy import stats
from models import Deployment

def stats_with_description(deployments):
    #I'll use successful deployments
    successful_deployments = [d for d in deployments if d.status == 'success']
    success_count = len(successful_deployments)

    #all deployments still count for to coount metrics for reliability + errors rates
    total_count = len(deployments)
    errors = [d.errors_count for d in deployments]

    if successful_deployments:
        durations = [d.duration_seconds for d in successful_deployments]
        mean_duration = np.mean(durations)
        median_duration = np.median(durations)
        std_duration = np.std(durations)
        min_duration = np.min(durations)
        max_duration = np.max(durations)
    else:
        mean_duration = 0
        median_duration = 0
        std_duration = 0
        min_duration = 0
        max_duration = 0


    return {
        'count': total_count,
        'successful_count': success_count,
        'mean_duration': mean_duration,
        'median_duration': median_duration,
        'std_duration': std_duration,
        'min_duration': min_duration,
        'max_duration': max_duration,
        'mean_errors': np.mean(errors) if errors else 0,
        'median_errors': np.median(errors) if errors else 0,
        'total_errors': np.sum(errors) if errors else 0,
        'success_count': success_count,
        'success_rate': (success_count / total_count) * 100 if total_count > 0 else 0
    }


def t_test(manual_deployments, automated_deployments):
    
    manual_successful = [d for d in manual_deployments if d.status == 'success']
    automated_successful = [d for d in automated_deployments if d.status == 'success']
    
    manual_durations = [d.duration_seconds for d in manual_successful]
    auto_durations = [d.duration_seconds for d in automated_successful]
    
    #ttest_ind does a t-test on the means of manual and automated times
    t_stat, p_value = stats.ttest_ind(manual_durations, auto_durations)
    
    mean_diff = np.mean(manual_durations) - np.mean(auto_durations)

    deviation = np.sqrt(
        ((len(manual_durations) - 1) * np.std(manual_durations, ddof=1)**2 + 
         (len(auto_durations) - 1) * np.std(auto_durations, ddof=1)**2) / (len(manual_durations) + len(auto_durations) - 2)
    )
    cohens_d = mean_diff / deviation if deviation > 0 else 0
    
    significant = p_value < 0.05
    effect_size_interpretation = cohens_d_interp(cohens_d)
    
    return {
        't_statistic': float(t_stat),
        'p_value': float(p_value),
        'degrees_of_freedom': len(manual_durations) + len(auto_durations) - 2,
        'significant': significant,
        'cohens_d': float(cohens_d),
        'effect_size': effect_size_interpretation,
        'manual_sample_size': len(manual_durations),
        'automated_sample_size': len(auto_durations),
        'interpretation': get_t_test_interpretation(significant, cohens_d)
    }

#COME BACK TO THIS LATER!
"""
def chi_square_tests(manual_deployments, automated_deployments):

    
    manual_success = sum(1 for d in manual_deployments if d.status == 'success')
    manual_failure = len(manual_deployments) - manual_success
    
    auto_success = sum(1 for d in automated_deployments if d.status == 'success')
    auto_failure = len(automated_deployments) - auto_success
    
    A = np.array([manual_success, auto_success])
    
    # will do for now but come back to
    chi2, p_value = stats.chisquare(A)
    significant = p_value < 0.05
    
    return {
        'chi_square': float(chi2),
        'p_value': float(p_value),
        'significant': significant,
        'manual_success_rate': (manual_success / len(manual_deployments)) * 100,
        'automated_success_rate': (auto_success / len(automated_deployments)) * 100,
        'interpretation': get_chi_square_interpretation(significant)
    }

"""

#gives me a range of plausible deployment times based on my sample data (confidence level)
def clevel(deployments, confidence=0.95):
    
    successful_deployments = [d for d in deployments if d.status == 'success']
   
    durations = [d.duration_seconds for d in successful_deployments]
    
    mean = np.mean(durations)
    std_error = stats.sem(durations)
    interval = std_error * stats.t.ppf((1 + confidence) / 2, len(durations) - 1)
    
    return {
        'mean': float(mean),
        'confidence_level': confidence,
        'lower_bound': float(mean - interval),
        'upper_bound': float(mean + interval),
        'margin': float(interval)
    }


def perform_analysis():
    
    manual_deployments = Deployment.query.filter_by(deployment_type='manual').all()
    automated_deployments = Deployment.query.filter_by(deployment_type='automated').all()
    

    manual_stats = stats_with_description(manual_deployments)
    automated_stats = stats_with_description(automated_deployments)
    
    improvement = None
    if manual_stats and automated_stats:
        improvement = {
            'time_reduction_percent': ((manual_stats['mean_duration'] - automated_stats['mean_duration']) / manual_stats['mean_duration']) * 100,
            'time_reduction_seconds': manual_stats['mean_duration'] - automated_stats['mean_duration'],
            'error_reduction_percent': ((manual_stats['mean_errors'] - automated_stats['mean_errors']) / manual_stats['mean_errors'] * 100) if manual_stats['mean_errors'] > 0 else 0,
            'success_rate_improvement': automated_stats['success_rate'] - manual_stats['success_rate']
        }

    t_tests = t_test(manual_deployments, automated_deployments)

    # Provide values when done
    chi_square_results = {
        'chi_square': 'N/A',
        'p_value': 'N/A',
        'degrees_of_freedom': 'N/A',
        'significant': False,
        'manual_success_rate': 'N/A',
        'automated_success_rate': 'N/A',
        'interpretation': 'N/A'
    }
    manual_ci = clevel(manual_deployments)
    automated_ci = clevel(automated_deployments)
    return {
        'descriptive_statistics': {
            'manual': manual_stats,
            'automated': automated_stats
        },
        'improved_statistics': {
            't_test': t_tests,
            'chi_square': chi_square_results
        },
        'confidence_intervals': {
            'manual': manual_ci,
            'automated': automated_ci
        },
        'improvement_metrics': improvement
    }


def cohens_d_interp(d):
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
    if significant:
        effect_size = cohens_d_interp(cohens_d)
        return f"Automated deployments are significantly faster than manual deployment with an effect size of: {effect_size}, This means the CI/CD pipeline produces a  speed improvement"
    else:
        return "No significant speed differences was found between automated and manual deployments. The difference could be due to chance (p ≥ 0.05), meaning the sample data does not strongly support a consistent time improvement."


#ncomment when chi-square tests are done properly
"""def get_chi_square_interpretation(significant):
    if significant:
        return "Automated and mannual deployments differ significantly in their success rates. Unlikely to be due to chance (p < 0.05)"
    else:
        return "No significant difference in success rates was found between automated and manual deployment. The observed difference could be due to chance (p ≥ 0.05), and the data does not strongly support a reliability improvement."
        """