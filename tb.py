import discord
import wmi
import win32api, win32con
import rotatescreen
import pyautogui
import asyncio

c = wmi.WMI(namespace='wmi')

methods = c.WmiMonitorBrightnessMethods()[0]

screen = rotatescreen.get_primary_display()

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

class GodBot(discord.Client):
    async def on_ready(self):
        actv = discord.Game(
            name= "huh",
            state= 'stop trying to hack me qaiik',
            details= 'controll!help in any server im in or my dms',
            large_image_url='https://i.pinimg.com/originals/50/8e/a8/508ea8f7efebdb885119039f8e249a3e.png'
        )
        await client.change_presence(status=discord.Status.idle, activity=actv)
        print('login', self.user)
    
    async def on_message(self, message):
        print(message.content)

        global clamp

        if message.content.startswith('controll!'):
            print('Command: ' + message.content)
            args = message.content.replace('controll!', '').split(' ')
            name = args[0]

            print("Args: " + ", ".join(args))

            print("Name: " + args[0])

            if args[0] == "display":
                if len(args) >= 2:
                    if args[1] == "brightness":
                        if len(args) == 2:
                            await message.channel.send("Main screen brightness: "+str(c.WmiMonitorBrightness()[0].CurrentBrightness))
                        elif args[2] == "set":
                            try:
                                if len(args) == 4:
                                    if args[3].isdigit():
                                        clamped = clamp(int(args[3]), 0, 100)
                                        methods.WmiSetBrightness(clamped, 0)
                                        await message.channel.send("Set the main screen brightness to " + str(clamped) + ".")
                                    else:
                                        await message.channel.send("Nice try! Sadly, win32api is smarter than that. Better luck next time!")
                                else:
                                    await message.channel.send("Oops! You didn't provide a valid brightness level.")
                            except Exception as e:
                                await message.channel.send(args[3] + " is not a valid brightness level.")
                    elif args[1] == "rotate":
                        if len(args) == 2:
                            await message.channel.send("Please tell me how to rotate the screen: landscape, portrait-flipped, landscape-flipped, or portrait.")
                        else:
                            if len(args) == 3:
                                if args[2] == "landscape":
                                    screen.set_landscape()
                                    await message.channel.send("Set the screen orientation to landscape.")
                                elif args[2] == "portrait-flipped":
                                    screen.set_portrait_flipped()
                                    await message.channel.send("Set the screen orientation to portrait (flipped).")
                                elif args[2] == "landscape-flipped":
                                    screen.set_landscape_flipped()
                                    await message.channel.send("Set the screen orientation to landscape (flipped).")
                                elif args[2] == "portrait":
                                    screen.set_portrait()
                                    await message.channel.send("Set the screen orientation to portrait.")
                                else:
                                    await message.channel.send("Invalid rotation. Please tell me how to rotate the screen: landscape, portrait-flipped, landscape-flipped, or portrait.")
                else:
                    await message.channel.send("Oops! You didn't give me a command to work with.")
            elif args[0] == "cursor":
                if len(args) >= 2:
                    if args[1] == "x":
                        if len(args) == 2:
                            await message.channel.send("Current cursor position (x): " + str(win32api.GetCursorPos()[0]))
                        elif len(args) == 3:
                            try:
                                if args[2].isdigit():
                                    clamped = clamp(int(args[2]), 0, win32api.GetSystemMetrics(0))
                                    pos = win32api.GetCursorPos()
                                    win32api.SetCursorPos((clamped, pos[1]))
                                    npos = win32api.GetCursorPos()
                                    await message.channel.send("Alright! Changed the cursor's x value to " + str(npos[0]))
                                else:
                                    await message.channel.send("Nice try! Sadly, win32api is smarter than that. Better luck next time!")
                            except Exception as e:
                                print(str(e))
                                await message.channel.send("Oops! You didn't provide a valid x value.")
                    elif args[1] == "y":
                        if len(args) == 2:
                            await message.channel.send("Current cursor position (y): " + str(win32api.GetCursorPos()[1]))
                        elif len(args) == 3:
                            try:
                                if args[2].isdigit():
                                    clamped = clamp(int(args[2]), 0, win32api.GetSystemMetrics(1))
                                    pos = win32api.GetCursorPos()
                                    win32api.SetCursorPos((pos[0], int(args[2])))
                                    npos = win32api.GetCursorPos()
                                    await message.channel.send("Alright! Changed the cursor's y value to " + str(npos[1]))
                                else:
                                    await message.channel.send("Nice try! Sadly, win32api is smarter than that. Better luck next time!")
                            except Exception as e:
                                print(str(e))
                                await message.channel.send("Oops! You didn't provide a valid x value.")
                    elif args[1] == "click":
                        if len(args) == 2:
                            await message.channel.send("Which button? left or right?")
                        elif len(args) == 3:
                            if args[2] == "left":
                                pyautogui.leftClick()
                                await message.channel.send("Clicked with the left mouse button!")
                            elif args[2] == "right":
                                pyautogui.rightClick()
                                await message.channel.send("Clicked with the right mouse button!")
                            else:
                                await message.channel.send("Oops! You didn't provide a valid mouse button.")
                else:           
                    await message.channel.send("Oops! You didn't give me a command to work with.")
            elif args[0] == "keyboard":
                if len(args) >= 2:
                    if args[1] == "press":
                        if len(args) >=  3:
                            pyautogui.press(args[2])
                            await message.channel.send("Pressed key " + args[2] + ".")
                        else:
                            await message.channel.send("Please specify a key.")
                    elif args[1] == "type":
                        if len(args) >= 3:
                            pyautogui.write(' '.join(args[2:]))
                            await message.channel.send("Typed " + ' '.join(args[2:]) + ".")
                        else:
                            await message.channel.send("Please specify a sentence.")
                    elif args[1] == "message":
                        if len(args) >= 3:
                            pyautogui.write(' '.join(args[2:]))
                            pyautogui.press('enter')
                            await message.channel.send("Sent " + ' '.join(args[2:]) + ".")
                        else:
                            await message.channel.send("Please specify a sentence.")
            elif args[0] == "help":
                await message.channel.send("controll!cursor x - get my mouse cursor's X position\ncontroll!cursor y - get my mouse cursor's Y position\ncontroll!cursor x (number) - sets cursor X position (left and right from 0 to whatever you want)\ncontroll!cursor y (number) - sets cursor Y position (up and down from 0 to whatever you want)\ncontroll!display brightness set (number) - sets my screen brightness\ncontroll!display rotate (portrait, landscape, portrait-flipped, landscape-flipped) - rotate my screen (this can cause serious damage)\ncontroll!keyboard press (key) - press a key, such as x, y, enter, alt, etc.\ncontroll!keyboard type (message) - make me type a message\ncontroll!keyboard message (message) - make me send a message in discord or search for something when i have my mouse cursor on the url bar\ncontroll!status (message) - control my bot status")
            elif args[0] == "status":
                if (len(args) >= 2):
                    await client.change_presence(activity=discord.Game(name=(' '.join(args[1:]))))
                    await message.channel.send("Okay! Changed my bot status to " + (' '.join(args[1:])))
            else:
                await message.channel.send("Invalid command.")
                        

client = GodBot()
client.run('token')
