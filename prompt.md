# Prompt for Generating a Modular, Prompt-Driven AI Video Application

## **Objective**

Create a modular Python application that automates the creation of a short video from a single text pitch. The application's core function is to generate individual creative scenes which are then **stitched together to make a longer, continuous clip**. The application must be "prompt-heavy," meaning the core creative logic is embedded within detailed prompts, while the Python code acts as a clean, efficient orchestrator. The code must be split into two separate files as described below.

## **Project Structure**

The application must be composed of two files:

1.  **`storycraft_prompts.py`**: A library file containing only the functions that generate the prompts. This file will not make any API calls. It will be imported by `storycraft.py`.
2.  **`storycraft.py`**: The main executable script. It will import the prompt functions, orchestrate the API calls to the various AI services, manage the data flow, and assemble the final video.

---

## **Part 1: `storycraft_prompts.py` (The Prompt Library)**

Generate a Python file named `storycraft_prompts.py` that contains the following functions. Each function's sole purpose is to take in data and return a formatted f-string that will be used as a prompt.

### **1. `get_scenario_prompt(...)`**

-   **Purpose:** To generate the prompt that turns a pitch into a full creative blueprint.
-   **Details:** This prompt should instruct the LLM to generate a JSON object containing the `scenario`, `style`, `genre`, `mood`, `music`, a detailed `color_palette` description, and full descriptions for `characters`, `settings`, and `props`.

### **2. `get_character_image_prompt(...)`**

-   **Purpose:** To generate a prompt for creating a character reference sheet.
-   **Details:** The prompt must instruct **Gemini 2.5 Flash Image** to create a `"full body portrait"`, on a `"neutral studio background"`, in the style of a `"character design sheet"`.

### **3. `get_scene_cards_prompt(...)`**

-   **Purpose:** To generate the prompt for the narrative storyboard.
-   **Details:** The prompt should instruct the LLM to act as a film director and output a JSON object containing a list of "scene cards." Each card must include: `"Scene #"`, `"Setting"`, `"Characters"`, `"Conflict/Tension"`, `"Purpose"`, a suggested `"duration"` in seconds (defaulting to 8s), and a `"transition"` (e.g., "CUT TO:", "FADE TO:").

### **4. `get_scene_assets_prompt(...)`**

-   **Purpose:** To generate the prompt that expands a single scene card into all the detailed elements needed for generation.
-   **Details:** This is a critical "prompt-heavy" function. It should take a scene card and instruct the LLM to generate a single JSON object containing:
    -   A detailed `imagePrompt` for the scene's keyframe.
    -   A detailed `videoPrompt` describing the action.
    -   A `voiceover` script for the narrator.
    -   A list of `sound_effects` crucial for immersion.

---

## **Part 2: `storycraft.py` (The Main Orchestrator)**

Generate a Python file named `storycraft.py` that imports functions from `storycraft_prompts.py` and orchestrates the entire video creation pipeline.

### **Configuration Section**

-   The script must begin with a configuration section for API keys, project IDs, and a global `ASPECT_RATIO` variable (e.g., "16:9").

### **Workflow Functions**

The script should contain the following functions, which will call the AI models.

1.  **`generate_scenario(...)`**: Takes a pitch, calls `get_scenario_prompt` to get the prompt, and executes the API call to Gemini.
2.  **`generate_character_images(...)`**: Takes the characters list, loops through them, uses `get_character_image_prompt` for each, and calls the **Gemini 2.5 Flash Image** model. It saves the results and returns a name-to-URI dictionary.
3.  **`generate_storyboard(...)`**: Takes the scenario, calls `get_scene_cards_prompt`, and executes the API call.
4.  **`generate_scene_assets(...)`**: The core asset generation loop function. For each scene card from the storyboard:
    -   It first calls `get_scene_assets_prompt` and makes an API call to Gemini to get the detailed generation instructions (image/video prompts, voiceover, sfx).
    -   It then orchestrates the individual API calls to **Gemini 2.5 Flash Image** (for the keyframe), **Veo** (for the video), and a TTS service. It must use the character and keyframe image references in the Veo prompt.
5.  **`assemble_final_video(...)`**:
    -   **Purpose:** The final step. **Stitches all the individual scene clips together to make one longer, continuous video**, adding music and titles.
    -   Uses `moviepy`.
    -   The total duration will be the number of scenes multiplied by 8 seconds.
    -   It should properly sequence the video clips, layer the voiceovers, and mix in the background music and sound effects.
    -   It should also add simple title and end cards.

### **Main Orchestration (`main()`) Function**

-   The `main()` function must clearly show the end-to-end pipeline.
-   It should initialize the API clients.
-   It must show the logical flow:
    1.  Define initial inputs (`pitch`, `style`, `num_scenes`).
    2.  Call `generate_scenario`.
    3.  Call `generate_character_images` and store the references.
    4.  Call `generate_storyboard`.
    5.  Initialize an empty list for `final_scene_assets`.
    6.  **Loop** through the `scene_cards`. In each iteration, call `generate_scene_assets` and append the result to `final_scene_assets`.
    7.  Call `assemble_final_video` with the completed list of assets.
    8.  Print a final "Success" message with the location of the output file.
-   The script should be runnable from the command line (i.e., include `if __name__ == "__main__":`).
-   Include placeholder comments like `# --- Call Gemini 2.5 Flash Image API ---` where external services are called.
