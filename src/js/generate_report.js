require('dotenv').config();
const path = require('path');
const fs = require('fs');
const url = require("url");
const reportGenerator = require("lighthouse/report/generator/report-generator");


const metrics = ["first-contentful-paint", "speed-index", "largest-contentful-paint", "total-blocking-time", "cumulative-layout-shift", "interactive"]
const record = {};


function generateReport(runnerResult) {
    const requestedUrl = runnerResult.lhr.requestedUrl;
    const filename = url.parse(requestedUrl, true).pathname.replaceAll("/", "_") + ".html";
    const filepath = path.join(__dirname, "../../report/collect_json");
    try {
        fs.accessSync(filepath, {recursive: true});
    } catch (err) {
        fs.mkdirSync(filepath, {recursive: true});
    }
    const htmlReportPath = path.join(__dirname, "../../report/collect_json", filename);
    // const htmlReportPath = path.join(filepath, filename);
    const htmlReport = reportGenerator.generateReport(runnerResult.lhr, 'html');
    fs.writeFileSync(htmlReportPath, htmlReport);
    const categories = Object.values(runnerResult.lhr.categories);
    for (let i = 0; i < categories.length; i += 1) {
        const key = `${categories[i].title}`;
        record[key] = categories[i].score;
    }
    metrics.forEach(value => record[value] = runnerResult.lhr.audits[value].numericValue);
    return record;
}


module.exports = {generateReport}


// (async () => {
//     const pr_dir = "D:\\Code\\python_project\\performance_test";
//     const all_dir = "../../report/collect_json";
//     try {
//         fs.accessSync(all_dir, {recursive: true});
//     } catch (err) {
//         fs.mkdirSync(all_dir, {recursive: true});
//     }
// })();