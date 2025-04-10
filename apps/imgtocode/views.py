import os
import base64
import re
import hashlib
import logging
import traceback
import requests
from bs4 import BeautifulSoup
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from anthropic import Anthropic
from .models import DesignRequest
from .serializers import DesignRequestSerializer, DesignHistorySerializer

# Configure logging
logger = logging.getLogger(__name__)

# Use an environment variable for the API key instead of hard coding it.
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "your-default-api-key-if-needed")
client = Anthropic(api_key=API_KEY)

def encode_image_to_base64(image):
    if image:
        data = image.read()
        image.seek(0)  # Reset the file pointer for future use.
        return base64.b64encode(data).decode('utf-8')
    return None

def fetch_webpage_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.prettify()
        return f"Error: Unable to fetch webpage, status code {response.status_code}"
    except Exception as e:
        logger.error("Error fetching webpage content: %s", e)
        return f"Error: Exception occurred while fetching webpage."

def generate_prompt_hash(prompt: str) -> str:
    return hashlib.sha256(prompt.encode('utf-8')).hexdigest()

class GenerateFlutterCodeView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = DesignRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        image = serializer.validated_data.get('image')
        url = serializer.validated_data.get('url')
        prompt = serializer.validated_data.get('prompt') or "Generate code for this image or URL."
        user = request.user

        # Build up the message payload
        message_content = []

        # Process image, if provided
        if image:
            image_base64 = encode_image_to_base64(image)
            message_content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",  # You might want to make this dynamic based on the image type.
                    "data": image_base64
                }
            })

        # Process URL, if provided. (This adds the webpage content as text.)
        if url:
            content = fetch_webpage_content(url)
            message_content.append({
                "type": "text",
                "text": f"Convert this webpage into Tailwind CSS code:\n{content}"
            })

        # Finally add the prompt text
        message_content.append({
            "type": "text",
            "text": prompt
        })

        try:
            # Log the outbound message payload for debugging
            logger.info("Sending message to Anthropic with content: %s", message_content)

            # Attempt the API call
            message = client.messages.create(
                model="claude-3-7-sonnet-20250219",
                max_tokens=5000,
                messages=[{"role": "user", "content": message_content}]
            )

            # Log the raw API response
            logger.info("Received message response: %s", message)

            # Adjust parsing based on the actual response structure.
            try:
                response_text = message.content[0].text
            except (TypeError, AttributeError, IndexError):
                response_text = getattr(message, "content", str(message))
            logger.info("Parsed response text: %s", response_text)

            # Extract code from markdown code blocks.
            code_pattern = r"```(.*?)```"
            match = re.search(code_pattern, response_text, re.DOTALL)
            responsed_code = match.group(1).strip() if match else "No code found in the response."

            prompt_hash = generate_prompt_hash(prompt)

            # Save the design request to the database.
            DesignRequest.objects.create(
                user=user,
                prompt=prompt,
                prompt_hash=prompt_hash,
                url=url if url else None,
                image=image if image else None,
                ai_response=responsed_code
            )

            return Response({"responsed_code": responsed_code}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("Error in GenerateFlutterCodeView: %s", traceback.format_exc())
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserDesignHistoryView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        design_requests = DesignRequest.objects.filter(user=user).order_by("-created_at")
        serializer = DesignHistorySerializer(design_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
