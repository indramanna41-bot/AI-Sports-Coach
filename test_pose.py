from backend.vision.pose_analyzer import PoseAnalyzer


video_path = "uploads/FREESTYLE 😱🔥 FOOTBALL SKILLS ⚽️⭐️ BEACH FOOTBALL valerikostovofficial - v7skills (1080p, h264, youtube).mp4"


analyzer = PoseAnalyzer()

result = analyzer.analyze_video(video_path)


print("\nPOSE ANALYSIS RESULT")
print("====================")

print("Total frames:", result["total_frames"])
print("Pose detected frames:", result["pose_detected_frames"])
print("Detection rate:", result["detection_rate"])


print("\nFIRST DETECTED FRAME")
print("====================")

if result["landmarks"]:

    first_frame = result["landmarks"][0]

    print("Frame:", first_frame["frame"])
    print("Timestamp:", first_frame["timestamp_ms"], "ms")

    print("\nLandmarks:")

    for name, data in first_frame["landmarks"].items():

        print(
            name,
            "x =", data["x"],
            "y =", data["y"],
            "z =", data["z"],
            "visibility =", data["visibility"]
        )

else:
    print("No pose landmarks detected.")


analyzer.close()