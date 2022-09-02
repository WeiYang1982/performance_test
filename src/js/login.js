require('dotenv').config();


async function login(passContext) {

    const {browser, page} = passContext;
    let login_url = process.env.base_url + "/config-center/login";
    // waitUntil对应的参数如下：
    // load - 页面的load事件触发时
    // domcontentloaded - 页面的 DOMContentLoaded 事件触发时
    // networkidle0 - 不再有网络连接时触发（至少500毫秒后）
    // networkidle2 - 只有2个网络连接时触发（至少500毫秒后）
    await page.goto(login_url, {waitUntil: 'networkidle0'});
    // 开启企业内部登录时，选择系统账号登录
    try {
        await page.click("input[type=radio][value='0']")
    }catch (e) {
        console.warn("尝试使用系统用户登录")
        console.warn(e)
    }
    const username = process.env.username;
    const password = process.env.password;
    await page.type('input[class=ant-input][type=text]', username)
    await page.type('input[class=ant-input][type=password]', password)
    // await page.click('button[type=\'submit\']', {waitUntil: 'networkidle0'})
    // 统一使用回车键进行登录
    await page.keyboard.press('Enter')
    // 等待页面加载完毕
    await page.waitForNavigation({waitUntil: 'networkidle0',});
}

module.exports = {login}