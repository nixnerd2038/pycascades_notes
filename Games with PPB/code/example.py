import ppb

 class Player(ppb.Sprite):
     image = ppb.Square()
     position = ppb.Vector()
     target = ppb.Vector()

     def on_update(self, update_event: ppb.events.Update, signal):
         self.position += (self.target - self.position)