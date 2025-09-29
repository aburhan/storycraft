import json
import time
import yaml
from . import storycraft_prompts

class StoryCraft_Combined:
    """
    A single, combined ComfyUI node that encapsulates the entire StoryCraft pipeline,
    from scenario generation to final video stitching.
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "pitch": ("STRING", {"multiline": True, "default": "A lone astronaut discovers a mysterious, glowing plant on an otherwise barren moon."}),
                "num_scenes": ("INT", {"default": 1, "min": 1, "max": 20}),
                "style": ("STRING", {"multiline": False, "default": "Cinematic, high-contrast, realistic"}),
                "language_name": ("STRING", {"multiline": False, "default": "English"}),
                "language_code": ("STRING", {"multiline": False, "default": "en-US"}),
                "gcs_bucket_uri": ("STRING", {"multiline": False, "default": "gs://your-gcs-bucket/storycraft_output"}),
                "tts_model_voice": ("STRING", {"multiline": False, "default": "en-US-Studio-O"}),
                "generation_model": ("STRING", {"multiline": False, "default": "gemini-1.5-flash"}),
                "image_model": ("STRING", {"multiline": False, "default": "imagen-4.0-generate-001"}),
                "video_model": ("STRING", {"multiline": False, "default": "veo-3.0-generate-001"}),
                "lyria_model": ("STRING", {"multiline": False, "default": "lyria-002"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("FINAL_VIDEO_URI",)
    FUNCTION = "run_full_pipeline"
    CATEGORY = "StoryCraft"

    def run_full_pipeline(self, pitch, num_scenes, style, language_name, language_code, gcs_bucket_uri, tts_model_voice, generation_model, image_model, video_model, lyria_model):
        print("--- Starting Full StoryCraft Pipeline ---")
        try:
            # 1. Generate Scenario Blueprint
            scenario_blueprint_str = self._generate_scenario(pitch, num_scenes, style, language_name, language_code, generation_model)
            if not scenario_blueprint_str or 'error' in scenario_blueprint_str:
                raise ValueError("Failed to generate scenario blueprint.")

            # 2. Generate Character Sheets
            scenario_with_images_str = self._generate_character_sheets(scenario_blueprint_str, gcs_bucket_uri, image_model)
            if not scenario_with_images_str or 'error' in scenario_with_images_str:
                raise ValueError("Failed to generate character sheets.")

            # 3. Generate Storyboard
            full_scenario_str = self._generate_storyboard(scenario_with_images_str, num_scenes, style, generation_model)
            if not full_scenario_str or 'error' in full_scenario_str:
                raise ValueError("Failed to generate storyboard.")
            
            full_scenario = json.loads(full_scenario_str)

            # 4. Process Each Scene
            all_video_clips = []
            all_voiceovers = []
            music_uri = ""

            scenes = full_scenario.get("scenes", [])
            if not scenes:
                raise ValueError("No scenes were generated in the storyboard.")

            for i, scene in enumerate(scenes):
                print(f"--- Processing Scene {i+1} ---")
                
                _, image_prompt_str, video_prompt_str, voiceover_text = self._select_scene(full_scenario_str, i)

                video_clip_uri = self._generate_scene_video(full_scenario_str, image_prompt_str, video_prompt_str, gcs_bucket_uri, image_model, video_model)
                if not video_clip_uri or 'error' in video_clip_uri:
                    print(f"Warning: Failed to generate video for scene {i+1}. Skipping.")
                    continue
                all_video_clips.append(video_clip_uri)

                voiceover_uri, music_uri = self._generate_audio(full_scenario_str, voiceover_text, gcs_bucket_uri, tts_model_voice, lyria_model)
                if voiceover_uri and 'error' not in voiceover_uri:
                    all_voiceovers.append(voiceover_uri)

            if not all_video_clips:
                raise ValueError("Video generation failed for all scenes.")

            # 5. Stitch Final Video
            final_video_uri = self._stitch_video(all_video_clips, all_voiceovers, music_uri, gcs_bucket_uri)

            print(f"--- Full StoryCraft Pipeline Complete. Final Video URI: {final_video_uri} ---")
            return (final_video_uri,)

        except Exception as e:
            print(f"An error occurred during the pipeline: {e}")
            return (f"{gcs_bucket_uri}/error.mp4",)

    def _generate_scenario(self, pitch: str, num_scenes: int, style: str, language_name: str, language_code: str, model_name: str):
        print(f"Generating scenario blueprint with model: {model_name}...")
        prompt = storycraft_prompts.get_scenario_prompt(pitch, num_scenes, style, language_name, language_code)
        
        # This is a placeholder for a real API call
        # In a real implementation, the response from the model would be used directly.
        mock_response_text = f'''
        {{
            "scenario": "On the desolate lunar surface, astronaut Eva Rostova discovers a single, bioluminescent plant pulsing with a soft, ethereal light. Taking a sample, she soon realizes the plant communicates through light patterns, revealing a history of a long-lost cosmic civilization.",
            "genre": "Cinematic",
            "mood": "Inspirational",
            "music": "A gentle, swelling orchestral piece with ethereal synth pads and a sense of wonder and discovery.",
            "language": {{"name": "{language_name}", "code": "{language_code}"}},
            "style": "{style}",
            "characters": [ {{"name": "Dr. Eva Rostova", "voice": "A calm, measured, and thoughtful female voice with a slight Eastern European accent.", "description": "A woman in her late 30s, of Russian descent, with sharp, intelligent eyes, and dark hair tied back in a practical bun. She wears a standard-issue, slightly worn, white and grey spacesuit with the 'Ares V' mission patch on the shoulder."}} ],
            "settings": [ {{"name": "Lunar Surface", "description": "A vast, silent expanse of grey dust and craters under a black, star-dusted sky. The Earth hangs like a giant blue marble in the distance, providing a cold, secondary light source."}}, {{"name": "The Bioluminescent Plant", "description": "A plant with crystalline, semi-translucent leaves that emit a soft, pulsing blue and green light. It grows in a small, protected crater, starkly contrasting with the lifeless surroundings."}} ],
            "props": []
        }}
        '''
        clean_json_text = mock_response_text.strip().replace("```json", "").replace("```", "").strip()
        return json.dumps(json.loads(clean_json_text), indent=4)

    def _generate_character_sheets(self, SCENARIO_BLUEPRINT: str, gcs_bucket_uri: str, model_name: str):
        print(f"Generating character sheets with model: {model_name}...")
        try:
            scenario_data = json.loads(SCENARIO_BLUEPRINT)
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON input"})

        style = scenario_data.get("style", "cinematic")

        for item_type in ["characters", "settings", "props"]:
            if item_type in scenario_data and isinstance(scenario_data[item_type], list):
                for item in scenario_data[item_type]:
                    shot_type = "Medium Shot" if item_type == "characters" else "Wide Shot" if item_type == "settings" else "Close Shot"
                    aspect_ratio = "1:1" if item_type != "settings" else "16:9"
                    item["imageGcsUri"] = self._generate_single_image(
                        item_name=item.get("name", f"unknown-{item_type}"),
                        item_description=item.get("description", ""),
                        style=style,
                        shot_type=shot_type,
                        aspect_ratio=aspect_ratio,
                        gcs_bucket_uri=gcs_bucket_uri,
                        model_name=model_name
                    )
        return json.dumps(scenario_data, indent=4)

    def _generate_single_image(self, item_name: str, item_description: str, style: str, shot_type: str, aspect_ratio: str, gcs_bucket_uri: str, model_name: str):
        prompt_data = {
            'style': style,
            'shot_type': shot_type,
            'description': item_description,
        }
        prompt_string = yaml.dump(prompt_data, indent=2, default_flow_style=False)
        print(f"--- Simulating Image Generation for: {item_name} with model {model_name} ---")
        sanitized_name = item_name.lower().replace(" ", "-")
        image_gcs_uri = f"{gcs_bucket_uri}/mock-images/{sanitized_name}.png"
        return image_gcs_uri

    def _generate_storyboard(self, SCENARIO_WITH_IMAGES: str, num_scenes: int, style: str, model_name: str):
        print(f"Generating storyboard scenes with model: {model_name}...")
        try:
            scenario_data = json.loads(SCENARIO_WITH_IMAGES)
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON input"})

        prompt = storycraft_prompts.get_scenes_prompt(scenario_data, num_scenes, style)
        # This is a placeholder for a real API call
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
        try:
            scenes_data = json.loads(mock_response_text)
            scenario_data["scenes"] = scenes_data.get("scenes", [])
        except json.JSONDecodeError:
            scenario_data["scenes"] = []

        return json.dumps(scenario_data, indent=4)

    def _select_scene(self, FULL_SCENARIO: str, scene_index: int):
        print(f"Selecting scene at index: {scene_index}")
        try:
            scenario_data = json.loads(FULL_SCENARIO)
        except json.JSONDecodeError:
            return (FULL_SCENARIO, "{}", "{}", "",)

        scenes = scenario_data.get("scenes", [])

        if not scenes or not isinstance(scenes, list) or scene_index >= len(scenes):
            return (FULL_SCENARIO, "{}", "{}", "",)
        
        selected_scene = scenes[scene_index]

        image_prompt_obj = selected_scene.get("imagePrompt", {})
        video_prompt_obj = selected_scene.get("videoPrompt", {})
        voiceover_text = selected_scene.get("voiceover", "")

        image_prompt_str = json.dumps(image_prompt_obj, indent=4)
        video_prompt_str = json.dumps(video_prompt_obj, indent=4)

        return (FULL_SCENARIO, image_prompt_str, video_prompt_str, voiceover_text)

    def _generate_scene_video(self, FULL_SCENARIO_PASSTHROUGH, IMAGE_PROMPT, VIDEO_PROMPT, gcs_bucket_uri, image_model, video_model):
        print("--- Starting Scene Video Generation ---")
        try:
            full_scenario = json.loads(FULL_SCENARIO_PASSTHROUGH)
            image_prompt_data = json.loads(IMAGE_PROMPT)
            video_prompt_data = json.loads(VIDEO_PROMPT)
        except json.JSONDecodeError as e:
            return f"{gcs_bucket_uri}/error.mp4"

        scene_keyframe_uri = self._generate_keyframe_image(full_scenario, image_prompt_data, gcs_bucket_uri, image_model)

        if "error" in scene_keyframe_uri:
            return f"{gcs_bucket_uri}/error.mp4"

        video_clip_uri = self._generate_video_clip(scene_keyframe_uri, video_prompt_data, full_scenario, gcs_bucket_uri, video_model)

        return video_clip_uri

    def _generate_keyframe_image(self, full_scenario, image_prompt_data, gcs_bucket_uri, model_name):
        subjects = image_prompt_data.get("Subject", [])
        character_uris = []
        for subject in subjects:
            char_name = subject.get("name")
            for character in full_scenario.get("characters", []):
                if character.get("name") == char_name:
                    if "imageGcsUri" in character:
                        character_uris.append(character["imageGcsUri"])

        prompt_parts = []
        for uri in character_uris:
            prompt_parts.append(f"[Image from: {uri}]")
        
        text_prompt = yaml.dump(image_prompt_data, indent=2, default_flow_style=False)
        prompt_parts.append(text_prompt)

        keyframe_uri = f"{gcs_bucket_uri}/scene_keyframes/mock_keyframe_{time.time()}.png"
        return keyframe_uri

    def _generate_video_clip(self, keyframe_uri, video_prompt_data, full_scenario, gcs_bucket_uri, model_name):
        video_text_prompt = f'''Action: {video_prompt_data.get("Action", "")}Camera Motion: {video_prompt_data.get("Camera_Motion", "")}'''
        aspect_ratio = full_scenario.get("aspectRatio", "16:9")
        duration_seconds = full_scenario.get("durationSeconds", 8)

        video_uri = f"{gcs_bucket_uri}/video_clips/mock_clip_{time.time()}.mp4"
        return video_uri

    def _generate_audio(self, FULL_SCENARIO_PASSTHROUGH, VOICEOVER_TEXT, gcs_bucket_uri, tts_model_voice, lyria_model):
        print("--- Starting Audio Generation ---")
        try:
            full_scenario = json.loads(FULL_SCENARIO_PASSTHROUGH)
        except json.JSONDecodeError as e:
            return (f"{gcs_bucket_uri}/error.mp3", f"{gcs_bucket_uri}/error.mp3",)

        voiceover_uri = self._generate_voiceover(VOICEOVER_TEXT, full_scenario, gcs_bucket_uri, tts_model_voice)
        music_uri = self._generate_music(full_scenario, gcs_bucket_uri, lyria_model)

        return (voiceover_uri, music_uri)

    def _generate_voiceover(self, voiceover_text, full_scenario, gcs_bucket_uri, tts_model_voice):
        if not voiceover_text.strip():
            return ""

        language_code = full_scenario.get("language", {}).get("code", "en-US")
        voiceover_gcs_uri = f"{gcs_bucket_uri}/voiceovers/mock_voiceover_{time.time()}.mp3"
        return voiceover_gcs_uri

    def _generate_music(self, full_scenario, gcs_bucket_uri, lyria_model):
        music_prompt = full_scenario.get("music", "A gentle, swelling orchestral piece.")
        music_gcs_uri = f"{gcs_bucket_uri}/music/mock_music_{time.time()}.mp3"
        return music_gcs_uri

    def _stitch_video(self, video_clip_uris: list, voiceover_uris: list, music_uri: str, gcs_bucket_uri: str):
        print(f"--- Assembling video from {len(video_clip_uris)} clips ---")
        # This is a placeholder for a real video stitching implementation that would
        # download, concatenate, and mix the assets before re-uploading.
        final_gcs_uri = f"{gcs_bucket_uri}/final_videos/final_movie_{time.time()}.mp4"
        return final_gcs_uri

NODE_CLASS_MAPPINGS = {
    "StoryCraft_Combined": StoryCraft_Combined
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StoryCraft_Combined": "StoryCraft Combined Pipeline"
}