import os

from dotenv import load_dotenv
from imagekitio import ImageKit

load_dotenv()

private_key = os.getenv("IMAGEKIT_PRIVATE_KEY")

if not private_key:
    raise RuntimeError("IMAGEKIT_PRIVATE_KEY is missing from your .env file")

imagekit = ImageKit(
    private_key=private_key,
)
