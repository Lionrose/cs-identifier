import io
import os
import sys
import urllib.request

from PIL import Image, ImageChops


REFERENCE_DIR = "reference_images"
PET_IMAGE_URL = "https://www.chickensmoothie.com/pet/%s&trans=1&noitems.jpg"
UNKNOWN_TYPE = "UNKNOWN"
ERROR_TYPE = "ERROR"

def crop(img):
  """Remove part of the pet that says "___'s pet"""
  w, h = img.size
  return img.crop((0, 0, w, h-9))


def download_image(img_url):
  """Downloads an image from a URL and returns an `Image` object."""
  with urllib.request.urlopen(img_url) as url:
    f = io.BytesIO(url.read())
  return Image.open(f)


def equal(image1, image2):
  """Checks that 2 images are exactly the same."""
  return ImageChops.difference(image1, image2).getbbox() is None


class PetReference(object):
  def __init__(self, reference_dir):
    self.reference_dir = reference_dir

    # Map string pet type/code to an Image
    self.type_to_image = {}

    # Maps int tuple of (width, height) to a list of pet types
    self.size_to_type = {}

    for img_file in os.listdir(reference_dir):
      pet_type = img_file.split('.')[0]
      img = crop(Image.open(os.path.join(reference_dir, img_file)))
      size = img.size

      self.type_to_image[pet_type] = img
      if size not in self.size_to_type:
        self.size_to_type[size] = []
      self.size_to_type[size].append(pet_type)

  def get_type(self, pet_id):
    # Assert pet_id is an integer
    assert isinstance(pet_id, int), "Pet ID must be an integer"
    image_url = PET_IMAGE_URL % pet_id
    downloaded_img = crop(download_image(image_url))

    size = downloaded_img.size

    if size in self.size_to_type:
      for pet_type in self.size_to_type[size]:
        img = self.type_to_image[pet_type]
        if equal(img, downloaded_img):
          return pet_type

    return UNKNOWN_TYPE


def main(args):
  if len(args) < 2:
    print("Please enter an input file. Quitting.")
    sys.exit(0)

  ref = PetReference(REFERENCE_DIR)

  input_file = args[1]
  output_file = os.path.basename(input_file).split('.')[0] + "_out.txt"

  errors = []

  with open(input_file, 'r') as f:
    with open(output_file, 'w') as w:
      for line in f:
        pet_id = line.strip()
        if not pet_id:
          continue

        print("Identifying pet", pet_id)
        try:
          pet_id = int(pet_id)
          pet_type = ref.get_type(pet_id)
        except Exception as e:
          print("\tSkipped %s because there was an error.")
          errors.append((pet_id, e))
          pet_type = ERROR_TYPE

        w.write("%s,%s" % (pet_id, pet_type))

  if errors:
    print("List of all errors")
    for pet_id, e in errors:
      print("\nPet ID:", pet_id)
      print(e)


if __name__ == "__main__":
  main(sys.argv)