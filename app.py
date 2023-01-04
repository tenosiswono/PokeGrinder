import rumps

class App(rumps.App):
    def __init__(self):
        super(App, self).__init__("Pokebot")
        self.menu.add(rumps.MenuItem(title='Details:'))
        self.menu.add(rumps.MenuItem(title='Time Elapsed:'))
        
    @rumps.timer(1)
    def refresh(self, _):
        f = open("status.txt", "r")
        status = f.read()
        self.title = f'{status}'
        ft = open("time.txt", "r")
        time = ft.read()
        self.menu['Time Elapsed:'].title = time
        fd = open("details.txt", "r")
        details = fd.read()
        self.menu['Details:'].title = details


App().run()