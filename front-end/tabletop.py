class Tabletop:
    def __init__(self, canvas, x, y, size, color, name, tabletop_id):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.name = name
        self.tabletop_id = tabletop_id
        self.id = self.canvas.create_rectangle(self.x, self.y, self.x + self.size, self.y + self.size, fill=self.color)
        self.text_id = self.canvas.create_text(self.x + self.size / 2, self.y + self.size / 2, text=self.name, fill="white")
    
    def move(self, dx, dy):
        self.canvas.move(self.id, dx, dy)
        self.canvas.move(self.text_id, dx, dy)
        self.x += dx
        self.y += dy
    
    def change_color(self, color):
        self.canvas.itemconfig(self.id, fill=color)
        self.color = color
    
    def change_name(self, new_name):
        self.name = new_name
        self.canvas.itemconfig(self.text_id, text=self.name)
    
    def delete(self):
        self.canvas.delete(self.id)
        self.canvas.delete(self.text_id)

    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.tabletop_id