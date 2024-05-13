from PIL import Image
import imagehash
import os
import numpy as np
from images_ext import IMAGES_EXT


class DuplicateRemover:
    def __init__(self, dirname, hash_size=8):
        self.dirname = dirname
        self.hash_size = hash_size

    def subdirs(self):
        for subdir, dirs, files in os.walk(self.dirname):
            for file in files:
                yield os.path.join(subdir, file)

    def no_subdirs(self):
        for file in os.listdir(self.dirname):
            yield os.path.join(self.dirname, file)

    def find_duplicates(self, subdirs=False):
        """
        Find and Delete Duplicates
        """

        hashes = {}
        duplicates = []
        print("Finding Duplicates Now!\n")

        if subdirs:
            file_iter = self.subdirs
        else:
            file_iter = self.no_subdirs

        for file in file_iter():
            file_ext = os.path.splitext(file)[1][1:].lower()

            # Skip not images
            if file_ext not in IMAGES_EXT:
                continue
            else:
                image = file

            # Hashing images
            try:
                image_path = file
                with Image.open(image_path) as img:
                    temp_hash = imagehash.average_hash(img, self.hash_size)
                    if temp_hash in hashes:
                        print(
                            f"Duplicate {image} \nfound for Image {hashes[temp_hash]}!\n"
                        )
                        duplicates.append(image_path)
                    else:
                        hashes[temp_hash] = image
            except Exception as e:
                print(e)

        # Delete duplicates
        if len(duplicates) != 0:
            a = input(
                f"Do you want to delete these {len(duplicates)} Images? Press Y or N:  "
            )
            space_saved = 0
            if a.strip().lower() == "y":
                for duplicate in duplicates:
                    space_saved += os.path.getsize(duplicate)

                    os.remove(duplicate)
                    print(f"{duplicate} Deleted Succesfully!")

                print(f"\n\nYou saved {round(space_saved / 1000000)} mb of Space!")
            else:
                print("Thank you for Using Duplicate Remover")
        else:
            print("No Duplicates Found :(")

    def find_similar(self, location, similarity=80):
        fnames = os.listdir(self.dirname)
        threshold = 1 - similarity / 100
        diff_limit = int(threshold * (self.hash_size**2))

        with Image.open(location) as img:
            hash1 = imagehash.average_hash(img, self.hash_size).hash

        print(f"Finding Similar Images to {location} Now!\n")
        for image in fnames:
            try:
                with Image.open(os.path.join(self.dirname, image)) as img:
                    hash2 = imagehash.average_hash(img, self.hash_size).hash

                    if np.count_nonzero(hash1 != hash2) <= diff_limit:
                        print(
                            f"{image} image found {similarity}% similar to {location}"
                        )
            except Exception as e:
                print(e)
