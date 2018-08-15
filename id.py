import io
import os
import sys
import urllib.request

from PIL import Image, ImageChops


REFERENCE_DIR = "reference_images"
PET_IMAGE_URL = "https://www.chickensmoothie.com/pet/%s&trans=1&noitems.jpg"
UNKNOWN_key = "UNKNOWN"
ERROR_key = "ERROR"

def crop(img):
  """Remove part of the pet that says "___'s pet and transparent edges."""
  w, h = img.size

  h = h - 9
  img = img.crop((0, 0, w, h))

  # Get cropping border
  left = w
  top = h
  right = 0
  bottom = 0

  img_data = img.getdata()
  # Loop from left->right and top->bottom to get the left/top cropping borders.
  for i_h in range(h):
    for i_w in range(w):
      if img_data[i_w + i_h * w] == (0, 0, 0, 0):
        continue
      top = min(top, i_h)
      left = min(left, i_w)
      break

  # Loop from right->left and bottom->top to get the right/bottom cropping
  # borders.
  for i_h in range(h - 1, 0, -1):
    for i_w in range(w - 1, 0, -1):
      if img_data[i_w + i_h * w] == (0, 0, 0, 0):
        continue
      bottom = max(bottom, i_h)
      right = max(right, i_w)
      break

  img = img.crop((left, top, right, bottom))
  return img



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

    # Map string pet key/code to an Image
    self.key_to_image = {}

    # Maps int tuple of (width, height) to a list of pet keys
    self.size_to_key = {}

    for img_file in os.listdir(reference_dir):
      pet_key = img_file.split('.')[0]
      img = crop(Image.open(os.path.join(reference_dir, img_file)))
      size = img.size

      self.key_to_image[pet_key] = img
      if size not in self.size_to_key:
        self.size_to_key[size] = []
      self.size_to_key[size].append(pet_key)

  def get_key(self, pet_id):
    # Assert pet_id is an integer
    assert isinstance(pet_id, int), "Pet ID must be an integer"
    image_url = PET_IMAGE_URL % pet_id
    downloaded_img = crop(download_image(image_url))

    size = downloaded_img.size

    if size in self.size_to_key:
      for pet_key in self.size_to_key[size]:
        img = self.key_to_image[pet_key]
        if equal(img, downloaded_img):
          return pet_key

    return UNKNOWN_key


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
          pet_key = ref.get_key(pet_id)
        except Exception as e:
          print("\tSkipped %s because there was an error.")
          errors.append((pet_id, e))
          pet_key = ERROR_key

        w.write("%s,%s\n" % (pet_id, pet_key))

  if errors:
    print("List of all errors")
    for pet_id, e in errors:
      print("\nPet ID:", pet_id)
      print(e)


if __name__ == "__main__":
  main(sys.argv)