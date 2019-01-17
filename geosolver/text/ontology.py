from geosolver.text.ontology_states import FunctionSignature

__author__ = 'minjoon'

def add_function_signature(signatures, signature_tuple):
    print(signatures)
    if len(signature_tuple) == 3:
        name, return_type, arg_types = signature_tuple
        is_symmetric = False
    elif len(signature_tuple) == 4:
        name, return_type, arg_types, is_symmetric = signature_tuple
    assert name not in signatures
    signatures[name] = FunctionSignature(name, return_type, arg_types, is_symmetric)

def issubtype(child, parent):
    if child == 'variable' and parent == 'number':
        return True
    if child in ['triangle', 'quad'] and parent == 'polygon':
        return True
    if child in ['line', 'circle', 'triangle', 'quad'] and parent == 'entity':
        return True
    if child in ['circle', 'triangle', 'quad'] and parent == 'circle+polygon':
        return True
    return child == parent


types = ['root', 'start', 'number', 'modifier', 'circle', 'line', 'truth', 'point', 'quad', 'arc','tangent']
function_signatures = {}
tuples = (
    ('all', 'modifier', []),
    ('Angle', 'angle', ['modifier']),
    ('angle', 'angle', []),
    ('AngleOf', 'number', ['angle']),
    ('AngleOfArc', 'number', ['arc']),
    ('AreaOf', 'number', ['circle+polygon']),
    ('Arc', 'arc', []),
    ('BisectsLine', 'truth', ['line', 'line']),
    ('BisectsAngle', 'truth', ['line', 'angle']),
    ('CC', 'truth', ['line', 'line']),
    ('Circle', 'circle', ['modifier']),
    ('circle', 'circle', []),
    ('DiameterOf', 'number', ['circle']),
    ('entity', 'entity', []),
    ('Equal', 'truth', ['number', 'number'], True),
    ('Equals', 'truth', ['number', 'number'], True),
    ('Equilateral', 'truth', ['triangle']),
    ('Find', 'truth', ['number']),
    ('IntersectAt', 'truth', ['line', 'point'], True),
    ('Intersects', 'truth', ['entity', 'entity'], True),
    ('Is', 'truth', ['point', 'point']),
    ('Is', 'truth', ['number', 'Which']),
    ('IsAngle', 'truth', ['angle']),
    ('IsAltitude', 'truth', ['line', 'triangle']),
    ('IsAltitudeOf', 'truth', ['line', 'triangle']),
    ('IsChord', 'truth', ['line', 'circle']),
    ('IsChordOf', 'truth', ['line']),
    ('IsCircle', 'truth', ['circle']),
    ('IsDiameter', 'truth', ['line', 'circle']),
    ('IsDiameterLineOf', 'truth', ['line']),
    ('IsHypotenuse', 'truth', ['line', 'triangle']),
    ('IsLine', 'truth', ['line']),
    ('IsMedian', 'truth', ['line', 'triangle']),
    ('IsMidpoint', 'truth', ['point', 'line']),
    ('IsMidpointOf', 'truth', ['point', 'line']),
    ('Isosceles', 'truth', ['triangle']),
    ('IsParallelogram', 'truth', ['quad']),
    ('IsPoint', 'truth', ['point']),
    ('IsRadius', 'truth', ['line', 'circle']),
    ('IsRhombus', 'truth', ['quad']),
    ('IsRight', 'truth', ['triangle']),
    ('IsRightTriangle', 'truth', ['triangle']),
    ('IsSecant', 'truth', ['line', 'circle']),
    ('IsSideOf', 'truth', ['line']),
    ('IsSquare', 'truth', ['quad']),
    ('IsTriangle', 'truth', ['triangle']),
    ('LengthOf', 'number', ['line']),
    ('Line', 'line', ['modifier']),
    ('line', 'line', []),
    ('Not', 'truth', [], False),  
    ('number', 'number', []),
    ('On', 'truth', ['point', 'line']),
    ('Parallel', 'truth', ['line', 'line'], True),
    ('PerimeterOf', 'number', ['polygon']),
    ('Perpendicular', 'truth', ['line', 'line'], True),
    ('Point', 'point', ['modifier']),
    ('point', 'point', []),
    ('PointLiesOnLine', 'truth', ['point', 'line']),
    ('quad', 'quad', []),
    ('Quad', 'quad', ['modifier']),
    ('RadiusOf', 'number', ['circle']),
    ('Root', 'root', ['start']),
    ('side', 'side', []),
    ('StartTruth', 'start', ['truth']),
    ('Tangent', 'truth', ['line', 'circle']),
    ('the', 'modifier', []),
    ('Triangle', 'triangle', ['modifier']),
    ('True', 'truth', [], True),  
    ('Two', 'truth', ['tangent']),  
    ('Secant', 'truth', ['line', 'circle']),    
    #('Equivalent')
    # ('Add', 'number', ['number', 'number']),
    ('unkNum', 'number', []),
    ('unkSt', 'truth', []),
    ('Which', 'Which', []),
    ('What', 'What', []),
)
for tuple_ in tuples:
    add_function_signature(function_signatures, tuple_)
