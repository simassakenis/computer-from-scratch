import numpy as np
import graphics


# Code for visualization


black = graphics.color_rgb(10, 10, 10),
white = graphics.color_rgb(255, 255, 255),
lightGray = graphics.color_rgb(245, 245, 245),
green = graphics.color_rgb(48, 209, 88),
blue = graphics.color_rgb(10, 132, 255),
teal = graphics.color_rgb(10, 210, 255),
yellow = graphics.color_rgb(255, 214, 10),
red = graphics.color_rgb(255, 69, 58),


def drawRoundedRect(win, upperLeft, lowerRight, radius, fill):
    width = lowerRight.getX() - upperLeft.getX()
    height = upperLeft.getY() - lowerRight.getY()

    r1 = graphics.Rectangle(
        graphics.Point(upperLeft.getX(), upperLeft.getY() + radius),
        graphics.Point(lowerRight.getX(), lowerRight.getY() - radius)
    )
    r2 = graphics.Rectangle(
        graphics.Point(upperLeft.getX() + radius, upperLeft.getY()),
        graphics.Point(lowerRight.getX() - radius, upperLeft.getY() + radius)
    )
    r3 = graphics.Rectangle(
        graphics.Point(upperLeft.getX() + radius, lowerRight.getY() - radius),
        graphics.Point(lowerRight.getX() - radius, lowerRight.getY())
    )

    c1 = graphics.Circle(
        graphics.Point(upperLeft.getX() + radius, upperLeft.getY() + radius),
        radius=radius
    )
    c2 = graphics.Circle(
        graphics.Point(lowerRight.getX() - radius, upperLeft.getY() + radius),
        radius=radius
    )
    c3 = graphics.Circle(
        graphics.Point(upperLeft.getX() + radius, lowerRight.getY() - radius),
        radius=radius
    )
    c4 = graphics.Circle(
        graphics.Point(lowerRight.getX() - radius, lowerRight.getY() - radius),
        radius=radius
    )

    for obj in [r1, r2, r3, c1, c2, c3, c4]:
        obj.setFill(fill)
        obj.setWidth(0)
        obj.draw(win)


class ComponentIndicator:
    def __init__(self, component, display, x, y, color,
                 radius=7, label='', vspace=0, fontsize=12):
        self.component = component
        self.color = color

        l = graphics.Text(graphics.Point(x, y - vspace), label)
        l.setFace('courier')
        l.setSize(fontsize)
        l.draw(display.win)

        self.i = graphics.Circle(graphics.Point(x, y), radius)
        self.i.setFill(self.color if self.component.state() else black)
        self.i.setWidth(0)
        self.i.draw(display.win)

    def update(self):
        self.i.setFill(self.color if self.component.state() else black)


class Display:
    def __init__(self, width=1200, height=800):
        self.width = width
        self.height = height
        self.win = graphics.GraphWin(title='Computer',
                                     width=self.width,
                                     height=self.height)
        self.win.setBackground(lightGray)
        self.inds = []

    def draw_box(self, components, labels, colors, title,
                 yoffset=0, sep_after=[]):
        hspace = 40
        hspaces = [1.5 if (j + 1) in sep_after else 1
                   for j in range(len(components))]
        hspaces = hspace * np.array([1.5] + hspaces[:-1] + [1.5])
        width = np.sum(hspaces)
        height = 100
        x = (self.width / 2) - (width / 2) # upper left corner
        y = (self.height / 2) - (height / 2) + yoffset # upper left corner

        drawRoundedRect(win=self.win,
                        upperLeft=graphics.Point(x, y),
                        lowerRight=graphics.Point(x + width, y + height),
                        radius=16, fill=white)

        title = graphics.Text(
            graphics.Point(x + 0.5 * width, y + 0.25 * height),
            title
        )
        title.setFace('courier')
        title.setSize(14)
        title.draw(self.win)

        self.inds.extend(
            [ComponentIndicator(component=c, display=self,
                                x=x + np.cumsum(hspaces)[i],
                                y=y + 0.75 * height,
                                color=colors[i], radius=0.07 * height,
                                label=labels[i], vspace=0.2 * height,
                                fontsize=12)
             for i, c in enumerate(components)]
        )

    def update(self):
        for ind in self.inds:
            ind.update()

