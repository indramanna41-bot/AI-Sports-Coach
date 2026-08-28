import json

from backend.database.database import SessionLocal
from backend.database.models import PerformanceRecord


def save_performance_result(
    user_id,
    sport,
    analysis_result
):
    """
    Save one sports analysis result into the database.
    """

    db = SessionLocal()

    try:
        record = PerformanceRecord(
            user_id=str(user_id),
            sport=sport,
            overall_score=analysis_result[
                "overall_score"
            ],
            components_json=json.dumps(
                analysis_result.get(
                    "components",
                    {}
                )
            ),
            strengths_json=json.dumps(
                analysis_result.get(
                    "strengths",
                    []
                )
            ),
            weaknesses_json=json.dumps(
                analysis_result.get(
                    "weaknesses",
                    []
                )
            ),
            recommendations_json=json.dumps(
                analysis_result.get(
                    "recommendations",
                    []
                )
            )
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return {
            "saved": True,
            "record_id": record.id
        }

    finally:
        db.close()


def get_user_history(
    user_id,
    sport=None
):
    """
    Get previous analysis results for one user.
    """

    db = SessionLocal()

    try:
        query = db.query(
            PerformanceRecord
        ).filter(
            PerformanceRecord.user_id
            == str(user_id)
        )

        if sport is not None:
            query = query.filter(
                PerformanceRecord.sport
                == sport
            )

        records = query.order_by(
            PerformanceRecord.created_at.asc()
        ).all()

        history = []

        for record in records:
            history.append({
                "id": record.id,
                "user_id": record.user_id,
                "sport": record.sport,
                "overall_score": record.overall_score,
                "components": json.loads(
                    record.components_json
                ),
                "strengths": json.loads(
                    record.strengths_json
                ),
                "weaknesses": json.loads(
                    record.weaknesses_json
                ),
                "recommendations": json.loads(
                    record.recommendations_json
                ),
                "created_at": (
                    record.created_at.isoformat()
                    if record.created_at
                    else None
                )
            })

        return history

    finally:
        db.close()


def get_progress_data(
    user_id,
    sport
):
    """
    Return graph-ready performance history
    for one user and one sport.
    """

    history = get_user_history(
        user_id=user_id,
        sport=sport
    )

    progress = []

    for record in history:
        progress.append({
            "record_id": record["id"],
            "date": record["created_at"],
            "overall_score": record[
                "overall_score"
            ],
            "components": record[
                "components"
            ]
        })

    if len(progress) >= 2:
        first_score = progress[0][
            "overall_score"
        ]

        latest_score = progress[-1][
            "overall_score"
        ]

        overall_improvement = round(
            latest_score - first_score,
            2
        )

    else:
        overall_improvement = 0.0

    latest_components = {}

    if progress:
        latest_components = progress[-1][
            "components"
        ]

    return {
        "user_id": str(user_id),
        "sport": sport,
        "total_analyses": len(progress),
        "overall_improvement": (
            overall_improvement
        ),
        "latest_components": (
            latest_components
        ),
        "progress": progress
    }