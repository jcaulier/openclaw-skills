import os
import sys
import json
import base64
from google.oauth2 import service_account
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel


def generate_image(prompt: str, ratio: str = None) -> str:
    """Generates an image using Imagen 3 via Google Cloud Vertex AI."""
    
    # Retrieve environment variables
    project_id = os.environ.get("IMAGEN_PROJECT_ID")
    service_account_email = os.environ.get("IMAGEN_SERVICE_ACCOUNT_EMAIL")
    private_key_content = os.environ.get("IMAGEN_PRIVATE_KEY_CONTENT")
    
    # Validate credentials
    if not all([project_id, service_account_email, private_key_content]):
        raise ValueError(
            "The IMAGEN_PROJECT_ID, IMAGEN_SERVICE_ACCOUNT_EMAIL, and IMAGEN_PRIVATE_KEY_CONTENT environment variables must be defined."
        )
    
    try:
        # Create credentials from necessary information and the PEM key directly
        credentials_info = {
            "private_key": private_key_content.replace("\\n", "\n"),  # Replace escaped newlines
            "client_email": service_account_email,
            "token_uri": "https://oauth2.googleapis.com/token",
        }
        credentials = service_account.Credentials.from_service_account_info(credentials_info)
        
        # Initialize Vertex AI with the credentials and project ID
        vertexai.init(project=project_id, location="us-central1", credentials=credentials)
        print("✅ Vertex AI initialized using private key from environment variables.")
        
        print(f"🎨 Generation prompt: {prompt}")
        if ratio:
            print(f"📐 Aspect ratio requested: {ratio}")
        
        # Load the model
        model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")
        print("✅ Imagen model loaded.")
        
        # Build the full prompt
        full_prompt = prompt
        if ratio:
            full_prompt += f", aspect ratio {ratio}"
        
        print("⏳ Image generation in progress...")
        images = model.generate_images(
            prompt=full_prompt,
            number_of_images=1
        )
        
        if images.images and len(images.images) > 0:
            output_file = "/data/.openclaw/workspace/generated_image.png"
            images[0].save(output_file)
            print(f"✅ Image saved: {output_file}")
            return output_file
        else:
            raise Exception("No image was generated.")
            
    except Exception as e:
        print(f"❌ Error during image generation: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        raise


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generates an image using Imagen 3")
    parser.add_argument("--prompt", required=True, help="The image prompt")
    parser.add_argument("--ratio", default=None, help="Aspect ratio (e.g., 16:9)")
    
    args = parser.parse_args()
    
    try:
        output_path = generate_image(args.prompt, args.ratio)
        print(f"\n🎉 SUCCESS: Image generated at {output_path}")
        
        # Signal for OpenClaw agent
        print(f"__IMAGE_GENERATED__: {output_path}")
        
    except Exception as e:
        print(f"\n💥 FAILURE: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
