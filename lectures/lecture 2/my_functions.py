def mean(data):
    """Computes the mean of all elements in `data`

    Args:
        data: List of numbers

    Returns: the mean over all numbers in `data`

    """
    mean_data = sum(data) / len(data)
    return mean_data
