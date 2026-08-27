Face Blurrer
Real-time face blurring application with GUI interface. Detects faces using OpenCV Haar Cascade and covers them with a colored rectangle.

### Features
    Real-time face detection and tracking

    Customizable fill color (RGB sliders)

    Multi-language support (Russian/English)

    Debug mode with FPS and face counter

    Pause/Resume with Space key

    Face tracking with smooth movement

    Adjustable window size

    Keyboard shortcuts support

### Controls
Key	Action
Space	Pause/Resume video
ESC	Exit program
D or F1	Toggle debug mode
R	Reset face tracking
###  How to Use

    Launch the program

    Select your preferred language (Russian/English)

    Wait for the camera to connect

    Use RGB sliders to change the overlay color

    The rectangle will automatically follow your face

    Press Space to pause or ESC to exit

### Frequently Asked Questions (FAQ)
    Face Blurrer - Frequently Asked Questions (FAQ)

### General Questions

### What is this program?
    Face Blurrer is a Windows application that detects faces in real-time through your webcam and covers them with a colored rectangle. Useful for streams, video calls, screen recording, and privacy.

### What is it used for?

### Hiding your face during screen recording

### Anonymity in streams

### Privacy in video calls

### Testing face recognition systems

### What are the system requirements?

### OS: Windows 10 / 11

### CPU: 1.5 GHz or higher

### RAM: 2 GB or more

### Camera: Any webcam (built-in or USB)

### Free space: ~100 MB

### Installation and Launch

### How to install the program?
    No installation required. Just extract the archive and run FaceBlurrer.exe.

### Why does the program not start?
    Possible reasons:

### Missing haarcascade_frontalface_default.xml file (should be next to .exe)

### Antivirus blocking the program (add to exceptions)

### No administrator rights (run as administrator)

### No webcam or it is busy with another app

### Why does antivirus flag the program?
    This is a false positive. The program does not contain viruses. It is detected because:

It is a single .exe file (packed by PyInstaller)

It accesses your webcam

It uses low-level system functions

### Solution: Add the program to antivirus exceptions.

### How to run the program?

Double-click FaceBlurrer.exe

Select language (Russian/English)

Wait for camera to connect

Use color sliders to change the overlay color

Press Space to pause/resume

Press ESC to exit

Controls

### What keyboard shortcuts are available?

Space - Pause/Resume video

ESC - Exit program

D or F1 - Toggle debug mode

R - Reset face tracking

### How to change the overlay color?
    Use the Red, Green, and Blue sliders in the control window. The preview shows the current color.

### How to pause the video?
  Press the Pause button or use the Space key.

### Camera Issues

### Why does the camera not work?
### Check:

### Is the camera connected?

### Is the camera being used by another app (Discord, Zoom, OBS)?

### Try changing the camera index in settings (0, 1, 2, etc.)

### Run the program as administrator

### Face Tracking

### Why does the square disappear when I turn my head?
    The program remembers the face position for about 2 seconds (60 frames). If you turn away and come back quickly, the square will       reappear.

### Why does the square disappear when I cover my face with my hand?
    The square stays for about 2 seconds after the face disappears. If you cover your face for longer, the tracking resets.

### Why does the square jump around?
    The program uses smoothing to make the square follow your face smoothly. If it jumps too much, try reducing movement speed.

### How to reset tracking?
    Press the Reset button or use the R key.

### Debug Mode

### What is debug mode?
    Debug mode shows additional information on the video screen and in the console.

### How to enable debug mode?
    Press F1 key.

### What information does debug mode show?

### Number of faces detected

### Current color (RGB values)

### Tracking timer

### No face counter

### Performance

### Why is the program slow?
Try:

### Closing other applications

### Reducing video resolution in settings

### Using a lower camera resolution

### Updating graphics drivers

### Why is there a delay in video?
  The program processes each frame, which may cause a slight delay. This is normal for real-time face detection.

### How to increase FPS?
  The camera runs at 30 FPS by default. If you need higher FPS, reduce the detection quality by changing scaleFactor and minNeighbors     parameters.

### Color Settings

### How to reset color to default?
    Set all sliders (Red, Green, Blue) to 0 for black color.

### Can I save my color settings?
    Currently, color settings are not saved. You need to set the color each time you start the program.

### What color formats are supported?
    The program uses RGB (Red, Green, Blue) color model with values from 0 to 255 for each channel.

### Troubleshooting

### The program crashes on startup

### Make sure haarcascade_frontalface_default.xml is in the same folder

### Run as administrator

### Disable antivirus temporarily

### Check Windows Event Viewer for errors

### Face is not detected

### Make sure your face is clearly visible

### Adjust lighting conditions

### Move closer to the camera

### Check if the camera is working in other apps

### The square is in the wrong place
    Press the Reset button or use the R key to restart tracking.

### Audio is not working
    The program does not capture audio. It only processes video.

### Sending to Friend

### How to send the program to a friend?

    Copy FaceBlurrer.exe and haarcascade_frontalface_default.xml to one folder
  
    Compress the folder (ZIP or RAR)

    Send via Telegram, Discord, Google Drive, or any file sharing service

    Friend extracts and runs FaceBlurrer.exe

### Does my friend need to install anything?
    No. The .exe file works on any Windows 10/11 computer without additional installation.

    Updates and Support

### How to update the program?
    Download the new version and replace the old .exe file.

### Technical Details

### What is the program written in?
    Python with OpenCV, Tkinter, and PyInstaller.

### Is the source code available?
    The source code can be provided upon request.

### Does the program collect my data?
    No. The program does not collect, store, or transmit any data. All processing is done locally on your computer.

### Is an internet connection required?
    No. The program works completely offline.

### Additional Questions

### Can I use this on Mac or Linux?
    Currently, the program is only compiled for Windows. The source code can be run on Mac/Linux with Python installed.

### Can I blur multiple faces?
    Yes. The program detects and blurs all faces in the frame.

### Can I change the shape of the blur?
    Currently, only rectangular blur is supported. Other shapes may be added in future updates.

### Can I use this in OBS?
    Yes. You can use window capture or game capture to add the Face Blurrer window to OBS.

### Can I use this in Discord?
    You cannot blur video directly in Discord. However, you can share your screen showing the Face Blurrer window, or use OBS Virtual Camera with the program.

###  Why is the square outline white?
    The white border helps you see where the face is detected. It is always shown regardless of   the fill color.

### How to exit the program?
    Press the Exit button, close the window, or press the ESC key.

### If your issue is not listed here, please contact the developer for assistance.

### License
    This project is for personal use only. Redistribution and commercial use are prohibited     without permission.

### Disclaimer
    This software is provided "as is" without warranty of any kind. Use at your own risk. The     developer is not responsible for any misuse of this software.

### Author
    air240

### Thank you for downloading the program!
    If you find this project useful, please give it a star on GitHub. Your support is greatly     appreciated!

