from math import sqrt, acos, pi
from decimal import Decimal, getcontext


getcontext().prec = 15


class Vector(object):
    
    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = "Cannot normalize the zero vector"
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = "No Unique Parallel component"
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = "No Unique Orthogonal component"
    ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG = "Only defined in two three dimension"
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def __add__(self, v):
        new_coordinates = [x+y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def __sub__(self, v):
        new_coordinates = [x-y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def times_scaler(self, c):
        new_coordinates = [Decimal(c)*x for x in self.coordinates]
        return Vector(new_coordinates)

    def magnitude(self):
        squared_coordinates = [x*x for x in self.coordinates]
        length = sqrt(sum(squared_coordinates))
        return Decimal(length)
        
    def normalize(self):
        try:
            magnitude = self.magnitude()                  
            return self.times_scaler(Decimal('1.0')/Decimal(magnitude))
        except ZeroDivisionError:
            raise Exception("Cannot normalize zero vector")


    def is_orthogonal_to(self, v, tolerance=1e-10):
        return abs(self.dot(v)) < tolerance

    def is_parallel_to(self, v):
        return (
            self.is_zero() or
            v.is_zero() or
            self.angle_with(v) == 0 or
            self.angle_with(v) == pi
        )

    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance


    def dot(self, v):
        return sum([Decimal(x)*Decimal(y) for x, y in zip(self.coordinates, v.coordinates)])

    def angle_with(self, v, in_degree=False):
        try:
            u1 = self.normalize()
            u2 = v.normalize()
            angle_in_radians = acos(u1.dot(u2))

            if in_degree:
                degrees_per_radians = 180. / pi
                return angle_in_radians * degrees_per_radians
            return angle_in_radians

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception("Cannot compute an angle with zero vector")
            else:
                raise e

    def component_orthogonal_to(self, basis):
        # v_orthogonal = v_basis - v_parallel

        try:
            projection = self.component_parallel_to(basis)
            return self.__sub__(projection)

        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e

    def component_parallel_to(self, basis):
        # (1) get a unit vector u
        # (2) take a dot product of v.u
        # (3) then multiply u but the result of the previous product
        #     result = (v.u) . u

        try:
            u = basis.normalize()
            weight = self.dot(u)
            return u.times_scaler(weight)

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e        

    def area_of_triangle_with(self, v):
        return self.area_of_parallelogram_with(v) / Decimal('2.0')

    def area_of_parallelogram_with(self, v):
        cross_product = self.cross(v)
        return cross_product.magnitude()

    def cross(self, v):
        try:
            x1, y1, z1 = self.coordinates
            x2, y2, z2 = v.coordinates
            new_coordinates = [
                y1*z2 - y2*z1,
                -(x1*z2 - x2*z1),
                x1*y2 - x2*y1
            ]

            return Vector(new_coordinates)
        except ValueError as e:
            msg = str(e)
            if msg == "need more than 2 values to unpack":
                self_embedded_in_R3 = Vector(self.coordinates + ('0',))
                v_embedded_in_R3 = Vector(v.coordinates + ('0',))
                return self_embedded_in_R3.cross(v_embedded_in_R3)
            elif (
                    msg == 'too many values to unpack',
                    msg == 'need more than 1 value to unpack'
            ):
                raise Exception(self.ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG)
            else:
                raise e
        
        

v = Vector([3.009, -6.172, 3.692])
w = Vector([6.404, -9.144, 2.759])

print(v.cross(w))
print("-------------")
print(v.area_of_parallelogram_with(w))
print("-------------")
print(v.area_of_triangle_with(w))
# print("#1")
# v = Vector([3.039, 1.879])
# w = Vector([0.825, 2.036])
# print(v.component_parallel_to(w))

# print("\n#2")
# v = Vector([-9.88, -3.264, -8.159])
# w = Vector([-2.155, -9.353, -9.473])
# print(v.component_orthogonal_to(w))

# print("\n#13")
# v = Vector([3.009, -6.172, 3.692, -2.51])
# w = Vector([6.404, -9.144, 2.759, 8.718])
# vpart = v.component_parallel_to(w)
# vorth = v.component_orthogonal_to(w)

# print("parallel component: {}".format(vpart))
# print("orthogonal component: {}".format(vorth))

# print('first pair...')
# v = Vector(['-7.579', '-7.88'])
# w = Vector(['22.737', '23.64'])

# # print(v.angle_with(w, in_degree=True))

# print('is parallel: {}'.format(v.is_parallel_to(w)))
# print('is orthogonal: {}'.format(v.is_orthogonal_to(w)))

# v = Vector([7.887, 4.138])
# w = Vector([-8.802, 6.776])

# print(v.dot(w))
# print(v.normalize())

# v1 = Vector([8.218, -9.341])
# v2 = Vector([-1.129, 2.111])
# print(v1 + v2)

# v1 = Vector([7.119, 8.215])
# v2 = Vector([-8.223, 0.878])
# print(v1 - v2)


# v1 = Vector([1.671, -1.012, -0.318])
# c = 7.41
# print(v1.times_scaler(c))
