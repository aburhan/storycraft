
import json

# You will need to install the Google AI Python SDK:
# pip install google-generativeai
#
# And configure your API key, typically by setting the GOOGLE_API_KEY environment variable.
#
# import google.generativeai as genai
# genai.configure(api_key="YOUR_API_KEY")


class StoryCraft_ScenarioGenerator:
    """
    A ComfyUI node to generate a story scenario blueprint from a pitch.
    It uses a generative model to create the story, character descriptions,
    setting descriptions, and music mood.
    """

    # Define the input types for the node
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "pitch": ("STRING", {"multiline": True, "default": "A lone astronaut discovers a mysterious, glowing plant on an otherwise barren moon."}),
                "num_scenes": ("INT", {"default": 5, "min": 1, "max": 20}),
                "style": ("STRING", {"multiline": False, "default": "Cinematic, high-contrast, realistic"}),
                "language_name": ("STRING", {"multiline": False, "default": "English"}),
                "language_code": ("STRING", {"multiline": False, "default": "en-US"}),
                "model_name": ("STRING", {"multiline": False, "default": "gemini-1.5-flash"}),
            }
        }

    # Define the return types of the node
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("SCENARIO_BLUEPRINT",)

    # The main function of the node
    FUNCTION = "generate_scenario"

    # The category for the node in the ComfyUI menu
    CATEGORY = "StoryCraft"

    def get_scenario_prompt(self, pitch: str, num_scenes: int, style: str, language_name: str, language_code: str) -> str:
        """
        Constructs the prompt for the generative model based on the logic
        from the original app/prompts.ts file.
        """
        return f'''
You are tasked with generating a creative scenario for a short movie and creating prompts for storyboard illustrations. Follow these instructions carefully:
1. First, you will be given a story pitch. This story pitch will be the foundation for your scenario.

<pitch>
{pitch}
</pitch>

2. Generate a scenario in {language_name} for a movie based on the story pitch. Stick as close as possible to the pitch. Do not include children in your scenario.

3. What Music Genre will best fit this video, pick from:
- Alternative & Punk
- Ambient
- Children's
- Cinematic
- Classical
- Country & Folk
- Dance & Electronic
- Hip-Hop & Rap
- Holiday
- Jazz & Blues
- Pop
- R&B & Soul
- Reggae
- Rock

4. What is the mood of this video, pick from:
- Angry
- Bright
- Calm
- Dark
- Dramatic
- Funky
- Happy
- Inspirational
- Romantic
- Sad

5. Generate a short description of the music, in English only, that will be used in the video. No references to the story, no references to known artists or songs.

6. Format your output as follows:
- First, provide a detailed description of your scenario in {language_name}.
- Then from this scenario provide a short description of each character in the story inside the characters key.
- Then from this scenario provide a short description of each setting in the story inside the settings key.
- Then, optionally, and only for very important props (products for ads, recurring objects, vehicles), if any, 0 to 2 props max, a short description of each prop important for the story

Format the response as a JSON object.
Here's an example of how your output should be structured:
{{
 "scenario": "[Brief description of your creative scenario based on the given story pitch]",
 "genre": "[Music genre]",
 "mood": "[Mood]",
 "music": "[Short description of the music that will be used in the video, no references to the story, no references to known artists or songs]",
 "language": {{
   "name": "{language_name}",
   "code": "{language_code}"
 }},
 "characters": [
  {{
    "name": "[character 1 name]",
    "voice": "[character's voice description. One sentence.]",
    "description": [
      "character 1 description in {language_name}",
      "Be hyper-specific and affirmative and short, one sentence max. Include age, gender, ethnicity, specific facial features if any, hair style and color, facial hair or absence of it for male, skin details and exact clothing, including textures and accessories."
      ]
  }}
 ],
 "settings": [
  {{
    "name": "[setting 1 name]",
    "description": [
      "setting 1 description in {language_name}",
      "This description establishes the atmosphere, lighting, and key features that must remain consistent.",
      "Be Evocative and short, one sentence max: Describe the mood, the materials, the lighting, and even the smell or feeling of the air."
    ]
  }}
 ],
 "props": [
  {{
    "name": "[prop 1 name]",
    "description": [
      "prop 1 description in {language_name}",
      "This description establishes the atmosphere, lighting, and key features that must remain consistent.",
      "Be Evocative and short, one sentence max: Describe the mood, the materials, the lighting, and even the smell or feeling of the air."
    ]
  }}
 ]
}}

Remember, your goal is to create a compelling and visually interesting story that can be effectively illustrated through a storyboard. Be creative, consistent, and detailed in your scenario and prompts.
'''

    def generate_scenario(self, pitch: str, num_scenes: int, style: str, language_name: str, language_code: str, model_name: str):
        """
        This function calls the generative model to produce the scenario blueprint.
        """
        print("Generating scenario blueprint...")

        prompt = self.get_scenario_prompt(pitch, num_scenes, style, language_name, language_code)

        # --- Mock Response ---
        # In a real implementation, you would make an API call to a generative model here.
        # The following is a mock JSON response for demonstration purposes.
        #
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
        #     # Return a default error structure if the API call fails
        #     raw_json_text = json.dumps({
        #         "error": "Failed to generate content from model.",
        #         "details": str(e)
        #     })
        # --- End of Real Implementation Block ---

        # Using a mock response for now.
        print("Using mock data. Replace with a real API call in production.")
        mock_response_text = f'''
        {{
            "scenario": "On the desolate lunar surface, astronaut Eva Rostova discovers a single, bioluminescent plant pulsing with a soft, ethereal light. Taking a sample, she soon realizes the plant communicates through light patterns, revealing a history of a long-lost cosmic civilization.",
            "genre": "Cinematic",
            "mood": "Inspirational",
            "music": "A gentle, swelling orchestral piece with ethereal synth pads and a sense of wonder and discovery.",
            "language": {{
                "name": "{language_name}",
                "code": "{language_code}"
            }},
            "characters": [
                {{
                    "name": "Dr. Eva Rostova",
                    "voice": "A calm, measured, and thoughtful female voice with a slight Eastern European accent.",
                    "description": "A woman in her late 30s, of Russian descent, with sharp, intelligent eyes, and dark hair tied back in a practical bun. She wears a standard-issue, slightly worn, white and grey spacesuit with the 'Ares V' mission patch on the shoulder."
                }}
            ],
            "settings": [
                {{
                    "name": "Lunar Surface",
                    "description": "A vast, silent expanse of grey dust and craters under a black, star-dusted sky. The Earth hangs like a giant blue marble in the distance, providing a cold, secondary light source."
                }},
                {{
                    "name": "The Bioluminescent Plant",
                    "description": "A plant with crystalline, semi-translucent leaves that emit a soft, pulsing blue and green light. It grows in a small, protected crater, starkly contrasting with the lifeless surroundings."
                }}
            ],
            "props": []
        }}
        '''
        raw_json_text = mock_response_text

        # The model might return the JSON wrapped in markdown, so we clean it up.
        clean_json_text = raw_json_text.strip().replace("```json", "").replace("```", "").strip()

        # We return the cleaned JSON as a string for the next node.
        # The 'json.dumps' ensures it's a properly formatted JSON string.
        try:
            parsed_json = json.loads(clean_json_text)
            output_string = json.dumps(parsed_json, indent=4)
        except json.JSONDecodeError:
            print("Error: Failed to parse JSON from model response.")
            output_string = json.dumps({"error": "Invalid JSON response from model", "response": clean_json_text})

        return (output_string,)

# A dictionary that maps class names to object instances
NODE_CLASS_MAPPINGS = {
    "StoryCraft_ScenarioGenerator": StoryCraft_ScenarioGenerator
}

# A dictionary that maps class names to display names
NODE_DISPLAY_NAME_MAPPINGS = {
    "StoryCraft_ScenarioGenerator": "StoryCraft Scenario Generator"
}
