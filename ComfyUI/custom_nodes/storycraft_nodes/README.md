# StoryCraft Custom Nodes for ComfyUI

## Overview

StoryCraft is a suite of custom nodes for ComfyUI that allows you to generate a complete video from a simple text-based pitch. The nodes leverage generative AI models to create a story, generate character sheets, build a storyboard, and then generate the video and audio for each scene before stitching it all together into a final movie.

## Nodes

This project includes the following nodes:

*   `StoryCraft_ScenarioGenerator.py`: Generates a story blueprint from a pitch, including characters, settings, and music mood.
*   `StoryCraft_CharacterSheetGenerator.py`: Creates reference images for all characters, settings, and props.
*   `StoryCraft_StoryboardGenerator.py`: Generates a scene-by-scene storyboard with detailed prompts for image and video generation.
*   `StoryCraft_SceneSelector.py`: A utility node to select and process a single scene from the storyboard.
*   `StoryCraft_SceneVideoGenerator.py`: Generates a video clip for a single scene.
*   `StoryCraft_AudioGenerator.py`: Generates the voiceover and background music for a scene.
*   `StoryCraft_VideoStitcher.py`: Assembles the final video by stitching together all the generated video and audio assets.
*   `StoryCraft_Combined.py`: An all-in-one node that encapsulates the entire video generation pipeline, providing a simplified user experience.

### `StoryCraft_Combined` Node

The `StoryCraft_Combined` node is the recommended entry point for most users. It combines the functionality of all the other nodes into a single, powerful interface.

**Inputs:**

*   `pitch`: A short, one-sentence idea for the story.
*   `num_scenes`: The number of scenes to generate.
*   `style`: The visual style of the video (e.g., "Cinematic, high-contrast, realistic").
*   `language_name` and `language_code`: The language for the generated content.
*   `gcs_bucket_uri`: The Google Cloud Storage bucket where the generated assets will be stored.
*   `tts_model_voice`: The voice to be used for the text-to-speech generation.
*   `generation_model`, `image_model`, `video_model`, `lyria_model`: The specific generative models to be used for each step of the pipeline.

**Output:**

*   `FINAL_VIDEO_URI`: The GCS URI of the final, stitched video.

## Workflow

The StoryCraft pipeline follows these steps:

1.  **Scenario Generation:** A story blueprint is created from a `pitch`.
2.  **Character Sheet Generation:** Reference images are created for all characters and assets.
3.  **Storyboard Generation:** A detailed, scene-by-scene storyboard is generated.
4.  **Scene-by-Scene Generation:** For each scene, a video clip and audio (voiceover and music) are generated.
5.  **Video Stitching:** All the generated video and audio assets are combined into a final video.

This entire workflow is encapsulated within the `StoryCraft_Combined` node.

## Prompts

The prompts sent to the generative models are managed in the `storycraft_prompts.py` file. This separation of concerns makes it easy to edit and refine the prompts without modifying the main application logic.

## Installation and Dependencies

1.  Place the `storycraft_nodes` directory inside your `ComfyUI/custom_nodes/` directory.
2.  Install the required Python dependencies:

    ```bash
    pip install PyYAML
    ```

3.  Ensure you have configured your environment with the necessary API keys for the generative models.

## Usage

1.  In ComfyUI, add the `StoryCraft_Combined` node to your graph.
2.  Fill in the required inputs, such as your `pitch` and `gcs_bucket_uri`.
3.  Queue the prompt to run the entire video generation pipeline.
