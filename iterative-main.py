import tkinter as tk


class HanoiGame:
    def __init__(self, root):
        # Define the application's main window and startup variables
        self.root = root
        self.num_disks = 4  
        self.towers = [[], [], []]  
        self.move_count = 0 
        self.create_widgets()  

    def create_widgets(self):
        # Main drawing area and control buttons
        self.canvas = tk.Canvas(self.root, width=600, height=300, bg='white')
        self.canvas.grid(row=1, column=0, columnspan=4)

        # Draw tower
        for i in range(3):
            self.canvas.create_rectangle(200 * i + 150, 250, 200 * i + 160, 50, fill='black')

        # Create the section to set the number of disks
        self.disk_scale_label = tk.Label(self.root, text="Disk Sayısı:")
        self.disk_scale_label.grid(row=2, column=0, sticky="w")
        self.disk_scale = tk.Scale(self.root, from_=1, to=10, orient='horizontal')
        self.disk_scale.grid(row=2, column=1, sticky="ew")
        self.disk_scale.set(self.num_disks)

        # Place reset button
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_game)
        self.reset_button.grid(row=3, column=1)
        
        # Label showing the number of moves
        self.move_label = tk.Label(self.root, text="Moves: 0")
        self.move_label.grid(row=3, column=2)

        # Scale for speed adjustment
        self.speed_scale = tk.Scale(self.root, from_=1, to=5, orient='horizontal', label="Hız:")
        self.speed_scale.grid(row=3, column=3)

        # Start button
        self.start_button = tk.Button(self.root, text="Start", command=self.start_game)
        self.start_button.grid(row=3, column=4)

    def set_num_disks(self, num_disks):
        # Set the number of disks selected by the user and reset the game
        self.num_disks = int(num_disks)
        self.reset_game()

    def start_game(self):
        # When the game starts, get the disk count and reset the game
        self.num_disks = self.disk_scale.get() 
        self.move_count = 0 
        self.update_move_count()  
        self.reset_game() 
        self.moves = self.calculate_moves() 
        self.move_disks()  

    def reset_game(self):
        # Game reset operations
        for tower in self.towers:
            tower.clear()  
            
        self.canvas.delete("disk") 
        self.move_count = 0  
        self.update_move_count() 
        self.init_disks()  

    def init_disks(self):
        # Initialize disks
        self.towers = [[], [], []] 
        for i in range(self.num_disks):
            disk_width = 120 - (self.num_disks - i) * 10
            disk = tk.Frame(self.root, height=20, width=disk_width, bg=self.get_color(i))
            disk.width = disk_width  
            self.towers[0].append(disk)  

    def draw_disks(self):
        # Draw disks in drawing area
        self.canvas.delete("disk") # Clean up previous disks

        for tower_index, tower in enumerate(self.towers):
            x_center = 200 * tower_index + 150

            for disk_index, disk in enumerate(reversed(tower)):
                x1 = x_center - disk.width / 2
                x2 = x_center + disk.width / 2
                y1 = 250 - (disk_index * 22 + 20)
                y2 = y1 + 20
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=disk.cget("bg"), tags="disk")

    def calculate_moves(self):
        # Calculate the necessary moves
        moves = []
        for i in range(1, 2 ** self.num_disks):
            from_tower = (i & i - 1) % 3
            to_tower = ((i | i - 1) + 1) % 3
            moves.append((from_tower, to_tower))
            
        return moves

    def move_disks(self):
        # Moving disks
        if self.moves:
            # If there are moves left, make the next move
            from_tower, to_tower = self.moves.pop(0)
            disk = self.towers[from_tower].pop()  # )
            self.towers[to_tower].append(disk)  
            self.move_count += 1  
            self.update_move_count() 
            self.draw_disks()  
            self.root.after(1000 // self.speed_scale.get(), self.move_disks)

    def update_move_count(self):
        self.move_label.config(text=f"Hareket Sayısı: {self.move_count}")

    def get_color(self, disk):
        colors = ['light blue', 'blue', 'dark blue', 'purple', 'violet', 'magenta', 'pink', 'red', 'orange', 'yellow']
        return colors[disk % len(colors)]


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tower of Hanoi")
    hanoi = HanoiGame(root)
    root.mainloop()
