# Virtual Camera Simulation with Viser

A 3D simulation with a virtual camera that streams its view to an independent window. Built with [Viser](https://viser.studio/) for 3D visualization and OpenCV for camera window rendering.

## Features

- **3D Animated Scene**: Multiple animated objects including orbiting spheres, rotating boxes, and bouncing spheres
- **Virtual Camera**: Yellow camera frustum visualization showing the camera's position and field of view
- **Independent Camera Window**: Real-time rendering displayed in a separate OpenCV window
- **Interactive Controls**: Adjust camera position, look-at point, animation speed, and rendering FPS
- **Performance Monitoring**: Real-time FPS display for both simulation and camera rendering

## Demo

The simulation includes:
- 🔴 Red sphere orbiting in a circle
- 🔵 Blue sphere orbiting in opposite direction
- 🟡 Yellow box continuously rotating
- 🟣 Pink sphere bouncing up and down
- 🟢 Green static box for reference

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/covenant-org/stationV0.git
   cd stationV0
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the simulation:**
   ```bash
   python virtual_camera_animated.py
   ```

2. **Open your browser:**
   - Navigate to: `http://localhost:8080`
   - You'll see the 3D scene with animated objects

3. **Enable camera streaming:**
   - In the sidebar, find "Virtual Camera" controls
   - Check the "Stream Camera" checkbox
   - A separate OpenCV window will open showing the camera's view

4. **Adjust settings:**
   - **Camera Position** (X/Y/Z sliders): Move the virtual camera in 3D space
   - **Look At** (X/Y/Z sliders): Change where the camera points
   - **Target FPS**: Control rendering frame rate (1-60 FPS)
   - **Animation Speed**: Adjust how fast objects move (0.1-3.0x)
   - **Pause**: Freeze the animation

5. **Close camera window:**
   - Press 'Q' while the camera window is focused
   - Or uncheck "Stream Camera" in the browser

6. **Stop the server:**
   - Press `Ctrl+C` in the terminal

## Controls Overview

### Virtual Camera Panel
- ☑️ **Stream Camera**: Opens/closes the camera window
- **Target FPS**: Render frame rate control
- **Camera X/Y/Z**: Virtual camera position
- **Look At X/Y/Z**: Camera aim point

### Animation Panel
- **Speed**: Animation playback speed multiplier
- **Pause**: Freeze/resume animation

### Status Panel
- **Status**: Current operation status
- **Render FPS**: Camera rendering frame rate
- **Simulation FPS**: Scene update rate

## Architecture

```
3D Viewer (Browser)          Virtual Camera Window
┌──────────────────┐        ┌──────────────────┐
│  🎥 Camera        │        │  📺 Camera View  │
│     (Yellow       │  ────▶ │                  │
│      Frustum)     │        │  Live rendering  │
│  📦 Scene Objects │        │  from camera POV │
│  🎚️ Controls      │        │  (Independent)   │
└──────────────────┘        └──────────────────┘
```

The system works by:
1. Positioning a virtual camera in the 3D scene (visualized as a yellow frustum)
2. Setting the browser's viewport to match the virtual camera's position
3. Capturing rendered frames using Viser's `get_render()` method
4. Displaying frames in a separate OpenCV window

## Technical Details

- **3D Engine**: Viser (web-based 3D visualization)
- **Window Management**: OpenCV (cv2)
- **Math/Arrays**: NumPy
- **Update Rate**: ~60 FPS for scene animation
- **Render Rate**: Configurable (1-60 FPS)

## Requirements

- Python 3.11+
- viser >= 1.0.0
- opencv-python >= 4.0.0
- numpy >= 2.0.0

See `requirements.txt` for full dependency list.

## Use Cases

- Virtual camera testing for robotics
- Computer vision algorithm validation
- Scene rendering pipeline development
- Latency testing between simulation and rendering
- Educational demonstrations of 3D graphics concepts

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Built with Claude Code
