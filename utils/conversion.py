import math
from shapely.ops import transform
from shapely.geometry import Polygon, MultiPolygon


'''
Functions to convert Swedish national coordinate system
to WGS84 coordinate system.
'''
class CoordinateTransformer:
    def __init__(self):
        self.axis = 6378137.0
        self.flattening = 1.0 / 298.257222101
        self.central_meridian = 15.0
        self.scale = 0.9996
        self.false_northing = 0.0
        self.false_easting = 500000.0

        self.e2 = self.flattening * (2 - self.flattening)
        self.n = self.flattening / (2 - self.flattening)
        self.a_roof = self.axis / (1 + self.n) * (1 + self.n**2 / 4 + self.n**4 / 64)
        self.delta1 = self.n / 2 - 2 * self.n**2 / 3 + 37 * self.n**3 / 96 - self.n**4 / 360
        self.delta2 = self.n**2 / 48 + self.n**3 / 15 - 437 * self.n**4 / 1440
        self.delta3 = 17 * self.n**3 / 480 - 37 * self.n**4 / 840
        self.delta4 = 4397 * self.n**4 / 161280

        self.Astar = self.e2 + self.e2**2 + self.e2**3 + self.e2**4
        self.Bstar = -(7 * self.e2**2 + 17 * self.e2**3 + 30 * self.e2**4) / 6
        self.Cstar = (224 * self.e2**3 + 889 * self.e2**4) / 120
        self.Dstar = -(4279 * self.e2**4) / 1260

        self.deg_to_rad = math.pi / 180
        self.lambda_zero = self.central_meridian * self.deg_to_rad

    def sweref99tm_to_wgs84(self, x, y):
        xi = (x - self.false_northing) / (self.scale * self.a_roof)
        eta = (y - self.false_easting) / (self.scale * self.a_roof)

        xi_prim = (xi - self.delta1 * math.sin(2 * xi) * math.cosh(2 * eta)
                   - self.delta2 * math.sin(4 * xi) * math.cosh(4 * eta)
                   - self.delta3 * math.sin(6 * xi) * math.cosh(6 * eta)
                   - self.delta4 * math.sin(8 * xi) * math.cosh(8 * eta))
        
        eta_prim = (eta - self.delta1 * math.cos(2 * xi) * math.sinh(2 * eta)
                    - self.delta2 * math.cos(4 * xi) * math.sinh(4 * eta)
                    - self.delta3 * math.cos(6 * xi) * math.sinh(6 * eta)
                    - self.delta4 * math.cos(8 * xi) * math.sinh(8 * eta))
        
        phi_star = math.asin(math.sin(xi_prim) / math.cosh(eta_prim))
        delta_lambda = math.atan(math.sinh(eta_prim) / math.cos(xi_prim))
        
        lon_radian = self.lambda_zero + delta_lambda
        lat_radian = (phi_star + math.sin(phi_star) * math.cos(phi_star) *
                      (self.Astar + self.Bstar * math.sin(phi_star)**2 +
                       self.Cstar * math.sin(phi_star)**4 + self.Dstar * math.sin(phi_star)**6))
        
        longitude = lon_radian * 180 / math.pi
        latitude = lat_radian * 180 / math.pi
        
        return latitude, longitude

    def transform_geometry(self, geom):
        def convert_point(x, y):
            return self.sweref99tm_to_wgs84(x, y)
        return transform(convert_point, geom)

    def swap_coordinates(self, geom):
        if geom.geom_type == 'Polygon':
            new_coords = [(y, x) for x, y in geom.exterior.coords]
            new_geom = Polygon(new_coords)
            if not geom.exterior.is_empty:
                new_geom = Polygon(new_coords, [[(y, x) for x, y in interior.coords] for interior in geom.interiors])
            return new_geom
        elif geom.geom_type == 'MultiPolygon':
            new_polygons = []
            for poly in geom:
                new_coords = [(y, x) for x, y in poly.exterior.coords]
                new_poly = Polygon(new_coords)
                if not poly.exterior.is_empty:
                    new_poly = Polygon(new_coords, [[(y, x) for x, y in interior.coords] for interior in poly.interiors])
                new_polygons.append(new_poly)
            return MultiPolygon(new_polygons)
        else:
            return geom


# Source: https://www.trafiklab.se/docs/using-trafiklab-data/combining-data/converting-sweref99-to-wgs84/
# Python equivalent of the Java code in the link above.