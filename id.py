import sys

REFERENCE_DIR = "reference_images"
GENERATED_DIR = "_generated_images"

def crop_and_shrink(img):
  pass

def load_reference(ref_dir):
  pass


def main(args):
  if len(args) < 2:
    print("Please enter an input file.")

  image_to_type = load_reference(REFERENCE_DIR)
  input_file = args[1]


if __name__ == "__main__":
  main(sys.argv)