import cv2
import numpy as np


def detect_apple_mouse_in_video(video_path, template_paths, output_video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file")
        return

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print("Video properties:")
    print("Frame width:", frame_width)
    print("Frame height:", frame_height)
    print("FPS:", fps)
    print("Total frames:", total_frames)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # or 'XVID'
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        best_matches = []

        for template_path in template_paths:
            template = cv2.imread(template_path, 0)
            w, h = template.shape[::-1]

            for scale in np.linspace(0.1, 1.5, 50):
                resized_template = cv2.resize(
                    template,
                    (int(w * scale), int(h * scale)),
                    interpolation=cv2.INTER_AREA,
                )
                res = cv2.matchTemplate(
                    img_gray, resized_template, cv2.TM_CCOEFF_NORMED
                )
                min_val, max_val_temp, min_loc, max_loc_temp = cv2.minMaxLoc(res)

                if max_val_temp > 0.8:
                    best_matches.append(
                        (max_val_temp, max_loc_temp, int(w * scale), int(h * scale))
                    )

        best_matches.sort(reverse=True, key=lambda x: x[0])

        for match in best_matches[:1]:
            max_val, best_loc, best_w, best_h = match
            top_left = best_loc
            bottom_right = (top_left[0] + best_w, top_left[1] + best_h)
            cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
            print("Match found with value: ", max_val)

        out.write(img)

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("Video processing complete and saved to", output_video_path)


# Example usage
template_paths = [
    "screenshots/templates/apple_hand_template.png",
    "screenshots/templates/apple_mouse_default_pointer_template.png",
    "screenshots/templates/apple_text_selection_template.png",
]

video_path = "videos/tester.mov"
output_video_path = "videos/p.mp4"

detect_apple_mouse_in_video(video_path, template_paths, output_video_path)
