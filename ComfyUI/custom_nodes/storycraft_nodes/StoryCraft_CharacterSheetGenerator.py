
import json
import yaml  # You will need to install PyYAML: pip install PyYAML

# In a real implementation, you would import the Vertex AI SDK
# from vertexai.preview.vision_models import ImageGenerationModel

class StoryCraft_CharacterSheetGenerator:
    """
    A ComfyUI node to generate reference images ("Character Sheets") for all
    characters, settings, and props defined in the scenario blueprint.
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "SCENARIO_BLUEPRINT": ("STRING", {"multiline": True}),
                "gcs_bucket_uri": ("STRING", {"multiline": False, "default": "gs://your-gcs-bucket/storycraft_output"}),
                "model_name": ("STRING", {"multiline": False, "default": "imagen-4.0-generate-001"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("SCENARIO_WITH_IMAGES",)
    FUNCTION = "generate_character_sheets"
    CATEGORY = "StoryCraft"

    def generate_single_image(self, item_name: str, item_description: str, style: str, shot_type: str, aspect_ratio: str, gcs_bucket_uri: str, model_name: str):
        """
        This function simulates calling an image generation API for a single item.
        In a real implementation, this would contain the API call logic.
        """
        # This prompt structure is based on the original TypeScript application
        prompt_data = {
            'style': style,
            'shot_type': shot_type,
            'description': item_description,
        }
        # The original app used YAML format for the prompt
        prompt_string = yaml.dump(prompt_data, indent=2, default_flow_style=False)

        print(f"--- Simulating Image Generation for: {item_name} ---")
        print(prompt_string)

        # --- Mock Response ---
        # In a real implementation, you would call the Imagen/Vertex AI API here.
        #
        # --- Start of Real Implementation Block ---
        # try:
        #     model = ImageGenerationModel.from_pretrained(model_name)
        #     response = model.generate_images(
        #         prompt=prompt_string,
        #         number_of_images=1,
        #         aspect_ratio=aspect_ratio,
        #         # The API might require a GCS path to save the output directly
        #         # This parameter may vary based on the SDK version.
        #     )
        #     # Assuming the response contains a GCS URI for the generated image
        #     image_gcs_uri = response.images[0]._image_uri
        # except Exception as e:
        #     print(f"An error occurred during image generation for {item_name}: {e}")
        #     image_gcs_uri = f"{gcs_bucket_uri}/error.png"
        # --- End of Real Implementation Block ---

        # Using a mock response for now.
        sanitized_name = item_name.lower().replace(" ", "-")
        image_gcs_uri = f"{gcs_bucket_uri}/mock-images/{sanitized_name}.png"
        print(f"--- Mock GCS URI: {image_gcs_uri} ---")

        return image_gcs_uri

    def generate_character_sheets(self, SCENARIO_BLUEPRINT: str, gcs_bucket_uri: str, model_name: str):
        """
        Orchestrates the generation of all character sheets.
        """
        print("Generating character sheets...")
        try:
            scenario_data = json.loads(SCENARIO_BLUEPRINT)
        except json.JSONDecodeError:
            print("Error: Invalid JSON in SCENARIO_BLUEPRINT input.")
            return (json.dumps({"error": "Invalid JSON input"}),)

        style = scenario_data.get("style", "cinematic")

        # Process Characters
        if "characters" in scenario_data and isinstance(scenario_data["characters"], list):
            for character in scenario_data["characters"]:
                character["imageGcsUri"] = self.generate_single_image(
                    item_name=character.get("name", "unknown-character"),
                    item_description=character.get("description", ""),
                    style=style,
                    shot_type="Medium Shot",
                    aspect_ratio="1:1",
                    gcs_bucket_uri=gcs_bucket_uri,
                    model_name=model_name
                )

        # Process Settings
        if "settings" in scenario_data and isinstance(scenario_data["settings"], list):
            for setting in scenario_data["settings"]:
                setting["imageGcsUri"] = self.generate_single_image(
                    item_name=setting.get("name", "unknown-setting"),
                    item_description=setting.get("description", ""),
                    style=style,
                    shot_type="Wide Shot",
                    aspect_ratio="16:9", # Or use a value from scenario_data if available
                    gcs_bucket_uri=gcs_bucket_uri,
                    model_name=model_name
                )

        # Process Props
        if "props" in scenario_data and isinstance(scenario_data["props"], list):
            for prop in scenario_data["props"]:
                prop["imageGcsUri"] = self.generate_single_image(
                    item_name=prop.get("name", "unknown-prop"),
                    item_description=prop.get("description", ""),
                    style=style,
                    shot_type="Close Shot",
                    aspect_ratio="1:1",
                    gcs_bucket_uri=gcs_bucket_uri,
                    model_name=model_name
                )

        # Return the updated scenario data as a JSON string
        output_string = json.dumps(scenario_data, indent=4)
        return (output_string,)

# A dictionary that maps class names to object instances
NODE_CLASS_MAPPINGS = {
    "StoryCraft_CharacterSheetGenerator": StoryCraft_CharacterSheetGenerator
}

# A dictionary that maps class names to display names
NODE_DISPLAY_NAME_MAPPINGS = {
    "StoryCraft_CharacterSheetGenerator": "StoryCraft Character Sheet Generator"
}
