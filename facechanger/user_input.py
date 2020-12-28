from facechanger.constants import INDICES
import copy

class UserInputHandler:
    NO_CLICK=0b00
    LEFT_CLICK=0b01
    RIGHT_CLICK=0b10

    def __init__(self, filter):
        self.filter = filter
        self.features = None
        self.selected = None
        self.start = None
        self.wip = None

    def click(self, event, x, y, flags, params):
        if self.features is not None:
            if flags == self.NO_CLICK:
                # Reset if no buttons is clicked
                if self.selected is not None:
                    self.selected = None
                    self.filter = self.wip
                    self.wip = None
                    self.start = None
            else:
                # Otherwise check what feature was clicked
                if self.selected is None and flags in [self.LEFT_CLICK, self.RIGHT_CLICK]:
                    for k, v in INDICES.items():
                        points = self.features[v]
                        if (points.min(axis=0)<(x,y)).all() and (points.max(axis=0)>(x,y)).all():
                            self.selected = k
                            self.start = (x,y)
                            self.wip = copy.deepcopy(self.filter)

                # Apply change in filter if an object was selected
                if self.selected is not None:
                    if flags == self.LEFT_CLICK:
                        type = "trans"
                        scale = 1
                    elif flags == self.RIGHT_CLICK:
                        type  = "zoom"
                        scale = 0.01
                    else:
                        type  = "zoom"
                        scale = 0
                    self.wip[self.selected][type][0]=self.filter[self.selected][type][0]+(x-self.start[0])*scale
                    self.wip[self.selected][type][1]=self.filter[self.selected][type][1]+(y-self.start[1])*scale

    def get_filter(self):
        if self.wip is not None:
            return self.wip
        else:
            return self.filter
