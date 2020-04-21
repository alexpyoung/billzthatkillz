import logging
import os
import re
import sys
from datetime import datetime
from glob import glob
from itertools import chain

import pyocr
import pyocr.builders
from django.core.management.base import BaseCommand
from pdf2image import convert_from_path
from PIL import Image

from purchases.models import Purchase

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

year_pattern = re.compile(r"[0-9]{2}_([0-9]{4})")


def process_pdfs(input_glob, output_dir):
    for abspath in glob(input_glob):
        filename = os.path.basename(abspath)
        logger.info("Converting %s", filename)
        convert_from_path(
            abspath,
            fmt="jpeg",
            output_folder=output_dir,
            output_file=os.path.splitext(filename)[0],
        )


def process_jpgs(input_glob, output_dir):
    # The tools are returned in the recommended order of usage
    tool = pyocr.get_available_tools()[0]
    logger.info("Using tool %s", tool.get_name())
    langs = tool.get_available_languages()
    lang = langs[0]
    logger.info("Using lang %s from %s available", lang, ", ".join(langs))

    files = glob(input_glob)
    count = len(files)
    for i, image in enumerate(files):
        filename = os.path.basename(os.path.splitext(image)[0])
        with open(f"{output_dir}/{filename}.txt", "w") as output:
            logger.info("Processing [%d/%d] %s", i + 1, count, image)
            output.write(
                tool.image_to_string(
                    Image.open(image),
                    lang=lang,
                    builder=pyocr.builders.TextBuilder(),
                )
            )


def find_purchases(input_glob, date_regex, price_regex):
    patterns = {
        "date": re.compile(date_regex),
        "price": re.compile(price_regex),
    }
    files = glob(input_glob)
    count = len(files)
    for i, text_file in enumerate(files):
        with open(text_file, "r") as text:
            year = year_pattern.findall(text_file)[0]
            logger.info("Parsing [%02d/%02d] %s", i + 1, count, text_file)
            for line in text:
                date_test = patterns["date"].findall(line)
                price_test = patterns["price"].findall(line)
                if date_test and price_test:
                    yield [year, date_test, price_test, line]


def find_chase_purchases(input_glob):
    date_regex = r"^([0-9]{2}\/[0-9]{2})"
    price_regex = r"\s([0-9]{1,5}\.[0-9]{2})$"
    for [year, date_test, price_test, line] in find_purchases(
        input_glob, date_regex, price_regex
    ):
        yield Purchase.sanitize(
            date=datetime.strptime(f"{date_test[0]}/{year}", "%m/%d/%Y"),
            vendor_name=re.sub(date_regex, "", re.sub(price_regex, "", line)),
            cost=price_test[0],
        )


def find_barclays_purchases(input_glob):
    date_regex = r"^([A-Z][a-z]{2}\s[0-9]{2})"
    price_regex = r"\s\$([0-9]{1,5}\.[0-9]{2})$"
    for [year, date_test, price_test, line] in find_purchases(
        input_glob, date_regex, price_regex
    ):
        vendor = re.sub(
            price_regex,
            "",
            re.sub(date_regex, "", re.sub(date_regex, "", line).strip()),
        )
        yield Purchase.sanitize(
            date=datetime.strptime(f"{date_test[0]} {year}", "%b %d %Y"),
            vendor_name=vendor,
            cost=price_test[0],
        )


class Command(BaseCommand):
    help = "Perform OCR and extract purchases from PDFs"

    def add_arguments(self, parser):
        parser.add_argument(
            "--sources", help="Glob of PDFs", default="/opt/btk/pdf/*.pdf"
        )

    def handle(self, *args, **options):
        temp_dir = "/tmp/btk"
        os.makedirs(temp_dir, exist_ok=True)

        process_pdfs(options["sources"], temp_dir)
        process_jpgs(f"{temp_dir}/*.jpg", temp_dir)

        for purchase in chain(
            find_chase_purchases(f"{temp_dir}/chase*.txt"),
            find_barclays_purchases(f"{temp_dir}/barclays*.txt"),
        ):
            purchase.save()
