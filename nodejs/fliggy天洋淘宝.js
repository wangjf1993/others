const puppeteer = require("puppeteer");


const url = "https://hotel.fliggy.com/hotel_list3.htm?cityName=%B1%B1%BE%A9&city=&keywords=&checkIn=2019-05-15&checkOut=2019-05-16";

//登陆相关
const LOGIN_FLAG = "#J_Quick2Static";
const username = "15972114563";
const password = "taobao950798";

const LOGIN_USERNAME = "#TPL_username_1";
const LOGIN_PASSWORD = "#TPL_password_1";
const LOGIN_SUBMIT = "#J_SubmitStatic";
const login = async function (page) {
    await page.click(LOGIN_FLAG);
    await page.click(LOGIN_USERNAME);
    await page.type(LOGIN_USERNAME, username, {delay: 31});
    await page.waitFor(1300);
    await page.click(LOGIN_PASSWORD);
    await page.type(LOGIN_PASSWORD, password, {delay: 67});
    await page.waitFor(800);

    //过验证
    await pass_checking(page);



};

const pass_checking = async function (page) {
    const LOGIN_CHECK = "#nc_1_n1z";
    if (await page.$(LOGIN_CHECK)!=null) {
        let times = 0;
        while (!await login_check(page) && times < 3) {
            await page.waitFor(1000);
            await times++;
        }
    }
    await page.click(LOGIN_SUBMIT);
    await page.waitFor(1000);
    //存在二次校验的情况
    if (await page.$(LOGIN_CHECK)!=null) {
        let times = 0;
        while (!await login_check(page) && times < 3) {
            await page.waitFor(1000);
            await times++;
        }
    }
};


const login_check = async function (page) {
    try {
        const block_selector = "#nc_1_n1z";
        //预置检测
        let element = await page.$(block_selector);
        const point = await element.boundingBox();
        await page.mouse.move(point.x, point.y);
        await page.mouse.down();
        await page.mouse.move(point.x + 13, point.y);
        await page.mouse.move(point.x + 39, point.y);
        await page.mouse.move(point.x + 51, point.y);
        await page.mouse.move(point.x + 74, point.y);
        await page.mouse.move(point.x + 95, point.y);
        await page.mouse.move(point.x + 113, point.y);
        await page.mouse.move(point.x + 123, point.y);
        await page.mouse.move(point.x + 139, point.y);
        await page.mouse.move(point.x + 182, point.y);
        await page.mouse.move(point.x + 201, point.y);
        await page.mouse.move(point.x + 220, point.y);
        await page.mouse.move(point.x + 261, point.y);
        await page.mouse.move(point.x + 272, point.y);
        await page.mouse.move(point.x + 294, point.y);
        await page.mouse.move(point.x + 343, point.y);
        await page.mouse.up();
        await page.waitFor(1000);
    } catch (e) {
        return false;
    }
    return true;
};


//主流程
(async function () {
    let browser = await puppeteer.launch({
        ignoreHTTPSErrors: true,
        headless: false,
        ignoreDefaultArgs: true
    });
    let page = await browser.newPage();
    await page.goto(url);
    await login(page);
	await login(page);
})();
