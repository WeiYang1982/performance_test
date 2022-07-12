require('dotenv').config();
const lighthouse = require('lighthouse');
const fs = require('fs');
const driver = require("./base_browser");
const login = require("./login");
const reporter = require("./generate_report");
const {throttling} = require("lighthouse/lighthouse-core/config/constants");
const path = require("path");


async function test_performance(name, url) {
    const passContext = await driver.openBaseBrowser();
    const {browser, page} = passContext;
    await login.login(passContext);
    let test_url = process.env.base_url + url;
    // await page.goto(test_url, {waitUntil: 'networkidle0'});
    await page.waitForNetworkIdle();
    const report = await lighthouse(
        test_url,
        {
            port: (new URL(browser.wsEndpoint())).port,
            output: 'json',
            logLevel: 'info',
            disableDeviceEmulation: true
        },
        {
            extends: 'lighthouse:default',
            settings: {
                locale: 'zh', //  国际化
                formFactor: 'desktop', // 桌面
                screenEmulation: {
                    mobile: false,
                    width: 1366,
                    height: 768,
                    deviceScaleFactor: 1,
                    disabled: false,
                },
                throttling : throttling.desktopDense4G, // 设置网络限速
            },
        }
    );
    let result = reporter.generateReport(report);
    const filepath = path.join(__dirname, "../../report/collect_json/");
    try {
        fs.accessSync(filepath, {recursive: true});
    } catch (err) {
        fs.mkdirSync(filepath, {recursive: true});
    }
    const filename = path.join(filepath, name + ".json");
    fs.writeFileSync(filename, JSON.stringify(result));
    console.log(JSON.stringify(result));
    await browser.close();
    return JSON.stringify(result);
}


module.exports.init = function (name, url){
    let result = test_performance(name, url);
    console.log(result);
    return result;
}

// (async () => {
//
//     let url = "/webapp/tasklist/agency";
//     const re = test_performance(url);
//     console.log(re);
// })();