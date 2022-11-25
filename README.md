# Screen Recorder App for MacOS

## Modules / Files

The body of work happens in ScreenRecorder and CaptureEngine.

- ScreenRecorder contains methods for checking `isRunning`
- When the app starts it will start recording automatically
- Recordings are stored in the ~/Documents directory.

## Known Bugs

[] If the screen goes into energy saving or is closed during a recording then `AVWriter` will bug out. 
[] The time needs to reset when the user finishes recording

## Nice to Haves

[] A split view on the left would be useful for config and viewing the files recorded.

