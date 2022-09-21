import turtle as t


t.speed(speed=0)
t.hideturtle()
t.Screen().setup(345, 240)
t.Screen().cv._rootwindow.resizable(False, False)
# t.pensize(1)

offsetX = 10
offsetY = -10

t.tracer(n=0, delay=10)
screen = t.Screen()

def draw_text(x,y,text):
    t.goto((-screen.window_width()/2)+offsetX+x,( screen.window_height()/2)-y+offsetY)
    t.setheading(0)
    t.write(text)


def set_color(rgb):
    r,g,b=rgb[0]/255,rgb[1]/255,rgb[2]/255
    t.color(r, g, b)

def check_buffer():
    print(t.tracer())

def use_buffer():
    t.tracer(n=0, delay=10)

def paint_buffer():
    t.update()


def fill_rect(x,y,w,h):

    t.up()
    # t.goto(x, -y)
    t.goto((-screen.window_width()/2)+offsetX+x,( screen.window_height()/2)-y+offsetY)

    t.setheading(0)
    t.down()

    t.begin_fill()

    t.forward(w)
    t.right(90)
    t.forward(h)
    t.right(90)
    t.forward(w)
    t.right(90)
    t.forward(h)
    t.right(90)

    t.end_fill()
