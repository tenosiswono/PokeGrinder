# PokeGrinder  🤖
This is an Auto-Grinding bot made for Pokemeow. Efficient with plenty of features and more to come.

## Supported features
This bot can currently handle :
1. Hunting
- Encounter then use a ball depending on the rarity of the Pokemon.
- Stops if a captcha appears then continue after the captcha has been solved.
- Logs elapsed time, encounters, catches, captchas solved and eggs hatched.

2. Captcha Solving
- Solves captchas using AntiCaptcha API.
- Notifies if unable to solve captcha.
- If captcha solver disabled, will notify otherwise.
- Captcha Solver and Notifier can both be toggles on/off.

3. Auto-Buy Balls
- Automatically buys balls when 0 are left.
- Can buy custom amounts which can be specified in `config.json`.

4. Handling Eggs
- Automatically hatches and holds eggs.
- You must be holding an egg before you start grinding.

## Upcoming Features
1. Fishing
2. Auto Release Duplicates
3. Log Pokecoins earned
4. Suspicion Avoidance Features

## Installating

### On your PC
1. Install Python 3.8 or higher.
2. Download this repo then unzip it.
3. Inside of the repo type the following command `python -m pip install -r requirements.txt`
4. Paste your Dicord Auth Token, User ID and the Channel ID you want to grind in inside `config.json`.
5. You may also edit the rarities section in `config.json` according to your convenience.

## Launching 
1. Run `main.py`.
2. Make sure to buy balls before launching.
3. The bot will take some time (depending on your hardware) to start. When it is ready it will do ;p in the channel you provided in `config.json` and then start grinding.

## Stoping
To stop the program simply close the command prompt.

## Disclamer ⚠️
- We're of course not responsible for any ban you recieve for using this bot.
- Please keep an eye on the bot to solve captchas. Do not be irresponsible if you don't want to get banned.
- Please do not grind in public servers.
