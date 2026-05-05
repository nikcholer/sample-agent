from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "samples" / "data" / "sales_orders.csv"
SEED = 20260505


@dataclass(frozen=True)
class Product:
    category: str
    name: str
    base_price: int
    margin_rate: float


REGIONS = {
    "EMEA": ["UK", "Ireland", "Germany", "France", "Netherlands"],
    "Americas": ["USA", "Canada", "Brazil"],
    "APAC": ["Japan", "Australia", "Singapore"],
}

PRODUCTS = [
    Product("Software", "Analytics Suite", 420, 0.62),
    Product("Software", "Forecast Pro", 360, 0.58),
    Product("Software", "Pipeline IQ", 290, 0.55),
    Product("Hardware", "Field Tablet", 680, 0.31),
    Product("Hardware", "Demo Kiosk", 1450, 0.28),
    Product("Hardware", "Sensor Hub", 760, 0.34),
    Product("Services", "Enablement Workshop", 2400, 0.46),
    Product("Services", "Premium Support", 1800, 0.52),
    Product("Services", "Data Migration", 3200, 0.43),
]

CUSTOMERS = [
    "Northstar Retail",
    "Clearline Manufacturing",
    "Bluepeak Logistics",
    "Summit Foods",
    "Cedar Finance",
    "Aster Health",
    "Redwood Energy",
    "Harbor Telecom",
    "Brightlane Travel",
    "Oakfield Distribution",
    "Silvergate Media",
    "Greenbridge Services",
]

SALESPEOPLE = {
    "EMEA": ["Amira Shah", "Luca Moretti", "Nora Hughes", "Tomas Berger"],
    "Americas": ["Diego Lopez", "Maya Brooks", "Noah Reed"],
    "APAC": ["Eva Chen", "Kenji Sato", "Priya Nair"],
}

SEGMENTS = ["Enterprise", "Mid-Market", "SMB"]
CHANNELS = ["Direct", "Partner", "Online"]


def month_starts() -> list[date]:
    months: list[date] = []
    year, month = 2025, 1
    while (year, month) <= (2026, 4):
        months.append(date(year, month, 1))
        month += 1
        if month == 13:
            year += 1
            month = 1
    return months


def main() -> None:
    rng = random.Random(SEED)
    rows: list[dict[str, object]] = []
    counter = 1

    for month_start in month_starts():
        for region, countries in REGIONS.items():
            for country in countries:
                for _ in range(3):
                    product = rng.choice(PRODUCTS)
                    units = rng.randint(6, 180)
                    segment = rng.choice(SEGMENTS)
                    segment_multiplier = {
                        "Enterprise": 1.35,
                        "Mid-Market": 1.0,
                        "SMB": 0.72,
                    }[segment]
                    channel = rng.choice(CHANNELS)
                    channel_multiplier = {
                        "Direct": 1.08,
                        "Partner": 0.96,
                        "Online": 0.88,
                    }[channel]
                    price_noise = rng.uniform(0.92, 1.12)
                    revenue = round(
                        units
                        * product.base_price
                        * segment_multiplier
                        * channel_multiplier
                        * price_noise,
                        2,
                    )
                    margin_noise = rng.uniform(0.94, 1.06)
                    gross_margin = round(revenue * product.margin_rate * margin_noise, 2)
                    order_date = month_start.replace(day=rng.randint(1, 28))

                    rows.append(
                        {
                            "order_id": f"SO-{order_date:%Y%m}-{counter:04d}",
                            "order_date": order_date.isoformat(),
                            "region": region,
                            "country": country,
                            "customer_segment": segment,
                            "product_category": product.category,
                            "product_name": product.name,
                            "customer_name": rng.choice(CUSTOMERS),
                            "salesperson": rng.choice(SALESPEOPLE[region]),
                            "channel": channel,
                            "revenue": f"{revenue:.2f}",
                            "gross_margin": f"{gross_margin:.2f}",
                            "units": units,
                        }
                    )
                    counter += 1

    rows.sort(key=lambda row: (row["order_date"], row["order_id"]))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "order_id",
                "order_date",
                "region",
                "country",
                "customer_segment",
                "product_category",
                "product_name",
                "customer_name",
                "salesperson",
                "channel",
                "revenue",
                "gross_margin",
                "units",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUTPUT}")


if __name__ == "__main__":
    main()
