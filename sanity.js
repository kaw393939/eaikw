// sanity.js
const sanityClient = require("@sanity/client");

module.exports = sanityClient({
  projectId: "546tpjxi",   // from sanity.cli.js
  dataset: "production",          // default dataset
  apiVersion: "2025-12-01",       // use a fixed date
  useCdn: true                    // `true` for cached, fast reads
});
