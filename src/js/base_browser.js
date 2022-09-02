const puppeteer = require('puppeteer');


async function openBaseBrowser() {
    const headless = process.env.headless;
    let option = {}
    option.headless = headless === "True";
    const browser = await puppeteer.launch({
        // 是否运行浏览器无头模式(boolean)
        headless: option.headless,
        // 设置浏览器大小
        defaultViewport: {width: 1366, height: 768},
        // defaultViewport: null,
        // 启动参数
        args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-cache', '--no-first-run', '--disable-application-cache'],
        // 是否自动打开调试工具(boolean)，若此值为true，headless自动置为false
        devtools: false,
        // 设置超时时间(number)，若此值为0，则禁用超时
        timeout: 20000,
    });
    const page = (await browser.pages())[0];
    return {browser, page}
}


module.exports = {openBaseBrowser}

