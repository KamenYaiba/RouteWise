from helping_functions import clean_url, time_to_gmt, add_route_to_json


class Route:
    def __init__(self, route_id, user_id, route, time_frame, offset_to_gmt, new=True):
        self.route_id = route_id
        self.user_id = user_id
        self.route = route
        if isinstance(time_frame, list):
            self.time_frame = time_frame
        else:
            self.time_frame = time_to_gmt(time_frame, offset_to_gmt)
        self.offset_to_gmt = offset_to_gmt

        if new:
            start, end = self.time_frame
            if start < end:
                for i in range(start, end):
                    add_route_to_json(i, self)
            else:
                for i in range(start, 24):  # Loop from start to midnight
                    add_route_to_json(i, self)
                for i in range(0, end):  # Loop from midnight to end
                    add_route_to_json(i, self)

    def to_dict(self):
        return {
            "route_id": self.route_id,
            "user_id": self.user_id,
            "route": self.route,
            "time_frame": self.time_frame,
            "offset_to_gmt": self.offset_to_gmt
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            route_id=data["route_id"],
            user_id=data["user_id"],
            route=data["route"],
            time_frame=data["time_frame"],
            offset_to_gmt=data["offset_to_gmt"],
            new=False
        )

#r=Route(3,2,"https://maps.app.goo.gl/QwhAoBWBYkn9dic5A", "6-8", 3)
