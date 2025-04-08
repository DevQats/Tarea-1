import pytest
from validaciones import valid_text, valid_descripcion, valid_stock, valid_precio, valid_usuario, valid_contraseña

@pytest.mark.parametrize(
    "nombre, expected",
    [   
        # Casos válidos
        ("Polera", True),
        ("Polera v123", True),

        # Casos inválidos
        ("Poler@ v123", False),
        ("!@#$", False),
    ]
)
def test_valid_text(nombre, expected):
    if expected:
        assert valid_text(nombre) is not None
    else:
        assert valid_text(nombre) is None 


@pytest.mark.parametrize(
    "input_desc, expected",
    [   #Casos válidos
        ("Descripción de prueba, con; punto.", True),
        ("Descripción de prueba, con; punto y número 123.", True),

        #Casos inválidos
        ("Descripción con @ en ella.", False),
        ("", False),
    ]
)


def test_valid_descripcion(input_desc, expected):
    if expected:
        assert valid_descripcion(input_desc) is not None
    else:
        assert valid_descripcion(input_desc) is None 


@pytest.mark.parametrize(
    "input_stock, expected",
    [
        (10, True),
        (0, True),
        (-1, False),
        ("10", False),
    ]
)
def test_valid_stock(input_stock, expected):
    assert valid_stock(input_stock) == expected


@pytest.mark.parametrize(
    "input_precio, expected",
    [
        (15000, True),
        (0, True),
        (-1, False),
        ("15000", False),
    ]
)
def test_valid_precio(input_precio, expected):
    assert valid_precio(input_precio) == expected


@pytest.mark.parametrize(
    "input_usuario, expected",
    [
        ("usuario123", True),
        ("usuario_123", True),
        ("us", False),
        ("usuario!@#", False),
    ]
)
def test_valid_usuario(input_usuario, expected):
    if expected:
        assert valid_usuario(input_usuario) is not None
    else:
        assert valid_usuario(input_usuario) is None

@pytest.mark.parametrize(
    "input_contraseña, expected",
    [   
        ("secreta", True),
        ("123", False),
        ("", False),
    ]
)
def test_valid_contraseña(input_contraseña, expected):
    assert valid_contraseña(input_contraseña) == expected
