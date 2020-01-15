import tkinter as tk

app = tk.Tk()

MATRIX = [[1,2,3],[1,2,2],[1,2,3],[1,4,3]]
VECTOR = [1,2,3]
current_steps = []

rectangle_coords = [(250, 150), (460, 150), (670, 150), (880, 150)]

top_frame = tk.Frame(app)
top_frame = top_frame.pack(side=tk.TOP)
bot_frame = tk.Frame(app)
bot_frame = bot_frame.pack(side=tk.BOTTOM)


canvas = tk.Canvas(top_frame, bg="white", height=500, width=1300)

class Step:
    # Each step for a rectangle
    def __init__(self, lines):
        self.input_left = 0
        self.input_right = 0
        self.lines = lines
        self.inner_value = 0

    def __str__(self):
        return "Input Left: " + str(self.input_left) + " Input Right: " + \
               str(self.input_right) + " Lines: " + str(self.lines) + \
               " Inner Value: " + str(self.inner_value)

def systolic_delay(mat_list):
    # ADD ZEROS TO MATRIX SO IT CAN ADD "DELAY"
    delay_num = 0

    for mat_line in mat_list:
        for i in range(delay_num):
            mat_line.insert(0,0)
        delay_num += 1

def get_mat_steps():
    # Create the steps list
    systolic_delay(MATRIX)

    ls = [Step(MATRIX[i]) for i in range(len(MATRIX))]

    return ls

list_steps = get_mat_steps()

def list_to_string(list1):
    # CONVERT PYTHON LIST TO A STRING
    string_list = ""

    for elem in list1:

        string_list += str(elem) + " "

    return string_list

def draw_rectangle(canvas, top_frame, P, x, y, hurdle = False):
    # draw the rectangles
    canvas.create_rectangle(x, y, x+100, y+200, fill="white", outline='black')

    #ingoing line
    canvas.create_line(top_frame, x-50, y+100, x, y+100)
    #outgoint line
    canvas.create_line(top_frame, x+100, y+100, x+150, y+100)

    # P
    canvas.create_text(top_frame, x + 50, y + 30, text=P, font="Times 20")


    if hurdle:
        #top left
        canvas.create_rectangle(x-60, y+110, x-50, y+90, fill="black", outline='black')
        #top right
        canvas.create_rectangle(x + 150, y + 110, x + 160, y+90, fill="black", outline='black')

def draw_updated_tags(steps):
    # draw the dynamic information (value of each step, current input etc.)
    counter = 0

    for step in steps:
        #value inside the rectangle
        if step.inner_value is not None:
            canvas.create_text((rectangle_coords[counter][0] + 50, rectangle_coords[counter][1] + 130), tag="DELETEME", text=str(step.inner_value), font="Times 20 bold")
        else:
            canvas.create_text((rectangle_coords[counter][0] + 50, rectangle_coords[counter][1] + 130), tag="DELETEME", text="", font="Times 20 bold")
        #the vectore input on the left
        if step.input_left != 0:
            canvas.create_text((rectangle_coords[counter][0] - 15 , rectangle_coords[counter][1] + 50), tag="DELETEME",
                               text=str(step.input_left), font="Times 14")
        else:
            canvas.create_text((rectangle_coords[counter][0] - 15, rectangle_coords[counter][1] + 50), tag="DELETEME",
                               text="", font="Times 14")
        #the vector input on the right
        if step.input_right != 0:
            canvas.create_text((rectangle_coords[counter][0] + 115 , rectangle_coords[counter][1] + 50), tag="DELETEME",
                               text=str(step.input_right), font="Times 14")
        else:
            canvas.create_text((rectangle_coords[counter][0] + 115, rectangle_coords[counter][1] + 50), tag="DELETEME",
                               text="", font="Times 14")

        # the matrix lines displayed on the bottom of the rectangles
        lower_line_pixels = 20
        for i in step.lines:
            if i != 0:
                canvas.create_text((rectangle_coords[counter][0] + 40, rectangle_coords[counter][1] + 200 + lower_line_pixels), tag="DELETEME", text=str(i), font="Times 14")
            else:
                canvas.create_text((rectangle_coords[counter][0] + 40, rectangle_coords[counter][1] + 200 +  lower_line_pixels), tag="DELETEME", text="Delay", font="Times 14")

            lower_line_pixels += 20

        counter += 1


def draw_vector():
    #draw the current values of the vector
    canvas.create_text(top_frame, 650, 80, text=list_to_string(VECTOR), font="Times 20", tag="DELETEME")

def calculate_step():
    # CALCULATE THE VALUE OF P0 P1 P2... EVEY STEP
    i = len(list_steps) - 1

    while i > 0:

        list_steps[i].input_left = list_steps[i - 1].input_right
        list_steps[i].input_right = list_steps[i].input_left

        if list_steps[i].lines:

            aux = list_steps[i].lines.pop(0)
            list_steps[i].inner_value = list_steps[i].inner_value + list_steps[i].input_left * aux

        i = i - 1

    if list_steps[0].lines:
        list_steps[0].lines.pop(0)

    if VECTOR:
        aux = VECTOR.pop(0)
        list_steps[0].input_left = aux
        list_steps[0].input_right = aux

        if list_steps[0].input_left is not None:
            list_steps[0].inner_value = list_steps[0].inner_value + list_steps[0].input_left * aux
    else:
        list_steps[0].input_left = 0
        list_steps[0].input_right = 0

    canvas.delete("DELETEME")

    draw_updated_tags(list_steps)

def on_click():
    #CALLED WHEN THE NEXT STEP BUTTON IS PRESSED
    calculate_step()

def draw_board(app):
    # DRAW THE STATIC ELEMENTS OF THE BOARD AND THE INITIAL VALUES FOR THE DYNAMIC ELEMENTS
    label = tk.Label(app, text="Matrix-Vector")
    label.pack()

    canvas.create_text(top_frame, 650, 50, text="Vector", font="Times 20")

    init_coord = [250, 150]
    cont = 0
    for i in MATRIX:

        if i == MATRIX[0] or i == MATRIX[-1]: # if it is the last or first elemnt do not add the black squares
            isHurdle = False
        else:
            isHurdle = True

        draw_rectangle(canvas, top_frame, "P"+str(cont), init_coord[0], init_coord[1], isHurdle)
        cont += 1
        init_coord[0] += 210

    draw_vector()

    draw_updated_tags(list_steps)

    step_button = tk.Button(bot_frame, text="Next Step", command=on_click)

    canvas.pack()
    step_button.pack()

def start_visual():

    app.geometry("1500x620")
    app.resizable(0, 0)

    draw_board(app)

    app.mainloop()

if __name__ == "__main__":
    start_visual()