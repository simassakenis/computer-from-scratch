import numpy as np
import graphics


# Code for visualizing the components


black = graphics.color_rgb(10, 10, 10),
white = graphics.color_rgb(255, 255, 255),
lightGray = graphics.color_rgb(245, 245, 245),
green = graphics.color_rgb(48, 209, 88),
blue = graphics.color_rgb(10, 132, 255),
teal = graphics.color_rgb(10, 210, 255),
yellow = graphics.color_rgb(255, 214, 10),
red = graphics.color_rgb(255, 69, 58),
indigo = graphics.color_rgb(94, 92, 230),


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


class DecimalIndicator:
    def __init__(self, components, display, x, y, color=white, fontsize=32):
        self.components = components

        self.i = graphics.Text(graphics.Point(x, y), '0000')
        self.i.setFace('courier')
        self.i.setSize(fontsize)
        self.i.setTextColor(color)
        self.i.setStyle('bold')
        self.i.draw(display.win)

        self.update()

    def update(self):
        val = int(''.join([f'{c.state()}' for c in self.components]), 2)
        self.i.setText(str(val))


class Display:
    def __init__(self, width=1600, height=900):
        self.width = width
        self.height = height
        self.win = graphics.GraphWin(title='Computer',
                                     width=self.width,
                                     height=self.height)
        self.win.setBackground(lightGray)
        self.inds = []

    def draw_box(self, components, title, labels=None, colors=None,
                 xoffset=0, yoffset=0, sep_after=[], decimal=False):
        hspace = 40
        hspaces = [1.5 if (j + 1) in sep_after else 1
                   for j in range(len(components))]
        hspaces = hspace * np.array([1.5] + hspaces[:-1] + [1.5])
        width = np.sum(hspaces) if not decimal else 3 * hspace
        height = 100
        x = (self.width / 2) - (width / 2) + xoffset # upper left corner
        y = (self.height / 2) - (height / 2) + yoffset # upper left corner

        drawRoundedRect(win=self.win,
                        upperLeft=graphics.Point(x, y),
                        lowerRight=graphics.Point(x + width, y + height),
                        radius=16, fill=white if not decimal else green)

        title = graphics.Text(
            graphics.Point(x + 0.5 * width, y + 0.25 * height),
            title
        )
        title.setFace('courier')
        title.setTextColor(black if not decimal else white)
        title.setSize(14)
        title.draw(self.win)

        if not decimal:
            self.inds.extend(
                [ComponentIndicator(component=c, display=self,
                                    x=x + np.cumsum(hspaces)[i],
                                    y=y + 0.75 * height,
                                    color=colors[i], radius=0.07 * height,
                                    label=labels[i], vspace=0.2 * height,
                                    fontsize=12)
                 for i, c in enumerate(components)]
            )
        else:
            self.inds.append(
                DecimalIndicator(components=components, display=self,
                                 x=x + 0.5 * width, y=y + 0.65 * height)
            )

    def update(self):
        for ind in self.inds:
            ind.update()

