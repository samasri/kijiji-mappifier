import config from "config";
import { search } from "kijiji-scraper";
import { appendFileSync, readFileSync, writeFileSync } from "fs";
import pMap from "p-map";

const locationIQToken = config.get("locationIQToken");
const leafletJsToken = config.get("leafletJsToken");

const scrape = async () => {
  const categoryId = 37; // houses
  const locationId = 1700273; // Greater Toronto Area

  const rawAds = await search(
    {
      locationId,
      categoryId,
    },
    {
      maxResults: 5000,
    }
  );

  const ads = rawAds.map((ad) => {
    const { title, description, attributes, url } = ad;
    const { price, location } = attributes;
    return {
      title,
      description,
      price,
      location,
      url,
    };
  });

  // In case of an error, make sure we don't have to rescrape kijiji
  writeFileSync("./temp.ads", JSON.stringify(ads));
  return ads;
};

const url = (query) =>
  new URL(
    `https://us1.locationiq.com/v1/search?key=${locationIQToken}&q=${query}&format=json`
  );

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const processAds = async (ads) => {
  if (!ads) {
    const rawAds = readFileSync("./temp.ads");
    ads = JSON.parse(rawAds);
  }
  console.log(`Processing ${ads.length} ads...`);

  const processedAds = [];

  await pMap(
    ads,
    async (ad) => {
      await sleep(1000); // Location IQ only allows 60 requests per minute for the free tier
      const resp = await fetch(url(ad.location));
      const locations = await resp.json();
      if (locations.length === 0) return;
      if (locations.error) {
        appendFileSync("./temp.errors", `${JSON.stringify(ad)},\n`);
        return;
      }
      const { lat, lon } = locations[0]; // pick one with highest priority
      ad.location = { lat, lon };
      appendFileSync("./temp.processed.ads", `${JSON.stringify(ad)},\n`);
      processedAds.push(ad);
    },
    {
      concurrency: 1,
    }
  );
  writeFileSync(
    "../frontend/data.json",
    `const data = ${JSON.stringify(processedAds)};`
  );
};

const main = async () => {
  // empty temp files
  writeFileSync("temp.ads", "");
  writeFileSync("temp.processed.ads", "");
  writeFileSync("temp.errors", "");

  await processAds(await scrape());
  writeFileSync("../frontend/token.js", `let token = "${leafletJsToken}"`);
};

main().catch((err) => {
  throw err;
});
