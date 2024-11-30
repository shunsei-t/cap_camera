import cv2
import imageio
import time


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 30)           # カメラFPSを60FPSに設定
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) # カメラ画像の横幅を1280に設定
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) # カメラ画像の縦幅を720に設定

    FPS = 30
    frames = []
    record_start = False
    tt = time.time()
    ret = False

    while True:
        now = time.time()
        dt = now - tt

        if dt > 1.0/FPS:
            ret, frame = cap.read()

            if record_start:
                print(f"{1.0/(now-tt):.3f} [Hz] RC ON")
            else:
                print(f"{1.0/(now-tt):.3f} [Hz] RC OFF")

            tt = now

            if record_start:
                frame_c = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(frame_c)

        if not ret:
            print("wait frame")
            continue

        cv2.imshow("cap", frame)
        k = cv2.waitKey(1)
        if k == ord("q"):
            break
        elif k == ord("r"):
            record_start = not record_start

    ffmpeg_output_params = {
        'codec': 'libx264',
        'fps': 30,
        'bitrate': '4000k',
        'macro_block_size': 1,
    }

    with imageio.get_writer("output.mp4", format='FFMPEG', mode='I', **ffmpeg_output_params) as writer:
        for idx, frame in enumerate(frames):
            writer.append_data(frame)