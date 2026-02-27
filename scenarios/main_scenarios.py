
from pydrivingsim import TrafficLight, Target, TrafficCone, SuggestedSpeedSignal, GraphicObject, Vehicle, Agent, Coin

class OnlyVehicle():
    def __init__(self):
        #Initialize the vehicle
        self.vehicle = Vehicle()
        self.vehicle.set_screen_here()
        self.vehicle.set_pos_ang((0, -1, 0))

        #Initialize target
        target = Target()
        target.set_pos((182, -1))
        target.set_object(self.vehicle)

    def update(self):
        self.vehicle.set_screen_here()
        self.vehicle.control([0.5, 0.0])

    def terminate(self):
        pass

class AutonomousVehicle():
    def __init__(self):
        # Initialize the vehicle
        self.vehicle = Vehicle()
        self.vehicle.set_screen_here()
        self.vehicle.set_pos_ang((0, -1, 0))

        #Initialize the agent
        self.agent = Agent(self.vehicle)

        #Initialize target
        target = Target()
        target.set_pos((182, -1))
        target.set_object(self.vehicle)

    def update(self):
        self.agent.compute()
        action = self.agent.get_action()

        self.vehicle.set_screen_here()
        self.vehicle.control([action[0], action[1]])

    def terminate(self):
        self.agent.terminate()


class BasicTrafficLight():
    def __init__(self):
        cone = TrafficCone()
        cone.set_pos((1.0,0))
        cone = TrafficCone()
        cone.set_pos((1.0,2))
        cone = TrafficCone()
        cone.set_pos((1.0,-2))

        trafficlight = TrafficLight()
        trafficlight.set_pos((160,-3))
        trafficlight.reset()

class GetTheCoins():
    def __init__(self):
        # Added point in zero to be able to start with a reference
        coin = Coin()
        coin.set_pos((0,-1))

        # Targets to avoid cones
        coin = Coin()
        coin.set_pos((10,-1))
        coin = Coin()
        coin.set_pos((35,1))
        coin = Coin()
        coin.set_pos((60,-1))
        coin = Coin()
        coin.set_pos((100,1))
        coin = Coin()
        coin.set_pos((130,-1))

        # Add two final points to stabilize the trajectory
        coin = Coin()
        coin.set_pos((160,-1))
        coin = Coin()
        coin.set_pos((182,-1))


class BasicSpeedLimit():
    def __init__(self):
        signal = SuggestedSpeedSignal(10)
        signal.set_pos((50, 4))
        bologna = GraphicObject("imgs/pictures/bologna.png", 35)
        bologna.set_pos((67,12))
        signal = SuggestedSpeedSignal(90)
        signal.set_pos((96, 4))
        super = GraphicObject("imgs/pictures/superstrada.png", 5)
        super.set_pos((100,6))



def add_intersection(
        # Function to spawn and populate an intersection
        x_cross: float,
        v_min: float,
        v_max: float,
        offset: float = 2.0,
        bg_img: str = "imgs/intersection.png",
        bg_scale: float = 5.7,
        bg_y: float = 8.1,
        n_per_direction: int = 4,   # Number of crossing vehicles for lane
):

    bg = GraphicObject(bg_img, bg_scale)
    bg.set_pos((x_cross + 1, bg_y))

    vehicles = []

    for _ in range(n_per_direction):
        vehicles.append(CrossingVehicle(x_cross=x_cross, v_min=v_min, v_max=v_max, direction=-1))
    for _ in range(n_per_direction):
        vehicles.append(CrossingVehicle(x_cross=x_cross + offset, v_min=v_min, v_max=v_max, direction=1))

    return bg, vehicles




class CrossingScenario():
    def __init__(self):
        v_min = 5
        v_max = 18

        #self.bg1, self.v1 = add_intersection(85.0, v_min=v_min, v_max=v_max)
        self.bg2, self.v2 = add_intersection(140.0, v_min=v_min, v_max=v_max)
        self.bg3, self.v3 = add_intersection(200.0, v_min=v_min, v_max=v_max)
        self.bg4, self.v4 = add_intersection(230.0, v_min=v_min, v_max=v_max)

