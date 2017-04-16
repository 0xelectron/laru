import numbers
import math
import decimal
from decimal import Decimal, getcontext

# set precision of decimal numbers
getcontext().prec = 30

class Vector(object):
    """Vector: A Simple Vector Object

    Attributes:

    """
    def __init__(self, coordinates):
        """__init__ method

        Args:
            coordinates (iterator): coordinates of the vector

        Raises:
            decimal.InvalidOperation: If coordinates values are invalid
            TypeError: if coordinates is not an iterator
        """

        if not coordinates:
            raise ValueError

        try:
            self.coordinates = tuple([Decimal(x) for x in coordinates])
        except decimal.InvalidOperation:
            raise decimal.InvalidOperation('The coordinates must be a valid number')
        except TypeError:
            raise TypeError('The coordinates must be iterable')

        # dimension of vector
        self.dimension = len(coordinates)

    @property
    def mag(self):
        """ Decimal: Magnitude of a vector """
        return Decimal(math.sqrt(sum([x**2 for x in self.coordinates])))


    @property
    def norm(self):
        """ Vector: Normalization of a vector """
        if (self.mag != 0):
            return self.__mul__((Decimal(1.0)/self.mag))
        else:
            raise ZeroDivisionError('Cannot normalize the zero vector')


    def dot(self, v):
        """ dot: dot product of two vectors

        Args:
            v: Vector object

        Returns:
            Decimal

        Raises:
            TypeError: if v is not a vector

        """
        if not isinstance(v, Vector):
            raise TypeError('Argument must be a vector')
        return Decimal(sum([x * v.coordinates[i] for i, x in enumerate(self.coordinates)]))


    def cross(self, v):
        """ cross: cross product of two vectors

        Args:
            v: Vector object

        Returns:
            Vector

        Raises:
            TypeError: if v is not a vector
            NotImplementedError: If dimension not equal to 3

        """
        if not isinstance(v, Vector):
            raise TypeError('Argument must be a vector')

        if not (self.dimension == v.dimension == 3):
            raise NotImplementedError

        x1, y1, z1 = self.coordinates
        x2, y2, z2 = v.coordinates

        # basic cross product formula for 3 dimensional vector
        x = y1*z2 - y2*z1
        y = -(x1*z2 - x2*z1)
        z = x1*y2 - x2*y1

        return Vector([x,y,z])


    def area_of_parallelogram(self, v):
        """ area_of_parallelogram: area of parallelogram spanned by
            self and v

        Args:
            v: Vector object

        Returns:
            Decimal: area of parellelogram

        Raises:
            TypeError: if v is not a vector

        """
        if not isinstance(v, Vector):
            raise TypeError('Argument must be a vector')

        return (self.cross(v)).mag


    def area_of_triangle(self, v):
        """ area_of_triangle: area of triangle spanned by self and v

        Args:
            v: Vector object

        Returns:
            Decimal: area of triangle

        Raises:
            TypeError: if v is not a vector

        """
        if not isinstance(v, Vector):
            raise TypeError('Argument must be a vector')

        return self.area_of_parallelogram(v) / 2


    def theta(self, v, in_degrees=False):
        """ theta: finds the angle between two vectors

        Args:
            v: Vector object
            in_degrees: boolean

        Returns:
            Angle between two vectors. Default in radians,
            and in degrees if in_degrees is True

        Raises:
            TypeError: if v is not a vector
            Exception: if product of magnitude of two vectors is zero

        """
        if not isinstance(v, Vector):
            raise TypeError('Argument must be a vector')

        mag_product = self.mag * v.mag
        if mag_product == 0:
            raise Exception('Cannot find angle for a zero vector')

        a = self.__clean_angle(self.dot(v)/mag_product)
        t = math.acos(a)
        if in_degrees:
            return math.degrees(t)
        return t


    def proj_on(self, v):
        """ proj_on: finds projection of vector on a given vector v

        Args:
            v: Vector object

        Returns:
            Vector

        Raises:
            TypeError: if v is not a vector

        """
        if not isinstance(v, Vector):
            raise TypeError('Argument must be a vector')

        return self.dot(v.norm) * v.norm


    def orthogonal_to(self, v):
        """ orthogonal_to: finds a vector to a given vector v

        Args:
            v: Vector object

        Returns:
            Vector

        Raises:
            TypeError: if v is not a vector

        """
        if not isinstance(v, Vector):
            raise TypeError('Argument must be a vector')

        return self.__sub__(self.proj_on(v))


    def decompose(self, v):
        """ decompose: decomposes the vector(self) into sum of two vectors.
        one of which is orthogonal to v and the other is parallel to v.

        Args:
            v: Vector object

        Returns:
            tuple of two vectors

        Raises:
            TypeError: if v is not a vector

        """
        if not isinstance(v, Vector):
            raise TypeError('Argument must be a vector')

        return (self.proj_on(v), self.orthogonal_to(v))


    def is_zero(self, tolerance=1e-10):
        """ is_zero: checks if vector is zero

        Args:
            tolerance: tolerance for the number to be zero

        Returns:
            True: if vector is zero
            False: if not

        """
        return self.mag < tolerance


    def is_orthogonal_to(self, v, tolerance=1e-10):
        """ is_orthogonal_to: check if two vectors are orthognal

        Args:
            v: Vector object
            tolerance: tolerance for the number to be orthogonal

        Returns:
            True: if two vectors are orthogonal to each other
            False: if not

        Raises:
            TypeError: If v is not a vector

        """
        if not isinstance(v, Vector):
            raise TypeError('Argument must be a vector')

        return abs(self.dot(v)) < tolerance


    def is_parallel_to(self, v):
        """ is_parallel_to: check if two vectors are parallel

        Args:
            v: Vector object

        Returns:
            True: if two vectors are parallel to each other
            False: if not

        Raises:
            TypeError: If v is not a vector

        """
        if not isinstance(v, Vector):
            raise TypeError('Argument must be a vector')

        return (self.is_zero() or
                v.is_zero() or
                self.theta(v) == Decimal(math.pi) or
                self.theta(v) == Decimal(0))


    def __clean_angle(self, a):
        """ __clean_angle: constraint angle between [-1, 1]

        Args:
            a: angle to be constrained

        Returns:
            Decimal: constrained number between -1 and 1

        Raises:
            TypeError: if a is not a number

        """
        if not isinstance(a, numbers.Number):
            raise TypeError('Invalied number provided')
        return Decimal(min(1, max(a, -1)))

    def __add__(self, v):
        """ __add__: Sum of two Vectors

        Args:
            v: Vector object

        Returns:
            Vector object

        Raises:
            TypeError: if v is not a Vector

        """
        if not isinstance(v, Vector):
            raise TypeError('You can only add two vectors')
        return Vector([x + v.coordinates[i] for i, x in enumerate(self.coordinates)])

    # allow in reverse
    __radd__ = __add__


    def __sub__(self, v):
        """ __sub__: Subtration of two Vectors

        Args:
            v: Vector object

        Returns:
            Vector object

        Raises:
            TypeError: if v is not a Vector

        """
        if not isinstance(v, Vector):
            raise TypeError('You can only add two vectors')
        return Vector([x - v.coordinates[i] for i, x in enumerate(self.coordinates)])

    # allow in reverse
    __rsub__ = __sub__


    def __mul__(self, v):
        """ __mul__: cross product of two vectors or
            multiplication of a scalar with a vector

        Args:
            v: Vector object

        Returns:
            Vector

        Raises:
            TypeError: if v is not a vector or a number

        """
        if (isinstance(v, numbers.Number)):
            return Vector([x * v for x in self.coordinates])
        elif (isinstance(v, Vector)):
            return self.cross(v)
        raise TypeError('Argument must be number or a vector')

    # allow in reverse
    __rmul__ = __mul__


    def __str__(self):
        """ returns a string representation of a vector """
        return 'Vector: {}'.format(self.coordinates)

    # representation == string
    __repr__ = __str__


    def __eq__(self, v):
        """ checks the equality of two vectors """
        return self.coordinates == v.coordinates
