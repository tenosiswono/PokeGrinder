from python3_anticaptcha import ImageToTextTask
from lib.parser import conf

async def anticaptcha(image):
    print("Solving captcha...")
    
    ANTICAPTCHA_KEY = conf.general.anticaptcha_token

    user_answer = ImageToTextTask.ImageToTextTask(anticaptcha_key = ANTICAPTCHA_KEY).\
        captcha_handler(captcha_link=image)
    
    return user_answer['solution']['text']