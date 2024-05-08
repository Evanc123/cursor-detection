import cv2
import numpy as np
from multiprocessing import Pool
import subprocess
import random
import string
import os


def process_chunk(args):
    (
        start_frame,
        end_frame,
        video_path,
        template_paths,
        fps,
        frame_width,
        frame_height,
        fourcc,
        output_chunk_path,
    ) = args
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    out = cv2.VideoWriter(output_chunk_path, fourcc, fps, (frame_width, frame_height))

    frame_number = 0
    while cap.get(cv2.CAP_PROP_POS_FRAMES) <= end_frame:
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
                _, max_val, _, max_loc = cv2.minMaxLoc(res)

                if max_val > 0.8:
                    best_matches.append(
                        (max_val, max_loc, int(w * scale), int(h * scale))
                    )

        best_matches.sort(reverse=True, key=lambda x: x[0])

        for match in best_matches[:1]:
            _, best_loc, best_w, best_h = match
            top_left = best_loc
            bottom_right = (top_left[0] + best_w, top_left[1] + best_h)
            cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)

        out.write(img)
        frame_number += 1
        print(
            f"Processed {frame_number} / {end_frame - start_frame} frames from {start_frame} to {end_frame}, with match count: {len(best_matches)}"
        )

    cap.release()
    out.release()


def detect_apple_mouse_in_video(video_path, template_paths, output_video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    num_chunks = 16
    frames_per_chunk = total_frames // num_chunks
    chunk_paths = [f"{output_video_path}_chunk_{i}.mp4" for i in range(num_chunks)]

    pool = Pool(processes=num_chunks)
    pool.map(
        process_chunk,
        [
            (
                i * frames_per_chunk,
                min((i + 1) * frames_per_chunk - 1, total_frames - 1),
                video_path,
                template_paths,
                fps,
                frame_width,
                frame_height,
                fourcc,
                chunk_paths[i],
            )
            for i in range(num_chunks)
        ],
    )

    pool.close()
    pool.join()

    # Combine video chunks using FFmpeg
    with open("file_list.txt", "w") as f:
        for path in chunk_paths:
            f.write(f"file '{path}'\n")

    subprocess.run(
        [
            "ffmpeg",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            "file_list.txt",
            "-c",
            "copy",
            output_video_path,
        ]
    )

    # Optionally, remove chunk files and the file list
    for path in chunk_paths:
        subprocess.run(["rm", path])
    subprocess.run(["rm", "file_list.txt"])

    cap.release()
    print("Video processing complete and saved to", output_video_path)


# Example usage
template_paths = [
    "screenshots/templates/apple_hand_template.png",
    "screenshots/templates/apple_mouse_default_pointer_template.png",
    "screenshots/templates/apple_text_selection_template.png",
]


video_path = "videos/tester.mov"

# generate short 5 random id and then write the folder name


if __name__ == "__main__":
    output_folder_name = "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(5)
    )
    # write the path
    os.makedirs(f"videos/{output_folder_name}", exist_ok=True)
    output_video_path = f"videos/{output_folder_name}/processed_video.mp4"
    print(output_video_path)

    detect_apple_mouse_in_video(video_path, template_paths, output_video_path)
