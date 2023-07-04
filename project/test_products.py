from config import settings as project_settings
from django.conf import settings
import django
import sys
import logging
import os
from django.core.exceptions import ObjectDoesNotExist


FILENAME = "products_pk_list"


if __name__ == "__main__":
    settings.configure(default_settings=project_settings, DEBUG=True)
    django.setup()

    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] (%(name)s) - %(message)s",
        datefmt="%H:%M:%S",
    )
    logging.root.setLevel(logging.NOTSET)

    from main.models import Products

    arg = sys.argv[1]

    if arg == "create":
        primary_keys = []

        product = Products.objects.create(
            name="Smartphone Samsung A035",
            price=3299,
            image_url="https://i.ibb.co/2cB80qY/Samsung-A035.webp",
            creator="Admin",
        )
        primary_keys.append(product.pk)

        product = Products.objects.create(
            name="Smartphone Xiaomi Mi 11T",
            price=8699,
            image_url="https://i.ibb.co/QDyzRF7/Xiaomi-Mi-11-T.webp",
            creator="Admin",
        )
        primary_keys.append(product.pk)

        product = Products.objects.create(
            name="Smartphone Apple iPhone 13",
            price=17900,
            image_url="https://i.ibb.co/pzz3nCz/Apple-i-Phone-13.webp",
            creator="Admin",
        )
        primary_keys.append(product.pk)

        product = Products.objects.create(
            name="Laptop Acer TMP215-53",
            price=10000,
            image_url="https://i.ibb.co/0FZvdP8/Acer-TMP215-53.webp",
            creator="Admin",
        )
        primary_keys.append(product.pk)

        product = Products.objects.create(
            name="Laptop Asus VivoBook K513EA-L11950",
            price=17000,
            image_url="https://i.ibb.co/M5CXpmk/Asus-Vivo-Book-K513-EA-L11950.webp",
            creator="Admin",
        )
        primary_keys.append(product.pk)

        product = Products.objects.create(
            name="TV LG 60UP77506LA",
            price=12800,
            image_url="https://i.ibb.co/89843fv/LG-60-UP77506-LA.jpg",
            creator="Admin",
        )
        primary_keys.append(product.pk)

        product = Products.objects.create(
            name="TV Sony XR65A80JAEP",
            price=46000,
            image_url="https://i.ibb.co/gSPShwQ/Sony-XR65-A80-JAEP.webp",
            creator="Admin",
        )
        primary_keys.append(product.pk)

        product = Products.objects.create(
            name="Headphones Hoco ES280SAPGD",
            price=900,
            image_url="https://i.ibb.co/7vkb2xd/Hoco-ES280-SAPGD.webp",
            creator="Admin",
        )
        primary_keys.append(product.pk)

        product = Products.objects.create(
            name="Headphones JBL Tune 215 TWS",
            price=1800,
            image_url="https://i.ibb.co/FhsWSDt/JBL-Tune-215-TWS.webp",
            creator="Admin",
        )
        primary_keys.append(product.pk)

        product = Products.objects.create(
            name="Microphone Marvo MIC-01",
            price=350,
            image_url="https://i.ibb.co/hXr8fxS/Marvo-MIC-01.webp",
            creator="Admin",
        )
        primary_keys.append(product.pk)

        with open(FILENAME, "wb") as file:
            file.write(bytes(primary_keys))

        logging.info(
            f'Test products were created successfully. Their primary keys: {", ".join([str(pk) for pk in primary_keys[:-1]]) + f" and {primary_keys[-1]}"}.'
        )
    elif arg == "delete":
        if os.path.exists(FILENAME):
            with open(FILENAME, "rb") as file:
                primary_keys = list(file.read())
            os.remove(FILENAME)

            for pk in primary_keys:
                try:
                    Products.objects.get(pk=pk).delete()
                except ObjectDoesNotExist:
                    logging.warning(
                        f"Product with PK {pk} was not deleted, because it not exists"
                    )
        else:
            logging.critical(
                f"Bytes file ({FILENAME}) with test products PK list was not found! Have you created test products?"
            )
