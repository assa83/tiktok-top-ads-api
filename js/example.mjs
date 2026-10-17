// Highest-CTR TikTok ads of the last 7 days in a country, with MP4 links.
// Usage: node example.mjs US
import { ApifyClient } from 'apify-client';

const token = process.env.APIFY_TOKEN;
if (!token) {
    console.error('Set APIFY_TOKEN first: https://console.apify.com/settings/integrations');
    process.exit(1);
}

const countryCode = process.argv[2] ?? 'US';
const client = new ApifyClient({ token });
const run = await client.actor('lagenuina_agency/tiktok-top-ads-scraper').call({
    countryCode,
    period: '7',
    orderBy: 'ctr',
    maxItems: 20,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const ad of items) {
    console.log(`#${ad.rank}  CTR ${ad.ctr}  ${ad.likes} likes  ${ad.brandName || '-'}  ${ad.adTitle}\n    ${ad.videoUrl720p ?? ad.coverUrl}`);
}
