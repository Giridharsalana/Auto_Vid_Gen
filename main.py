import yt_dlp
import cv2

class Auto_Vid_Gen:
    def __init__(self, url):
        self.url = url
        self.output_path_1 = '1_video.mp4'
        self.output_path_2 = '2_video.mp4'
        self.video_stream = None
        self.audio_stream = None
    
    def download_video(self):
        try:
            # Set up options for yt-dlp to download the highest quality video and audio
            ydl_opts = {
                'format': "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",  # Download the best video and audio
                'outtmpl': self.output_path_1.split('.')[0],  # Use dynamic extension based on format
                'noplaylist': True,  # Do not download playlists
                'quiet': False,  # Show progress and information
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
                print(f"Download completed: {self.output_path_1}")
        
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def draw_face_bbox(self):
        print("Drawing face bounding boxes...")
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        cap = cv2.VideoCapture(self.output_path_1)  # Replace with your video file or webcam (0 for webcam)

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        output_video = cv2.VideoWriter(self.output_path_2, 
                                    cv2.VideoWriter_fourcc(*'XVID'), 
                                    fps, 
                                    (frame_width, frame_height))

        while True:
            # Read each frame from the video
            ret, frame = cap.read()
            
            if not ret:
                break

            # Convert the frame to grayscale (Haar Cascade works on grayscale images)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces in the grayscale image
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            
            # Draw bounding boxes around detected faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Blue color, 2px thickness
            
            # Write the frame with bounding boxes to the output video
            output_video.write(frame)
            
            # Press 'q' to exit the loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the video capture and writer objects, and close all windows
        cap.release()
        output_video.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    youtube_url = 'https://www.youtube.com/watch?v=UWkmWzCRz0s'  # The provided YouTube URL
    Auto_Vid_Gen = Auto_Vid_Gen(youtube_url)
    Auto_Vid_Gen.download_video()
    Auto_Vid_Gen.draw_face_bbox()
