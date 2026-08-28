from backend.services.progress_service import (
    save_performance_result,
    get_user_history
)


sample_result = {
    "overall_score": 71.2,

    "components": {
        "movement": 75.1,
        "lower_body_technique": 81.4,
        "balance": 73.5,
        "ball_interaction": 74.9,
        "consistency": 60.7,
        "running_ability": 76.5,
        "ball_control": 57.1,
        "kicking_posture": 70.3
    },

    "strengths": [
        "Strong movement",
        "Good lower body technique"
    ],

    "weaknesses": [
        "Ball control needs improvement"
    ],

    "recommendations": [
        "Practice close-control dribbling drills."
    ]
}


save_result = save_performance_result(
    user_id="test_user_1",
    sport="football",
    analysis_result=sample_result
)


print()
print("SAVE RESULT")
print("===========")

print(save_result)


history = get_user_history(
    user_id="test_user_1",
    sport="football"
)


print()
print("USER HISTORY")
print("============")

for record in history:
    print(record)