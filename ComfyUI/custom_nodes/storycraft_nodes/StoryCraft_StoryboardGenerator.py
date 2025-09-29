
import json

# You will need to install the Google AI Python SDK:
# pip install google-generativeai
#
# And configure your API key, typically by setting the GOOGLE_API_KEY environment variable.
#
# import google.generativeai as genai
# genai.configure(api_key="YOUR_API_KEY")

class StoryCraft_StoryboardGenerator:
    """
    A ComfyUI node to generate the detailed, scene-by-scene storyboard,
    including image and video prompts for each scene.
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "SCENARIO_WITH_IMAGES": ("STRING", {"multiline": True}),
                "num_scenes": ("INT", {"default": 5, "min": 1, "max": 20}),
                "model_name": ("STRING", {"multiline": False, "default": "gemini-1.5-flash"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("FULL_SCENARIO",)
    FUNCTION = "generate_storyboard"
    CATEGORY = "StoryCraft"

    def get_scenes_prompt(self, scenario_data: dict, num_scenes: int) -> str:
        """
        Constructs the prompt for the generative model based on the logic
        from the original app/prompts.ts:getScenesPrompt file.
        """
        scenario_text = scenario_data.get("scenario", "")
        language_name = scenario_data.get("language", {}).get("name", "English")
        style = scenario_data.get("style", "cinematic")
        duration_seconds = scenario_data.get("durationSeconds", 8)

        characters_str = "\n".join([f'''Name: {c.get("name", "")} 
Description: {c.get("description", "")} 
Voice Description: {c.get("voice", "")}''' for c in scenario_data.get("characters", [])])
        props_str = "\n".join([f'{p.get("name", "")}\n\n{p.get("description", "")}' for p in scenario_data.get("props", [])])
        settings_str = "\n".join([f'{s.get("name", "")}\n\n{s.get("description", "")}' for s in scenario_data.get("settings", [])])
        music_str = scenario_data.get("music", "")
        mood_str = scenario_data.get("mood", "")

        character_names = [c.get("name") for c in scenario_data.get("characters", [])]
        prop_names = [p.get("name") for p in scenario_data.get("props", [])]
        setting_names = [s.get("name") for s in scenario_data.get("settings", [])]

        return f'''
        You are tasked with generating creative scenes for a short movie and creating prompts for storyboard illustrations. Follow these instructions carefully:
1. First, you will be given a scenario in {language_name}. This scenario will be the foundation for your storyboard.

<scenario>
{scenario_text}
</scenario>

<characters>
{characters_str}
</characters>

<props>
{props_str}
</props>

<settings>
{settings_str}
</settings>

<music>
{music_str}
</music>

<mood>
{mood_str}
</mood>

2. Generate exactly {num_scenes}, creative scenes to create a storyboard illustrating the scenario. Follow these guidelines for the scenes:
 a. For each scene, provide a JSON object with the keys: "imagePrompt", "videoPrompt", "description", "voiceover", and "charactersPresent".

3. The `imagePrompt` should be a JSON object for AI image generation for the first frame of the video, in {language_name}, with the style "{style}".

4. The `videoPrompt` should be a JSON object in {language_name}, focusing on movement and sound within the scene.

5. Format your entire output as a single JSON object with one key, "scenes", which contains a list of the {num_scenes} scene objects you generated.

Here is the required schema for your JSON output:
{{
  "scenes": [
    {{
      "imagePrompt": {{ ... }},
      "videoPrompt": {{ ... }},
      "description": "[A scene description explaining what happens]",
      "voiceover": "[A short, narrator voiceover text. One full sentence.]",
      "charactersPresent": ["[An array list of names of characters visually present in the scene]"]
    }}
  ]
}}

Remember, your goal is to create a compelling and visually interesting story that can be effectively illustrated through a storyboard. Be creative, consistent, and detailed in your prompts.
Remember, the number of scenes should be exactly {num_scenes}.
'''

    def generate_storyboard(self, SCENARIO_WITH_IMAGES: str, num_scenes: int, model_name: str):
        print("Generating storyboard scenes...")
        try:
            scenario_data = json.loads(SCENARIO_WITH_IMAGES)
        except json.JSONDecodeError:
            print("Error: Invalid JSON in SCENARIO_WITH_IMAGES input.")
            return (json.dumps({"error": "Invalid JSON input"}),)

        prompt = self.get_scenes_prompt(scenario_data, num_scenes)

        # --- Mock Response ---
        # In a real implementation, you would make an API call to a generative model here.
        # --- Start of Real Implementation Block ---
        # try:
        #     model = genai.GenerativeModel(model_name)
        #     response = model.generate_content(
        #         prompt,
        #         generation_config={"response_mime_type": "application/json"}
        #     )
        #     raw_json_text = response.text
        # except Exception as e:
        #     print(f"An error occurred: {e}")
        #     raw_json_text = json.dumps({"scenes": []})
        # --- End of Real Implementation Block ---

        print("Using mock data. Replace with a real API call in production.")
        mock_response_text = '''
        {
            "scenes": [
                {
                    "imagePrompt": {
                        "Style": "Cinematic, high-contrast, realistic",
                        "Scene": "The first frame shows Dr. Eva Rostova inside her helmet, her eyes wide with awe, reflecting the glow of the alien plant.",
                        "Composition": {
                            "shot_type": "Extreme Close-up on Eva's face",
                            "lighting": "Soft blue light from the plant illuminating her face in the darkness of space",
                            "overall_mood": "Awe and wonder"
                        },
                        "Subject": [{"name": "Dr. Eva Rostova"}],
                        "Prop": [],
                        "Context": [{"name": "Lunar Surface"}]
                    }
                    ,
                    "videoPrompt": {
                        "Action": "Dr. Eva Rostova slowly reaches out a gloved hand towards the glowing plant. The plant pulses with light as her finger gets closer.",
                        "Camera_Motion": "Static, fixed on the interaction.",
                        "Ambiance_Audio": "The low hum of the suit's life support, the soft crackle of radio static.",
                        "Dialogue": []
                    },
                    "description": "Eva, mesmerized by the discovery, cautiously extends her hand to touch the mysterious plant.",
                    "voiceover": "In the unending silence of space, a single, impossible spark of life appeared.",
                    "charactersPresent": ["Dr. Eva Rostova"]
                }
            ]
        }
        '''
        raw_json_text = mock_response_text

        try:
            # The model response should be a JSON object like {"scenes": [...]} 
            scenes_data = json.loads(raw_json_text)
            if "scenes" in scenes_data and isinstance(scenes_data["scenes"], list):
                # Append the new scenes to the main scenario object
                scenario_data["scenes"] = scenes_data["scenes"]
            else:
                print("Warning: 'scenes' key not found or not a list in model response.")
                scenario_data["scenes"] = []
        except json.JSONDecodeError:
            print("Error: Failed to parse JSON from model response.")
            scenario_data["scenes"] = []

        # Return the full, updated scenario data as a JSON string
        output_string = json.dumps(scenario_data, indent=4)
        return (output_string,)

# A dictionary that maps class names to object instances
NODE_CLASS_MAPPINGS = {
    "StoryCraft_StoryboardGenerator": StoryCraft_StoryboardGenerator
}

# A dictionary that maps class names to display names
NODE_DISPLAY_NAME_MAPPINGS = {
    "StoryCraft_StoryboardGenerator": "StoryCraft Storyboard Generator"
}
