# CS Pet Identifier (LITERALLY NO CODE WRITTEN BUT HERE'S THE DOCUMENTATION)

## Required

* [Python >= 3.5](https://www.python.org/downloads/)
* [Pillow (for image processing)](https://pypi.org/project/Pillow/)

## Run with example data
```
python id.py example_input.txt
```

This will produce an output file named "example_input_out.txt"

## Configure inputs
This script takes in two inputs:

1. Input file: Pet IDs separted by lines (e.g. example_input.txt).
2. Reference images:

   Must be **named by key** (see the names in the `reference_image` folder).

   These images must have a **transparent background, and saved without items**. For example,
   * DO: [Pet without items](https://www.chickensmoothie.com/pet/40773414&trans=1&noitems.jpg)

     ![https://www.chickensmoothie.com/pet/40773414&trans=1&noitems.jpg](https://www.chickensmoothie.com/pet/40773414&trans=1&noitems.jpg)

   * DO NOT: [Pet with items](https://www.chickensmoothie.com/pet/40773414&trans=1.jpg)

     ![https://www.chickensmoothie.com/pet/40773414&trans=1.jpg](https://www.chickensmoothie.com/pet/40773414&trans=1.jpg)

   Note that the URLs have `.jpg`, but the images are actually PNGS. I don't know why it's like this. ¯\\\_(ツ)_/¯

## Outputs
The output file will be named `${INPUT_NAME}_out.txt`.

Each line contains the `ID` and `KEY` separated by a comma

e.g.
```
40773414,E2BA461F667E5DB6881FBC1C3442CC86
51218734,8CF714DA1859489A09C1C3F374935782
```