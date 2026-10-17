# TikTok Top Ads API – working example (Python, JS, n8n)

Export the best-performing TikTok ads from the **TikTok Creative Center Top Ads** page – ad copy, brand, CTR, likes, budget level, industry, objective, MP4 video URLs, cover image, landing page and ad keywords – to CSV or JSON. Filter by country, period (7/30/180 days), industry, campaign objective, ad language, Spark Ads and keyword.

Powered by the [tiktok-top-ads-scraper](https://apify.com/lagenuina_agency/tiktok-top-ads-scraper) actor on Apify. No browser, no TikTok account, no login.

## Example output (real result, shortened)

```json
{
  "rank": 2,
  "adId": "7680863927458562066",
  "adTitle": "It's still summer: 30% off",
  "brandName": "hesperia",
  "ctr": 0.45,
  "likes": 4246,
  "costScore": 2,
  "industryName": "Hotels & Accommodation",
  "objectiveKey": "campaign_objective_conversion",
  "durationSec": 15.019,
  "countryCode": "IT",
  "periodDays": 30,
  "landingPageUrl": "https://www.hesperia.com/en/offers/its-still-summer/?utm_source=tiktok&utm_medium=paid",
  "videoUrl720p": "https://v16m-default.tiktokcdn.com/.../video/tos/...",
  "detailUrl": "https://ads.tiktok.com/business/creativecenter/topads/7680863927458562066/pc/en?countryCode=IT&period=30"
}
```

## Quickstart (3 steps)

1. Create a free Apify account and copy your API token from [Settings → Integrations](https://console.apify.com/settings/integrations).
2. Put it in an environment variable (never in code): `export APIFY_TOKEN=your_token`
3. Run the example:

```bash
pip install -r python/requirements.txt
python python/example.py --country US --period 30 --order ctr --limit 100 --details
```

JavaScript: `cd js && npm install && node example.mjs US`

## Examples

**Python** (`pip install "apify-client<2"`)

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("lagenuina_agency/tiktok-top-ads-scraper").call(run_input={
  "countryCode": "US",
  "period": "30",
  "orderBy": "ctr",
  "industry": "Skincare",
  "maxItems": 100
})
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item["adTitle"], item["ctr"], item["videoUrl720p"])
```

**JavaScript / Node.js** (`npm install apify-client`)

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('lagenuina_agency/tiktok-top-ads-scraper').call({ countryCode: 'US', period: '7', orderBy: 'ctr', maxItems: 20 });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

**cURL / any language** – one HTTP call, results in the response:

```bash
curl -X POST "https://api.apify.com/v2/acts/lagenuina_agency~tiktok-top-ads-scraper/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"countryCode": "GB", "period": "30", "keyword": "skincare", "maxItems": 50, "extractDetails": true}'
```

All input fields are documented on the [actor page](https://apify.com/lagenuina_agency/tiktok-top-ads-scraper) (Input tab).

## Use case: TikTok ad spy swipe file in CSV

`python/example.py` collects the top ads of one market and writes `tiktok_top_ads_<country>_<period>d.csv` with rank, ad copy, brand, CTR, likes, budget level, industry, objective, landing page, ad keywords, MP4 link and Creative Center link – ready for Excel or Google Sheets. Video links expire after a day or two: download the MP4s you want to keep right away.

## n8n workflow

[`n8n/workflow.json`](n8n/workflow.json): every Monday 08:00 → run the actor (top 100 US ads of the last 7 days by CTR, with landing pages) → keep the main fields with a Set node → append to Google Sheets.

1. In n8n: **Workflows → Import from File** and pick `n8n/workflow.json`.
2. Create a **Header Auth** credential named `Apify API token` with name `Authorization` and value `Bearer <your token>`, and select it in the *Run Apify actor* node.
3. Edit the JSON body (country, industry, keyword), set your Google Sheet ID and activate.

The `run-sync-get-dataset-items` endpoint waits up to 300 s; for bigger runs use `/runs` plus a webhook.

## Use with AI agents (MCP)

Give Claude, ChatGPT, Cursor or any MCP client this actor as a tool:

```
https://mcp.apify.com/?actors=lagenuina_agency/tiktok-top-ads-scraper
```

Example config (Claude Desktop, Cursor, VS Code):

```json
{
  "mcpServers": {
    "tiktok-top-ads-scraper": {
      "url": "https://mcp.apify.com/?actors=lagenuina_agency/tiktok-top-ads-scraper"
    }
  }
}
```

Sign in with Apify OAuth when asked, or send `Authorization: Bearer <APIFY_TOKEN>`.

## Pricing

$0.80 per 1,000 ads on every Apify plan, plus $1.60 per 1,000 when you turn on full details (landing page, keywords, tags). No start fee, pay only for results – see [lagenuina_agency/tiktok-top-ads-scraper](https://apify.com/lagenuina_agency/tiktok-top-ads-scraper).

## More tools from Quelli di Carne Genuina

- **Ad intelligence:** [Google Ads Transparency](https://github.com/assa83/google-ads-transparency-api) · [Meta Ad Library](https://github.com/assa83/facebook-ad-library-api) · [LinkedIn Ad Library](https://github.com/assa83/linkedin-ad-library-api)
- **Competitor & SEO research:** [Similarweb traffic](https://github.com/assa83/similarweb-traffic-api) · [Google Trends](https://github.com/assa83/google-trends-api-python) · [Google Play](https://github.com/assa83/google-play-scraper-api)
- **Travel prices:** [Google Hotels](https://github.com/assa83/google-hotels-prices-api) · [Google Flights](https://github.com/assa83/google-flights-api)
- **Retail prices:** [Woolworths & Coles](https://github.com/assa83/australian-supermarket-prices-api)
- **Content & social data:** [YouTube Transcript](https://github.com/assa83/youtube-transcript-scraper-api) · [Medium](https://github.com/assa83/medium-scraper-api) · [Likee](https://github.com/assa83/likee-scraper-api)

All actors: [apify.com/lagenuina_agency](https://apify.com/lagenuina_agency) · Tutorials: [assa83.github.io](https://assa83.github.io)

## Disclaimer

Independent, not affiliated with TikTok or ByteDance. It reads only publicly available data from TikTok Creative Center. Use it in line with the applicable terms and laws, including the copyright of the creatives.

## License

[MIT](LICENSE) © Quelli di Carne Genuina
