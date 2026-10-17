"""Export the top TikTok ads of a market (TikTok Creative Center Top Ads) to CSV.

Usage: python example.py --country US --period 30 --order ctr --limit 100 [--industry Skincare] [--keyword serum] [--details]
"""
import argparse
import csv
import os
import sys

from apify_client import ApifyClient

ACTOR = "lagenuina_agency/tiktok-top-ads-scraper"
TOKEN = os.environ.get("APIFY_TOKEN")
if not TOKEN:
    sys.exit("Set APIFY_TOKEN first: https://console.apify.com/settings/integrations")

FIELDS = ["rank", "adId", "adTitle", "brandName", "ctr", "likes", "costScore", "industryName", "objectiveKey",
          "durationSec", "landingPageUrl", "keywords", "videoUrl720p", "coverUrl", "detailUrl"]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--country", default="US", help="two-letter code, e.g. US, GB, DE, IT")
    p.add_argument("--period", default="30", choices=["7", "30", "180"])
    p.add_argument("--order", default="for_you", help="for_you, impression, ctr, play_2s_rate, play_6s_rate, cvr, like")
    p.add_argument("--industry", default="", help="Creative Center industry name, e.g. Skincare")
    p.add_argument("--keyword", default="")
    p.add_argument("--limit", type=int, default=100)
    p.add_argument("--details", action="store_true", help="add landing page and ad keywords")
    a = p.parse_args()

    client = ApifyClient(TOKEN)
    run_input = {"countryCode": a.country, "period": a.period, "orderBy": a.order,
                 "keyword": a.keyword, "maxItems": a.limit, "extractDetails": a.details}
    if a.industry:  # leave it out for all industries
        run_input["industry"] = a.industry
    run = client.actor(ACTOR).call(run_input=run_input)
    out = f"tiktok_top_ads_{a.country}_{a.period}d.csv"
    n = 0
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        for ad in client.dataset(run["defaultDatasetId"]).iterate_items():
            w.writerow({**ad, "keywords": " | ".join(ad.get("keywords") or [])})
            n += 1
    print(f"{n} ads -> {out}")


if __name__ == "__main__":
    main()
