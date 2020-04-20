#!/usr/bin/env python3

import logging
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from glob import glob
from itertools import chain
from operator import itemgetter

import pyocr
import pyocr.builders
from money import Money
from pdf2image import convert_from_path
from PIL import Image

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

year_pattern = re.compile(r"[0-9]{2}_([0-9]{4})")


@dataclass
class Purchase:
    date: datetime
    vendor: str
    cost: Money

    def __init__(self, date, vendor, cost):
        self.date = date
        # Strip digits for better coalescing
        self.vendor = re.sub(r"([0-9]+)", "", vendor.strip())
        self.cost = Money(amount=cost, currency="USD")


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
        yield Purchase(
            datetime.strptime(f"{date_test[0]}/{year}", "%m/%d/%Y"),
            re.sub(date_regex, "", re.sub(price_regex, "", line)),
            price_test[0],
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
        yield Purchase(
            datetime.strptime(f"{date_test[0]} {year}", "%b %d %Y"),
            vendor,
            price_test[0],
        )


def cost_by_vendor(purchases):
    unique_vendors = {}
    for purchase in purchases:
        subtotal = unique_vendors.get(
            purchase.vendor, Money(amount="0", currency=purchase.cost.currency)
        )
        unique_vendors[purchase.vendor] = subtotal + purchase.cost
    for vendor, cost in sorted(unique_vendors.items(), key=itemgetter(1)):
        yield vendor, cost


def cost_by_currency(purchases):
    total = {}
    for purchase in purchases:
        c = purchase.cost.currency
        total[c] = total.get(c, Money(amount="0", currency=c)) + purchase.cost
    for currency, cost in total.items():
        yield currency, cost


def main():
    temp_dir = "/tmp/btk"
    os.makedirs(temp_dir, exist_ok=True)

    process_pdfs(f"/opt/btk/pdf/*.pdf", temp_dir)
    process_jpgs(f"{temp_dir}/*.jpg", temp_dir)

    purchases = list(
        chain(
            find_chase_purchases(f"{temp_dir}/chase*.txt"),
            find_barclays_purchases(f"{temp_dir}/barclays*.txt"),
        )
    )
    for vendor, cost in cost_by_vendor(purchases):
        logger.info("%s %8.2f %s:", cost.currency, cost.amount, vendor)
    for currency, total in cost_by_currency(purchases):
        logger.info("%s %8.2f ==∙∙=== TOTAL ===∙∙==", currency, total)


if __name__ == "__main__":
    sys.exit(main())
