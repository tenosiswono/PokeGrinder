from python3_anticaptcha import ImageToTextTask

async def anticaptcha(image):
    print("Solving captcha...")
    
    ANTICAPTCHA_KEY = "43485a97fc151a8cd654141a46cdaea2"

    user_answer = ImageToTextTask.ImageToTextTask(anticaptcha_key = ANTICAPTCHA_KEY).\
        captcha_handler(captcha_link=image)
    
    return user_answer['solution']['text'] + "0"