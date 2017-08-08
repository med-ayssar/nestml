"""
TODO header
@author kperun
"""
import ASTEquation
import ASTShape
import ASTOdeFunction


class ASTOdeDeclaration:
    """
    This class is used to store an arbitrary ODE declaration, e.g., a shape.
    """
    __equations = None
    __shapes = None
    __odeFunctions = None

    def __init__(self, _equations: list(ASTEquation) = list(), _shapes: list(ASTShape) = list(),
                 _odeFunctions: list(ASTOdeFunction) = list()):
        """
        Standard constructor.
        :param _equations: a list of ASTEquation elements.
        :type _equations: list(ASTEquation)
        :param _shapes: a list of ASTShape elements.
        :type _shapes: list(ASTShape)
        :param _odeFunctions: a list of ASTOdeFunction elements.
        :type _odeFunctions: list(ASTOdeFunction).
        """
        self.__equations = _equations
        self.__shapes = _shapes
        self.__odeFunctions = _odeFunctions

    @classmethod
    def makeASTOdeDeclaration(cls, _equations: list(ASTEquation) = list(), _shapes: list(ASTShape) = list(),
                              _odeFunctions: list(ASTOdeFunction) = list()):
        """
        A factory method used to generate new ASTOdeDeclaration.
        :param _equations: a list of ASTEquation elements.
        :type _equations: list(ASTEquation)
        :param _shapes: a list of ASTShape elements.
        :type _shapes: list(ASTShape)
        :param _odeFunctions: a list of ASTOdeFunction elements.
        :type _odeFunctions: list(ASTOdeFunction).
        """
        return cls(_equations, _shapes, _odeFunctions)

    def getEquations(self) -> list(ASTEquation):
        """
        Returns the list of stored equation objects.
        :return: a list of ASTEquation objects.
        :rtype: list(ASTEquation)
        """
        return self.__equations

    def getShapes(self) -> list(ASTShape):
        """
        Returns the list of stored shape objects.
        :return: a list of ASTShape objects.
        :rtype: list(ASTShape)
        """
        return self.__shapes

    def getOdeFunction(self) -> list(ASTOdeFunction):
        """
        Returns the list of stored ode function objects.
        :return: a list of ASTShape objects.
        :rtype: list(ASTOdeFunction)
        """
        return self.__odeFunctions
