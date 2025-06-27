from datetime import timedelta
from typing import List

def calculate_total_time(timedelta_list: List[timedelta]) -> timedelta:
    """
    Calculate the total time from a list of timedelta objects.
    
    Args:
        timedelta_list (List[timedelta]): List of timedelta objects
        
    Returns:
        timedelta: Total time calculated from the list of timedeltas
    """
    if not timedelta_list:
        return timedelta()
    
    return sum(timedelta_list, timedelta())

def get_largest_times(timedelta_list: List[timedelta], n: int = 5) -> List[timedelta]:
    """
    Get the n largest timedeltas from a list.
    
    Args:
        timedelta_list (List[timedelta]): List of timedelta objects
        n (int): Number of largest timedeltas to return (default: 5)
        
    Returns:
        List[timedelta]: List containing the n largest timedeltas
    """
    if not timedelta_list:
        return []
    
    # Sort the list in descending order and take the first n elements
    return sorted(timedelta_list, reverse=True)[:n] 