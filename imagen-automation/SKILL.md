---
name: imagen-automation
description: Automates image generation and sending via Google Imagen 3 (Vertex AI).
---

# Skill: Imagen Automation

## Description

This skill automates image generation via the Google Cloud Vertex AI Imagen 3 API and automatically sends the resulting image to the chat channel after its creation. It is designed to simplify the visual creation process and enhance agent proactivity.

## Benefits

* **Proactivity:** Images are sent as soon as they are ready, without waiting or manual request.
* **Seamlessness:** Simplifies the workflow by eliminating a manual step after generation.
* **Continuity:** Automatic sending logic is integrated, ensuring consistency across sessions and agents.
* **Portability:** The skill is packaged for reusability in other OpenClaw projects.

---

### Technical Documentation

**Google API Used:** Image generation is performed via the **Google Cloud Vertex AI Imagen 3 API**. Specifically, the `imagen-3.0-generate-002` model is used by the skill's main script (`imagen_generate.py`).

**Automatic Detection and Sending Mechanism:**

1. **Script Execution:** The agent executes the Python script `imagen_generate.py` (e.g., via `python3 ./skills/imagen-automation/scripts/imagen_generate.py --prompt "Your prompt here"`).

2. **Completion Signal:** Once the image is generated and saved locally (default: `/data/.openclaw/workspace/generated_image.png`), the `imagen_generate.py` script prints a specific line to its standard output: `__IMAGE_GENERATED__: <full_path_to_image>`.

3. **Agent Interception:** Thanks to a directive added in `AGENTS.md` (which is read by the agent at the start of each session), the agent monitors command output. When it detects the string `__IMAGE_GENERATED__:`, it extracts the image path.

4. **Automatic Sending:** The agent then uses the `message` tool with the `send` action, specifying the image path via the `media` parameter and a confirmation message to the current chat channel.

**Key Skill Files:**

* **`SKILL.md` (this file):** Complete skill documentation.
* **`scripts/imagen_generate.py`:** The main Python script that interacts with the Imagen 3 API.
* **`_meta.json`:** Skill metadata for OpenClaw.

**Required Configuration (Environment Variables):**

The `imagen_generate.py` script requires the following environment variables to be defined on the system where OpenClaw is running. These variables contain your authentication information for the Google Cloud API.

* `IMAGEN_PROJECT_ID` : Your Google Cloud project ID.
* `IMAGEN_SERVICE_ACCOUNT_EMAIL` : The email address of the service account used for authentication.
* `IMAGEN_PRIVATE_KEY_CONTENT` : The full content of your JSON private key, base64 encoded **or with escaped newlines (`\n`) if you define it directly in a configuration file or via `export`**. It is recommended to define it securely (e.g., in OpenClaw daemon environment variables or via a secrets manager).

**Example configuration in OpenClaw's `.env` (adapt as needed):**

```
IMAGEN_PROJECT_ID="your-project-id-here"
IMAGEN_SERVICE_ACCOUNT_EMAIL="your-service-account@your-project-id-here.iam.gserviceaccount.com"
IMAGEN_PRIVATE_KEY_CONTENT="-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_CONTENT_HERE\n-----END PRIVATE KEY-----"
```

*(Make sure to replace `YOUR_PRIVATE_KEY_CONTENT_HERE` with your actual private key and properly escape newlines with `\n` if you paste it on a single line.)*

---

### Usage via Telegram

To use this feature directly from our Telegram conversation, it's very simple:

1. **Send me a message** containing the command to execute the skill's script, prefixed with `python3`.

2. Use the following format, replacing `"Your prompt here"` with the description of the image you want:

```
python3 ./skills/imagen-automation/scripts/imagen_generate.py --prompt "Your prompt here"
```

3. **Example:** If you want a "realistic photo of Gérard with blue hair", you would send me:

```
python3 ./skills/imagen-automation/scripts/imagen_generate.py --prompt "A realistic photo of Gérard with blue hair, an AI expert managing a team of AI bots in a digital agency"
```

4. **Automatic Reception:** Once the generation is complete, I will automatically send you the image directly in our Telegram conversation, without you needing to ask for it.

---

### Prompt Examples (`--prompt` for `imagen_generate.py`)

Here are some example prompts you can use with the `imagen_generate.py` script:

* **Realistic Photo:** `"A realistic photo of Gérard with blue hair, an AI expert managing a team of AI bots in a digital agency"`
* **Cartoon Style:** `"Gérard with blue hair in cartoon style that perfectly represents your identity"`
* **Fantastic Scene:** `"A futuristic cyberpunk landscape with bright neon lights and flying cars, detailed artistic style"`
* **Artistic Portrait:** `"An oil portrait of a woman with flowers in her hair, impressionist style, vibrant colors"`
* **Detailed Object:** `"A vintage camera on a wooden table, soft lighting, focus on the camera body"`

---
