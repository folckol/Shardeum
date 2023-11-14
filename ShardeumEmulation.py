import os
import random
import shutil
import time
import traceback
import pyperclip
import ua_generator
from ShardeumRequests import Shardeum
from utils.logger import logger
from playwright.sync_api import sync_playwright


class PWModel:

    def __init__(self, number, private=None, proxy=None):
        self.playwright = sync_playwright().start()

        self.number = number
        self.proxy = proxy
        self.privateKey = private

        EX_path = "MetaMask"

        user_data_dir = f"{os.getcwd()}\\dataDir"

        self.context = self.playwright.chromium.launch_persistent_context(user_data_dir,
                                                                          user_agent=ua_generator.generate(
                                                                              device="desktop", browser="chrome").text,
                                                                          proxy={
                                                                              "server": f"{proxy.split(':')[0]}:{proxy.split(':')[1]}",
                                                                              "username": f"{proxy.split(':')[2]}",
                                                                              "password": f"{proxy.split(':')[3]}",
                                                                          } if proxy != None else None, headless=False,
                                                                          devtools=False, args=[
                f'--load-extension={os.getcwd()}\\{EX_path}',
                f'--disable-extensions-except={os.getcwd()}\\{EX_path}'
                ])

        self.page = self.context.new_page()

        self.page.set_default_timeout(60000)

    def CreateNewWallet(self):
        # Открытие страницы Twitter
        self.page.goto('https://yandex.ru')
        self.page.wait_for_timeout(5000)

        # print(self.context.pages)

        self.MMPage = self.context.pages[-1]
        self.MMPage.bring_to_front()
        self.MMPage.reload()
        self.MMPage.wait_for_selector('input[id="onboarding__terms-checkbox"]').click()
        self.MMPage.wait_for_selector('button[data-testid="onboarding-create-wallet"]').click()
        self.MMPage.wait_for_selector('button[data-testid="metametrics-i-agree"]').click()
        self.MMPage.wait_for_selector('input[data-testid="create-password-new"]').fill('Passwordsdjeruf039fnreo')
        self.MMPage.wait_for_selector('input[data-testid="create-password-confirm"]').fill('Passwordsdjeruf039fnreo')
        self.MMPage.wait_for_selector('input[data-testid="create-password-terms"]').click()
        self.MMPage.wait_for_selector('button[data-testid="create-password-wallet"]').click()
        self.MMPage.wait_for_selector('button[data-testid="secure-wallet-later"]').click()
        self.MMPage.wait_for_selector('input[data-testid="skip-srp-backup-popover-checkbox"]').click()
        self.MMPage.wait_for_selector('button[data-testid="skip-srp-backup"]').click()
        self.MMPage.wait_for_selector('button[data-testid="onboarding-complete-done"]').click()
        self.MMPage.wait_for_selector('button[data-testid="pin-extension-next"]').click()
        self.MMPage.wait_for_timeout(1000)
        self.MMPage.wait_for_selector('button[data-testid="pin-extension-done"]').click()
        self.MMPage.wait_for_timeout(4000)
        self.MMPage.wait_for_selector('button[data-testid="popover-close"]').click()
        # self.MMPage.wait_for_timeout(1000)
        # self.MMPage.wait_for_selector('button[data-testid="popover-close"]').click()

        if self.privateKey == None:
            self.MMPage.wait_for_selector(
                'xpath=//*[@id="app-content"]/div/div[3]/div/div/div/div[1]/div/div/div/button').click()
            self.MMPage.wait_for_timeout(3000)
            self.address = pyperclip.paste()

            self.MMPage.wait_for_selector(
                'xpath=//*[@id="app-content"]/div/div[3]/div/div/div/div[1]/span/button/span').click()
            self.MMPage.wait_for_selector('xpath=//*[@id="popover-content"]/div[2]/button[2]').click()

            self.MMPage.wait_for_selector('xpath=//*[@id="app-content"]/div/span/div[1]/div/div/div/button[3]').click()
            self.MMPage.wait_for_selector(
                'xpath=//*[@id="app-content"]/div/span/div[1]/div/div/div/div[5]/div/input').fill(
                'Passwordsdjeruf039fnreo')
            self.MMPage.wait_for_selector(
                'xpath=//*[@id="app-content"]/div/span/div[1]/div/div/div/div[7]/button[2]').click()

            holdButton = self.MMPage.wait_for_selector(
                'xpath=//*[@id="app-content"]/div/span/div[1]/div/div/div/div[3]/button/span')
            holdButton.hover()
            self.MMPage.mouse.down()
            self.MMPage.wait_for_timeout(3000)
            self.MMPage.mouse.up()

            self.privateKey = '0x' + self.MMPage.wait_for_selector(
                'xpath=//*[@id="app-content"]/div/span/div[1]/div/div/div/div[5]/div').text_content()
            self.MMPage.wait_for_selector(
                'xpath=//*[@id="app-content"]/div/span/div[1]/div/div/div/div[7]/button').click()


        else:

            self.MMPage.wait_for_timeout(1000)
            self.MMPage.wait_for_selector('button[data-testid="account-menu-icon"]').click()
            self.MMPage.wait_for_selector('div.account-menu > button.account-menu__item.account-menu__item--clickable')
            self.MMPage.query_selector_all(
                'div.account-menu > button.account-menu__item.account-menu__item--clickable')[1].click()
            self.MMPage.wait_for_selector('input[id="private-key-box"]').fill(self.privateKey)
            self.MMPage.wait_for_selector('xpath=//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/button[2]').click()
            self.MMPage.wait_for_selector('button[data-testid="eth-overview-send"]')

            self.MMPage.wait_for_selector(
                'xpath=//*[@id="app-content"]/div/div[3]/div/div/div/div[1]/div/div/div/button').click()
            self.address = pyperclip.paste()



    def AddNetwork(self):

        self.MMPage.goto("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#settings/networks/add-network")

        self.MMPage.wait_for_timeout(2000)
        self.MMPage.wait_for_selector('xpath=//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/label/input').fill("Shardeum Sphinx Dapp 1.X")
        self.MMPage.wait_for_selector('xpath=//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/label/input').fill("https://dapps.shardeum.org")
        self.MMPage.wait_for_selector('xpath=//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[3]/label/input').fill("8081")
        self.MMPage.wait_for_selector('xpath=//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[4]/label/input').fill("SHM")
        self.MMPage.wait_for_selector('xpath=//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[2]/div[5]/label/input').fill("https://explorer-dapps.shardeum.org")

        self.MMPage.wait_for_timeout(2000)
        self.MMPage.wait_for_selector('xpath=//*[@id="app-content"]/div/div[3]/div/div[2]/div[2]/div/div[2]/div/div[3]/button[2]').click()

        self.MMPage.wait_for_timeout(2000)
        self.MMPage.wait_for_selector(
            'xpath=//*[@id="popover-content"]/div/div/section/div/div/button[1]').click()

        self.MMPage.wait_for_timeout(5000)



    def DotshmMintDomen(self):

        self.page.bring_to_front()
        self.page.goto("https://dotshm.me/")

        self.page.wait_for_selector('xpath=//*[@id="__next"]/div/main/div[2]/div/div/div/input').fill(self.address)
        self.page.wait_for_selector('button[id*="headlessui-menu"]').click()

        self.SpecialConnect('p.flex.items-center.justify-center')

        self.page.wait_for_selector('button[id*="headlessui-listbox-button"]').click()
        self.page.wait_for_timeout(3000)
        self.page.query_selector_all('li[id*="headlessui-listbox-option-"]')[-1].click()

        self.page.wait_for_timeout(7000)

        self.page.wait_for_selector('xpath=//*[@id="__next"]/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div/button').click()

        self.page.wait_for_timeout(6000)
        self.page.wait_for_selector('img[src="/images/wallets/metamask.svg"]').click()

        self.page.wait_for_timeout(6000)
        self.page.wait_for_selector('xpath=//*[@id="__next"]/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div/button').click()

        self.ConfirmTransaction('button.w-full.my-3.text-white.capitalize.border-none')

        self.page.wait_for_timeout(random.randint(10000, 30000))

        # self.page.wait_for_selector('xpath=//*[@id="__next"]/div/header/div/div[2]/div/div').click()
        # self.ConnectWallet('xpath=//*[@id="headlessui-dialog-17"]/div/div[2]/div/div[2]/div[1]')

        logger.success(f"{self.number} | Domen Mint Success")




    def Spriyo(self):

        pages = len(self.context.pages)
        self.page.goto("https://www.spriyo.xyz/")

        _ = 0
        while pages == len(self.context.pages) and _ < 60:
            self.page.wait_for_timeout(1000)
            _ += 1

        if _ >= 60:
            raise Exception("Превышено время ожидания открытия страницы Метамаск")

        else:

            self.MMConfirmer = self.context.pages[-1]
            self.MMConfirmer.wait_for_selector('button.btn-primary.button').click()
            self.MMConfirmer.wait_for_timeout(3000)
            self.MMConfirmer.wait_for_selector('button.btn-primary.button').click()
            self.MMConfirmer.wait_for_timeout(3000)
            try:
                self.MMConfirmer.wait_for_selector('button[data-testid="page-container-footer-next"]', timeout=7000).click()
            except:
                pass

        self.page.wait_for_selector('xpath=//*[@id="root"]/div[1]/div[2]/div/div/div[1]/div/div/div[2]/div[5]/div').click()
        self.page.wait_for_timeout(1000)
        self.page.wait_for_selector('xpath=//*[@id="root"]/div[1]/div[2]/div/div[1]/div/div').click()

        self.page.wait_for_timeout(random.randint(1000,10000))
        self.page.wait_for_selector('input[placeholder="Enter your NFT title"]').fill(self.randomTitle)
        self.page.wait_for_timeout(random.randint(1000,10000))
        self.page.wait_for_selector('textarea').fill(self.randomDescription)
        self.page.wait_for_timeout(random.randint(5000,10000))

        try:
            self.page.set_input_files('input[type="file"]', self.randomFile)
            self.page.wait_for_timeout(random.randint(1000,10000))

            self.ConfirmTransaction('xpath=//*[@id="root"]/div[1]/div/div[2]/div[2]/div[5]/div')
        except:
            try:
                self.page.set_input_files('input[type="file"]', self.randomFile)
                self.page.wait_for_timeout(random.randint(1000, 10000))

                self.ConfirmTransaction('xpath=//*[@id="root"]/div[1]/div/div[2]/div[2]/div[5]/div')
            except:
                try:
                    self.page.set_input_files('input[type="file"]', self.randomFile)
                    self.page.wait_for_timeout(random.randint(1000, 10000))

                    self.ConfirmTransaction('xpath=//*[@id="root"]/div[1]/div/div[2]/div[2]/div[5]/div')
                except:

                    raise Exception("Не удалось установить картинку при создании NFT")


        logger.success(f"{self.number} | Create NFT Success")

        self.page.wait_for_timeout(3000)

    @property
    def randomTitle(self) -> str:
        adjectives = [
            "Red", "Blue", "Majestic", "Lonely", "Vibrant", "Mysterious", "Serene",
            "Ethereal", "Dynamic", "Gloomy", "Harmonious", "Infinite", "Radiant",
            "Surreal", "Ancient", "Charming", "Elegant", "Graceful", "Quaint",
            "Rustic", "Stunning", "Sublime", "Whimsical", "Dazzling", "Exquisite",
            "Magnificent", "Opulent", "Picturesque", "Timeless", "Captivating",
            "Enchanting", "Peaceful", "Breathtaking", "Luminous", "Translucent",
            "Mesmerizing", "Spellbinding", "Delightful", "Divine", "Idyllic",
            "Lavish", "Luxurious", "Poetic", "Splendid", "Striking", "Grandiose"
        ]
        nouns = [
            "Sunset", "Ocean", "Mountain", "Forest", "Sky", "River", "Moon",
            "Desert", "Prairie", "Lake", "Star", "Planet", "Galaxy", "Comet",
            "Meadow", "Island", "Beach", "Waterfall", "Cliff", "Volcano",
            "Canyon", "Fjord", "Cave", "Valley", "Gorge", "Summit",
            "Horizon", "Glacier", "Grove", "Plateau", "Lagoon", "Marsh",
            "Swamp", "Estuary", "Reef", "Jungle", "Archipelago", "Bay",
            "Dune", "Oasis", "Tundra", "Savannah", "Rainforest", "Woodland",
            "Hill", "Field", "Pond", "Brook", "Stream", "Fountain"
        ]
        return f"{random.choice(adjectives)} {random.choice(nouns)}"

    @property
    def randomDescription(self) -> str:
        beginnings = [
            "A stunning view of", "Witness the beauty of", "Experience the serenity of",
            "Get lost in", "Explore the tranquility of", "The majesty of", "Marvel at",
            "Behold the wonder of", "Discover the splendor of", "Feel the awe of",
            "Contemplate the grandeur of", "Soak in the loveliness of", "The allure of",
            "Bask in the glory of", "Immerse yourself in", "Indulge in the richness of",
            "Delight in", "The magic of", "Savor the elegance of", "Revel in",
            "The enchantment of", "Find peace in", "Experience the opulence of",
            "The simplicity of", "Find solace in", "The charm of", "Embrace the wonder of",
            "The sacred beauty of", "Engage with the allure of", "Immerse in the atmosphere of"
        ]

        adjectives = [
            "a tranquil", "an idyllic", "a majestic", "a breathtaking", "a serene",
            "an awe-inspiring", "a mesmerizing", "an exquisite", "a peaceful",
            "an elegant", "a sublime", "a vibrant", "an arresting", "an intriguing",
            "an enchanting", "a spellbinding", "a captivating", "a picturesque",
            "an evocative", "a poetic", "a dreamy", "a resplendent", "an ethereal",
            "a celestial", "a heavenly", "a lavish", "a timeless", "a romantic",
            "a dazzling", "an ostentatious"
        ]

        nouns = [
            "sunset", "ocean", "mountain range", "forest", "night sky", "river", "full moon",
            "desert", "waterfall", "meadow", "lake", "beach", "cave", "valley",
            "volcano", "snowfield", "dune", "savannah", "reef", "woodland",
            "fjord", "cliff", "canyon", "plateau", "tundra", "swamp", "prairie",
            "estuary", "lagoon", "archipelago"
        ]

        endings = [
            "awaits you.", "captures the imagination.", "is a feast for the eyes.",
            "will take your breath away.", "like you've never seen before.",
            "will touch your soul.", "is a natural wonder.", "is a paradise on Earth.",
            "beckons the wanderer.", "is an artist's dream.", "is the ultimate escape.",
            "is a sanctuary for the senses.", "offers a moment of reprieve.",
            "is a glimpse into heaven.", "will leave you speechless.",
            "is where dreams come to life.", "is poetry in motion.",
            "invokes a sense of wonder.", "is pure magic.", "is beyond words.",
            "is a sight to behold.", "is your next adventure.", "offers an ethereal experience.",
            "is where reality meets fantasy.", "is an ode to Mother Nature.",
            "is a hidden gem.", "is a true masterpiece.", "is an experience of a lifetime.",
            "is a moment frozen in time.", "is a journey for the soul."
        ]

        return f"{random.choice(beginnings)} {random.choice(adjectives)} {random.choice(nouns)} {random.choice(endings)}"

    @property
    def randomFile(self) -> str:
        return f'{os.getcwd()}/InputData/Media/{random.choice(os.listdir(f"{os.getcwd()}/InputData/Media"))}'.replace('/', '\\')

    def ConnectWallet(self, element):

        pages = len(self.context.pages)
        self.page.wait_for_selector(element).click()

        _ = 0
        while pages == len(self.context.pages) and _ < 60:
            self.page.wait_for_timeout(1000)
            _ += 1

        if _ >= 60:
            raise Exception("Превышено время ожидания открытия страницы Метамаск")

        else:

            self.MMConfirmer = self.context.pages[-1]
            self.MMConfirmer.wait_for_selector('button.btn-primary.button').click()
            self.MMConfirmer.wait_for_timeout(3000)
            self.MMConfirmer.wait_for_selector('button.btn-primary.button').click()
            self.MMConfirmer.wait_for_timeout(3000)
            try:
                self.MMConfirmer.wait_for_selector('button.btn-primary.button', timeout=5000).click()
            except:
                pass

    def ConfirmTransaction(self, element):

        pages = len(self.context.pages)
        self.page.wait_for_selector(element).click()

        _ = 0
        while pages == len(self.context.pages) and _ < 20:
            self.page.wait_for_timeout(1000)
            _ += 1

        if _ >= 20:
            raise Exception("Превышено время ожидания открытия страницы Метамаск")

        else:

            self.MMConfirmer = self.context.pages[-1]
            self.MMConfirmer.wait_for_selector('button[data-testid="page-container-footer-next"]').click()
            self.MMConfirmer.wait_for_timeout(3000)

    def SpecialConnect(self, element):

        pages = len(self.context.pages)
        self.page.wait_for_selector(element).click()

        _ = 0
        while pages == len(self.context.pages) and _ < 60:
            self.page.wait_for_timeout(1000)
            _ += 1

        if _ >= 60:
            raise Exception("Превышено время ожидания открытия страницы Метамаск")

        else:

            self.MMConfirmer = self.context.pages[-1]
            self.MMConfirmer.wait_for_selector('button.btn-primary.button').click()
            self.MMConfirmer.wait_for_timeout(3000)
            self.MMConfirmer.wait_for_selector('button[data-testid="page-container-footer-next"]').click()
            self.MMConfirmer.wait_for_timeout(3000)

    def Faucet(self):

        RM = Shardeum(self.address, self.proxy)
        status = RM.Faucet()
        # print(status)


    def close(self):
        self.playwright.stop()



if __name__ == '__main__':


    try:
        shutil.rmtree(f"{os.getcwd()}/dataDir")
    except:
        pass

    delay = (15, 30)


    proxies = []
    with open('InputData/Proxies.txt', 'r') as file:
        for i in file:
            proxies.append(i.rstrip())

    privates = []
    with open('InputData/Privates.txt', 'r') as file:
        for i in file:
            privates.append(i.rstrip())

    if len(proxies) != 0 and proxies[0] != "":

        logger.warning("Вы запустили скрипт с проксями")
        time.sleep(1)
        print('')

        for i in range(len(proxies)):

            try:
                shutil.rmtree(f"{os.getcwd()}/dataDir")
            except:
                pass

            try:
                model = PWModel(i + 1, privates[i] if len(privates) != 0 and privates[0] != "" else None, proxies[i])
                model.CreateNewWallet()
                model.AddNetwork()
                model.Faucet()

                model.DotshmMintDomen()
                model.Spriyo()


            except Exception as e:
                # traceback.print_exc()
                # model.page.wait_for_timeout(100000000)
                logger.error(f"{i + 1} | Произошла ошибка ({str(e)})")

            try:
                model.close()
            except:
                pass

            try:
                with open("result.txt", "a+") as file:
                    file.write(model.privateKey + '|' + proxies[i] + '\n')
            except:
                pass

            time.sleep(random.randint(delay[0], delay[1]))
            print('')

    else:

        logger.warning("Вы запустили скрипт без проксей")
        time.sleep(5)
        print('')

        c = 0
        while True:

            try:
                shutil.rmtree(f"{os.getcwd()}/dataDir")
            except:
                pass

            try:
                model = PWModel(c + 1, privates[c] if len(privates) != 0 and privates[0] != "" else None)
                model.CreateNewWallet()
                model.AddNetwork()
                model.Faucet()

                model.DotshmMintDomen()
                model.Spriyo()

            except Exception as e:
                # traceback.print_exc()
                # model.page.wait_for_timeout(100000000)
                logger.error(f"{c + 1} | Произошла ошибка ({str(e)})")

            try:
                model.close()
            except:
                pass

            try:
                with open("result.txt", "a+") as file:
                    file.write(model.privateKey + '|' + proxies[i] + '\n')
            except:
                pass

            c += 1

            time.sleep(random.randint(delay[0], delay[1]))
            print('')

    logger.warning("Скрипт успешно завершил свою работу")
    input()

