
import json

class StoryCraft_SceneSelector:
    """
    A utility node to select a specific scene from the full scenario blueprint
    and extract its corresponding prompts.
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "FULL_SCENARIO": ("STRING", {"multiline": True}),
                "scene_index": ("INT", {"default": 0, "min": 0, "max": 100}),
            }
        }

    # Pass through the main scenario, and output the specific prompts for the selected scene
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING",)
    RETURN_NAMES = ("FULL_SCENARIO_PASSTHROUGH", "IMAGE_PROMPT", "VIDEO_PROMPT", "VOICEOVER_TEXT",)
    FUNCTION = "select_scene"
    CATEGORY = "StoryCraft/Utils"

    def select_scene(self, FULL_SCENARIO: str, scene_index: int):
        """
        Parses the scenario, selects the scene by index, and returns its components.
        """
        print(f"Selecting scene at index: {scene_index}")
        try:
            scenario_data = json.loads(FULL_SCENARIO)
        except json.JSONDecodeError:
            print("Error: Invalid JSON in FULL_SCENARIO input.")
            # Return empty values on error
            return (FULL_SCENARIO, "{}", "{}", "",)

        scenes = scenario_data.get("scenes", [])

        if not scenes or not isinstance(scenes, list):
            print("Warning: 'scenes' array not found or is empty in the scenario.")
            return (FULL_SCENARIO, "{}", "{}", "",)

        # Bounds checking for the scene_index
        if scene_index >= len(scenes):
            print(f"Warning: scene_index {scene_index} is out of bounds. Clamping to last scene at index {len(scenes) - 1}.")
            scene_index = len(scenes) - 1
        
        selected_scene = scenes[scene_index]

        # Extract the required components. The prompts are objects, so we dump them back to JSON strings.
        image_prompt_obj = selected_scene.get("imagePrompt", {})
        video_prompt_obj = selected_scene.get("videoPrompt", {})
        voiceover_text = selected_scene.get("voiceover", "")

        # Convert the prompt objects to formatted JSON strings for output
        image_prompt_str = json.dumps(image_prompt_obj, indent=4)
        video_prompt_str = json.dumps(video_prompt_obj, indent=4)

        print(f"-- Selected Image Prompt: --\n{image_prompt_str}")
        print(f"-- Selected Video Prompt: --\n{video_prompt_str}")
        print(f"-- Selected Voiceover: --\n{voiceover_text}")

        # We pass the original FULL_SCENARIO through so it can be used by other nodes
        return (FULL_SCENARIO, image_prompt_str, video_prompt_str, voiceover_text)

# A dictionary that maps class names to object instances
NODE_CLASS_MAPPINGS = {
    "StoryCraft_SceneSelector": StoryCraft_SceneSelector
}

# A dictionary that maps class names to display names
NODE_DISPLAY_NAME_MAPPINGS = {
    "StoryCraft_SceneSelector": "StoryCraft Scene Selector"
}
