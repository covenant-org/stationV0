import viser
import numpy as np
import cv2
import time

def main():
    server = viser.ViserServer()

    # Create static objects
    server.scene.add_box(
        "/box1",
        color=(0.2, 0.8, 0.2),
        dimensions=(1.0, 1.0, 1.0),
        position=(0.0, 0.0, 0.5),
    )

    # Create moving objects (will be updated in loop)
    moving_sphere1 = server.scene.add_icosphere(
        "/moving_sphere1",
        color=(0.8, 0.2, 0.2),
        radius=0.3,
        position=(2.0, 0.0, 0.3),
    )

    moving_sphere2 = server.scene.add_icosphere(
        "/moving_sphere2",
        color=(0.2, 0.2, 0.8),
        radius=0.3,
        position=(-2.0, 0.0, 0.3),
    )

    # Rotating box
    rotating_box = server.scene.add_box(
        "/rotating_box",
        color=(0.8, 0.8, 0.2),
        dimensions=(0.5, 0.5, 2.0),
        position=(0.0, 2.0, 1.0),
    )

    # Bouncing sphere
    bouncing_sphere = server.scene.add_icosphere(
        "/bouncing_sphere",
        color=(0.8, 0.2, 0.8),
        radius=0.25,
        position=(0.0, -2.0, 0.25),
    )

    # Add a coordinate frame
    server.scene.add_frame(
        "/world",
        wxyz=(1.0, 0.0, 0.0, 0.0),
        position=(0.0, 0.0, 0.0),
        axes_length=1.0,
        axes_radius=0.02,
    )

    # Virtual camera settings
    camera_position = np.array([5.0, 5.0, 4.0])
    camera_look_at = np.array([0.0, 0.0, 0.5])
    camera_fov = 60.0  # degrees

    # Add a camera frustum to visualize the virtual camera
    frustum = server.scene.add_camera_frustum(
        "/virtual_camera",
        fov=np.deg2rad(camera_fov),
        aspect=16/9,
        scale=0.5,
        color=(1.0, 1.0, 0.0),  # Yellow
        position=camera_position,
    )

    # GUI controls
    with server.gui.add_folder("Virtual Camera"):
        streaming = server.gui.add_checkbox("Stream Camera", initial_value=False)
        fps_slider = server.gui.add_slider("Target FPS", min=1.0, max=60.0, step=1.0, initial_value=30.0)

        cam_x = server.gui.add_slider("Camera X", min=-10.0, max=10.0, step=0.1, initial_value=camera_position[0])
        cam_y = server.gui.add_slider("Camera Y", min=-10.0, max=10.0, step=0.1, initial_value=camera_position[1])
        cam_z = server.gui.add_slider("Camera Z", min=0.1, max=10.0, step=0.1, initial_value=camera_position[2])

        look_x = server.gui.add_slider("Look At X", min=-5.0, max=5.0, step=0.1, initial_value=camera_look_at[0])
        look_y = server.gui.add_slider("Look At Y", min=-5.0, max=5.0, step=0.1, initial_value=camera_look_at[1])
        look_z = server.gui.add_slider("Look At Z", min=-5.0, max=5.0, step=0.1, initial_value=camera_look_at[2])

    with server.gui.add_folder("Animation"):
        animation_speed = server.gui.add_slider("Speed", min=0.1, max=3.0, step=0.1, initial_value=1.0)
        pause_animation = server.gui.add_checkbox("Pause", initial_value=False)

    with server.gui.add_folder("Status"):
        status_text = server.gui.add_text("Status", initial_value="Waiting for connection...", disabled=True)
        fps_text = server.gui.add_text("Render FPS", initial_value="0.0", disabled=True)
        sim_fps_text = server.gui.add_text("Simulation FPS", initial_value="0.0", disabled=True)

    print("🎬 Virtual Camera with Animated Scene!")
    print(f"🌐 Open your browser to: http://localhost:8080")
    print("📺 Enable 'Stream Camera' to open the camera window")
    print("🎯 Moving objects:")
    print("   - Red & Blue spheres orbiting in circles")
    print("   - Yellow box rotating")
    print("   - Pink sphere bouncing up and down")
    print("⚠️  Press 'Q' in the camera window to close it")
    print("⚠️  Press Ctrl+C here to stop the server")

    # Wait for client connection
    print("⏳ Waiting for client connection...")
    while len(server.get_clients()) == 0:
        time.sleep(0.1)

    client = server.get_clients()[0]
    print(f"✅ Client connected!")
    status_text.value = "Connected. Enable streaming to start."

    window_created = False
    frame_count = 0
    start_time = time.time()
    sim_frame_count = 0
    sim_start_time = time.time()

    # Animation time
    anim_time = 0.0

    try:
        while True:
            loop_start = time.time()

            # Update animation (if not paused)
            if not pause_animation.value:
                anim_time += 0.016 * animation_speed.value  # ~60fps baseline

                # Orbiting spheres
                radius = 2.0
                moving_sphere1.position = (
                    radius * np.cos(anim_time),
                    radius * np.sin(anim_time),
                    0.3 + 0.2 * np.sin(anim_time * 2)
                )

                moving_sphere2.position = (
                    radius * np.cos(anim_time + np.pi),
                    radius * np.sin(anim_time + np.pi),
                    0.3 + 0.2 * np.sin(anim_time * 2 + np.pi)
                )

                # Rotating box
                angle = anim_time
                rotating_box.wxyz = (
                    np.cos(angle / 2),
                    0,
                    0,
                    np.sin(angle / 2)
                )

                # Bouncing sphere
                bounce_height = abs(np.sin(anim_time * 2)) * 2.0 + 0.25
                bouncing_sphere.position = (0.0, -2.0, bounce_height)

            # Update simulation FPS
            sim_frame_count += 1
            sim_elapsed = time.time() - sim_start_time
            if sim_elapsed > 0.5:
                sim_fps = sim_frame_count / sim_elapsed
                sim_fps_text.value = f"{sim_fps:.1f}"
                sim_frame_count = 0
                sim_start_time = time.time()

            # Update camera frustum position from sliders
            new_cam_pos = np.array([cam_x.value, cam_y.value, cam_z.value])
            new_look_at = np.array([look_x.value, look_y.value, look_z.value])

            # Update frustum position
            frustum.position = new_cam_pos

            # If streaming, capture and display frame
            if streaming.value:
                # Create window if not already created
                if not window_created:
                    cv2.namedWindow("Virtual Camera View", cv2.WINDOW_NORMAL)
                    cv2.resizeWindow("Virtual Camera View", 800, 600)
                    window_created = True
                    status_text.value = "Streaming to window..."
                    frame_count = 0
                    start_time = time.time()
                    print("📺 Camera window opened!")

                # Set the client's camera to the virtual camera position
                client.camera.position = new_cam_pos
                client.camera.look_at = new_look_at

                # Small delay for camera update
                time.sleep(0.03)

                # Capture the render from this viewpoint
                render = client.get_render(height=600, width=800)

                # Convert RGB to BGR for OpenCV display
                frame_bgr = cv2.cvtColor(render, cv2.COLOR_RGB2BGR)

                # Calculate FPS
                frame_count += 1
                elapsed = time.time() - start_time
                if elapsed > 0:
                    fps = frame_count / elapsed
                    fps_text.value = f"{fps:.1f}"

                    # Add overlays to the frame
                    cv2.putText(frame_bgr, f"Render FPS: {fps:.1f}", (10, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    cv2.putText(frame_bgr, f"Time: {anim_time:.2f}s", (10, 60),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

                # Display the frame
                cv2.imshow("Virtual Camera View", frame_bgr)

                # Check for 'q' key press to close window
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == ord('Q'):
                    streaming.value = False
                    cv2.destroyAllWindows()
                    window_created = False
                    status_text.value = "Streaming stopped (user closed window)"
                    print("📺 Camera window closed by user")
                    continue

                # Target FPS delay
                target_delay = 1.0 / fps_slider.value
                elapsed_loop = time.time() - loop_start
                time.sleep(max(0.001, target_delay - elapsed_loop))
            else:
                # Not streaming - close window if open
                if window_created:
                    cv2.destroyAllWindows()
                    window_created = False
                    status_text.value = "Streaming stopped"
                    print("📺 Camera window closed")

                time.sleep(0.016)  # ~60fps for animation

    except KeyboardInterrupt:
        print("\n🛑 Stopping virtual camera demo...")
        if window_created:
            cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
