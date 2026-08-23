import asyncio
import random
import string
from playwright.async_api import async_playwright, Playwright

async def run(playwright: Playwright):
    chromium = playwright.chromium
    browser = await chromium.launch(headless=False, args=["--start-maximized"])
    page = await browser.new_page(no_viewport=True)
    await page.goto("https://accounts.google.com")
    
    def name():
        nameLength = 5;
        firstName = ''.join(random.choices(string.ascii_letters, k=nameLength));
        
        passwordLength = 14;
        passwordCharacters = string.ascii_letters + string.digits + string.punctuation;
        password = ''.join(random.choices(passwordCharacters, k=passwordLength));
        
        userLength = 12;
        userName = ''.join(random.choices(string.ascii_letters + string.digits, k=userLength))
        
        
        phoneNumber = ""
        email = ""
        
        
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
        days = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28];
        years = [1965,1966,1967,1968,1969,1970,1971,1972,1973,1974,1975,1976,1977,1978,1979,1980,1981,1982,1983,1984,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005];
        genders = ["Female", "Male", "Rather not say"]
        
        #i forgot to write the days and years as string, im too lazy to rewrite them
        stringDays = list(map(str, days))
        stringYears = list(map(str, years))
        
        #''.join is important because random.choices() returns a list
        month = ''.join(random.choices(months, k=1)) 
        day = ''.join(random.choices(stringDays, k=1)) 
        year = ''.join(random.choices(stringYears, k=1))
        gender = ''.join(random.choices(genders, k=1))  
        
        
        return firstName, password, userName, month, day, year, gender;
    
    firstName, password, userName, month, day, year, gender = name();
    
    
    await page.locator("div.n3Clv").click()
    await page.locator("span.VfPpkd-StrnGf-rymPhb-b9t22c", has_text="For my personal use").click()
    await page.locator("input#firstName").fill(firstName)
    await page.locator("div#collectNameNext").click()
    await page.locator("div#month").click()
    await page.locator(f'span:text-is("{month}")').click(force=True) #has_text matches with all parent elements that contain the element with the text. Using :text-is ensures that it only matches with the specific element that contains the specified text. For some weird reason it wasn't able to click even though i was certain i had chosen the correct element, setting force=True fixed it
    await page.locator("input#day").fill(day)
    await page.locator("input#year").fill(year)
    await page.locator("div#gender").click()
    await page.locator(f'#gender span:text-is("{gender}")').click(force=True) #there were two different spans with the same text. One had the ID gender and the other one had genderpronoun. Our element didn't have a unique ID so it automatically gets assigned the ID of the closest ancestor that has a unique ID. The ancestor had the ID gender so i added #gender to the locator 
    await page.locator("div#birthdaygenderNext").click()
    await page.locator("button:text-is(\"Don't have an email address or phone number?\")").click()
    await page.locator("div#selectionc24").click() # This part was tricky because i used my firefox browser to inspect the elements. In my browser, the div element with ID selectionc22 was assigned to "Create your own Gmail address" but in my script i noticed that it selected the first option instead. I decided to run the script and inspect the elements from the chromium browser instead, it turned out that in the chromium browser, the div element with ID selectionc24 was assigned to "Create your own Gmail address"
    await page.locator("input.whsOnd.zHQkBf").fill(userName) #if the element class has a space, seperate them by a dot in the selector, do not seperate them by a space
    await page.locator("div#next").click()
    await page.locator('[aria-label="Password"]').fill(password) # await page.locator('[aria-label="Confirm"]').fill(password) is better than await page.get_by_label("Password").fill(password) because aria-label="Confirm" ONLY filters for a matching aria-label while get_by_label filters for any type of lable, including aria-labelledby. Why is filtering by all labels bad? because we want to narrow down the filtering to the specific target element, get_by_label matched with an additional element.  
    await page.locator('[aria-label="Confirm"]').fill(password)
    
    
    
    
    #await page.locator("input#emailPhone").fill(userName)
    
    await asyncio.to_thread(input, "Press Enter to close the browser...");
    
    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)

asyncio.run(main())