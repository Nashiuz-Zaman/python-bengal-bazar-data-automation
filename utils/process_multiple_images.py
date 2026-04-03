import json


def process_multiple_images(multiple_image_data):
    """
    Convert multipleImageData to JSON string with only imageUrl and fullImageUrl,
    removing LevelId.
    """
    result = []
    for item in multiple_image_data or []:
        result.append(
            {
                "imageUrl": item.get("ImageUrl"),
                "fullImageUrl": item.get("fullimageURl"),  
            }
        )
    return json.dumps(result, ensure_ascii=False) 
