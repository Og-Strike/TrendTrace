import os
import numpy as np
import cv2
from skimage.measure import label, regionprops, find_contours
import argparse
import google.generativeai as genai
import json
import universal

def mask_to_border(mask):
    h, w = mask.shape
    border = np.zeros((h, w))

    contours = find_contours(mask, 128)
    for contour in contours:
        for c in contour:
            x = int(c[0])
            y = int(c[1])
            border[x][y] = 255

    return border

""" Mask to bounding boxes """
def mask_to_bbox(mask):
    bboxes = []

    mask = mask_to_border(mask)
    lbl = label(mask)
    props = regionprops(lbl)
    for prop in props:
        x1 = prop.bbox[1]
        y1 = prop.bbox[0]
        x2 = prop.bbox[3]
        y2 = prop.bbox[2]
        bboxes.append([x1, y1, x2, y2])

    return bboxes

def parse_mask(mask, target_shape):
    mask_resized = cv2.resize(mask, (target_shape[1], target_shape[0]), interpolation=cv2.INTER_NEAREST)
    mask_resized = np.expand_dims(mask_resized, axis=-1)
    mask_resized = np.concatenate([mask_resized, mask_resized, mask_resized], axis=-1)
    return mask_resized

def non_max_suppression(boxes, overlapThresh):
    if len(boxes) == 0:
        return []

    pick = []

    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)

    while len(idxs) > 0:
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        overlap = (w * h) / area[idxs[:last]]

        idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlapThresh)[0])))

    return boxes[pick]

def calculate_mask_area(mask_path):
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    masked_pixels = cv2.countNonZero(mask)
    total_pixels = mask.shape[0] * mask.shape[1]
    mask_area_percentage = (masked_pixels / total_pixels) * 100
    return mask_area_percentage


def generate_crop(x,mask_path,name_image,tmp_dir):
    y = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

    """ Check if images are valid """
    if x is None or y is None:
        print(f"Error loading image or mask")
        exit(1)

    """ Detecting bounding boxes """
    bboxes = mask_to_bbox(y)

    """ Apply Non-Maximum Suppression to remove overlapping boxes """
    if len(bboxes) > 0:
        boxes = np.array(bboxes)
        boxes = non_max_suppression(boxes, overlapThresh=0.3)

    """ Marking bounding box on image """
    for idx, bbox in enumerate(boxes):
        largest_box = boxes[np.argmax((boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0]))]
        x1, y1, x2, y2 = largest_box
        cropped_image = x[y1:y2, x1:x2]
        save_path = os.path.join(tmp_dir, f"{name_image}.png")
        cv2.imwrite(save_path, cropped_image)
        return save_path

def generate_features(path,model_name):

    genai.configure(api_key=universal.API_KEY)
    sample_file = genai.upload_file(path=path,
                                )

    print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")
    file = genai.get_file(name=sample_file.name)
    print(f"Retrieved file '{file.display_name}' as: {sample_file.uri}")
    model = genai.GenerativeModel(model_name=model_name)

    # Prompt the model with text and the previously uploaded image.
    response = model.generate_content([sample_file, '''Return one word for each thing about cloth that goes as follows {
        "Type": "Specifies the type of clothing not accessories",
        "Color": "Identifies the dominant color(s)",
        "Pattern": "Describes any patterns present (e.g., \\"striped\\")",
        "Texture": "Describes the texture of the material (e.g., \\"knit\\", \\"smooth\\")",
        "Brand": "Identifies the brand if visible (e.g., \\"Nike\\", \\"Adidas\\")",
        "Style": "Describes the style (e.g., \\"casual\\", \\"formal\\")",
        "Season": "Suggests the season the clothing is suitable for (e.g., \\"winter\\", \\"summer\\")",
        "Gender": "Suggests the target gender (e.g., \\"male\\", \\"female\\", \\"unisex\\")",
        "Usage": "Suggests potential usage (e.g., \\"outdoor\\", \\"sports\\")"
    }'''])

    try:
        info_dict = json.loads(response.text)
    except Exception as e:
        print("Error Getting data")
        return None


    return info_dict



    

if __name__ == "__main__":
    """ Specify the paths for the image and mask """
    parser = argparse.ArgumentParser(description="Process an image and its mask to extract bounding boxes.")
    parser.add_argument("--image", required=True, help="Path to the input image.")
    parser.add_argument("--name_image", required=True, help="Path to the mask image.")

    args = parser.parse_args()

    image_path = args.image
    name_image=args.name_image

    """ Extract the name """

    """ Read image and mask """
    x = cv2.imread(image_path, cv2.IMREAD_COLOR)
    cwd = os.getcwd()
    tmp_dir=os.path.join(cwd,'tmp')
    mask1_path = os.path.join(cwd, 'output', 'alpha',f'{name_image}_1.png')
    mask2_path = os.path.join(cwd, 'output', 'alpha',f'{name_image}_2.png')
    mask3_path = os.path.join(cwd, 'output', 'alpha',f'{name_image}_3.png')

    upper=False
    lower=False
    full=False

    area_full = 0.0
    area_upper = 0.0
    area_lower = 0.0

    #Final dict
    universal.final_dict={'upper':None,'lower':None,'full':None}
    

    if(os.path.exists(mask3_path)):
        full=True
        area_full = calculate_mask_area(mask3_path)


    if(os.path.exists(mask1_path)):
        upper=True
        area_upper = calculate_mask_area(mask1_path)

    if(os.path.exists(mask2_path)):
        lower=True
        area_lower = calculate_mask_area(mask2_path)
    
    print(area_full,area_upper,area_lower)

    if (full and area_full>(area_lower+area_upper)*3):
        full_name_image=name_image+'_full'
        fullbox_image=generate_crop(x,mask3_path,full_name_image,tmp_dir)
        universal.final_dict['full']=generate_features(fullbox_image,"gemini-1.5-flash-001")
        # os.remove(fullbox_image)

    if upper and area_upper > 5:
        full_name_image=name_image+'_upper'
        upperbox_image=generate_crop(x,mask1_path,full_name_image,tmp_dir)
        universal.final_dict['upper']=generate_features(upperbox_image,"gemini-1.5-pro-001")
        # os.remove(upperbox_image)


    if lower and area_lower >= 5:
        full_name_image=name_image+'_lower'
        lowerbox_image=generate_crop(x,mask2_path,full_name_image,tmp_dir)
        universal.final_dict['lower']=generate_features(lowerbox_image,"gemini-1.5-pro-001")
        # os.remove(lowerbox_image)

    full_seg=os.path.join(cwd, 'output', 'cloth_seg',f'{name_image}_final_seg.png')

    print(f"Final Output For Image {name_image} : \n {universal.final_dict}  ")

    with open('database.py') as file:
        exec(file.read())
        file.close()

    # if os.path.exists(mask1_path):
    #      os.remove(mask1_path)
    # if os.path.exists(mask2_path):
    #      os.remove(mask2_path)
    # if os.path.exists(mask3_path):
    #     os.remove(mask3_path)
    # if os.path.exists(full_seg):
    #     os.remove(full_seg)
    

   




    



    
    

    """ Check if images are valid """

    # parse_mask_resized = parse_mask(y, x.shape)

    # """ Saving the image """
    # cat_image = np.concatenate([x, parse_mask_resized], axis=1)
    # cv2.imwrite(f"{name}_result.png", parse_mask_resized)

    """ Display the image """
    # cv2.imshow("Result", cropped_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # exit()
