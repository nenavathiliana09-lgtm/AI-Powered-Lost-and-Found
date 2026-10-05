from sentence_transformers import SentenceTransformer, util
from PIL import Image

model = SentenceTransformer("clip-ViT-B-32")


def get_image_embedding(image_path):
    image = Image.open(image_path).convert("RGB")
    return model.encode(image, convert_to_tensor=True)


def calculate_similarity(image1, image2):
    embedding1 = get_image_embedding(image1)
    embedding2 = get_image_embedding(image2)

    score = util.cos_sim(embedding1, embedding2)
    return float(score[0][0])


def calculate_text_similarity(text1, text2):
    embedding1 = model.encode(text1, convert_to_tensor=True)
    embedding2 = model.encode(text2, convert_to_tensor=True)

    score = util.cos_sim(embedding1, embedding2)
    return float(score[0][0])


def calculate_location_similarity(location1, location2):
    location1 = location1.lower()
    location2 = location2.lower()

    if location1 == location2:
        return 1.0

    words1 = set(location1.split())
    words2 = set(location2.split())

    if not words1 or not words2:
        return 0.0

    common = words1.intersection(words2)

    return len(common) / max(len(words1), len(words2))


def calculate_overall_score(image_score, text_score, location_score):
    image_score = max(0, image_score)
    text_score = max(0, text_score)

    return (
        image_score * 0.6
        + text_score * 0.3
        + location_score * 0.1
    )