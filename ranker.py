# Dummy logic: Replace with OpenCV/YOLO logic later

def calculate_score(video_path: str) -> int:
    # TODO: Replace with actual OpenCV logic
    # For now, return a random number or fixed test score
    import random
    return random.randint(0, 50)

def get_rank(score: int) -> str:
    if score >= 46:
        return "ht1"  # Highest rank
    elif score >= 41:
        return "lt1"
    elif score >= 36:
        return "ht2"
    elif score >= 31:
        return "lt2"
    elif score >= 26:
        return "ht3"
    elif score >= 21:
        return "lt3"
    elif score >= 16:
        return "ht4"
    elif score >= 11:
        return "lt4"
    elif score >= 6:
        return "ht5"
    else:
        return "lt5"
