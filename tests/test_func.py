import sqlite3
import pytest
import getpass
from unittest.mock import patch
from func import auth, add_user, add_producto, get_productos, update_producto, delete_producto, update_stock, lookup_producto, gen_report

@pytest.fixture
def setup_db():
    """Configuración de la base de datos en memoria antes de cada prueba."""
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE productos (
            sku INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            descripcion TEXT,
            cantidad INTEGER,
            precio REAL,
            categoria TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE usuarios (
            usuario TEXT PRIMARY KEY,
            contraseña TEXT NOT NULL
        )
    ''')
    conn.commit()

    yield conn

@patch('builtins.input', side_effect=['testuser'])
@patch('func.getpass')
def test_auth(mock_getpass, mock_input, setup_db):
    """Prueba para autenticar un usuario."""
    conn = setup_db
    mock_getpass.return_value = 'password123'
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios VALUES ('testuser', 'password123')")
    conn.commit()

    resultado = auth(conn)
    
    assert resultado is True

@patch('builtins.input', side_effect=['testuser'])
@patch('func.getpass')
def test_add_user(mock_getpass, mock_input, setup_db):
    """Prueba para agregar un usuario."""
    conn = setup_db
    mock_getpass.return_value = 'password123'
    add_user(conn)
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = 'testuser'")
    resultado = cursor.fetchone()

    assert resultado is not None
    assert resultado[0] == 'testuser'
    assert resultado[1] == 'password123'

@patch('builtins.input', side_effect=['Polera', 'Algodón', '10', '15000', 'Ropa'])
def test_add_producto(mock_input, setup_db):
    """Prueba para agregar un producto."""
    conn = setup_db
    add_producto(conn)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE nombre = 'Polera'")
    resultado = cursor.fetchone()

    assert resultado is not None
    assert resultado[1] == 'Polera'
    assert resultado[2] == 'Algodón'
    assert resultado[3] == 10
    assert resultado[4] == 15000
    assert resultado[5] == 'Ropa'

@patch('builtins.input', side_effect=['Polera', 'Algodón', '10', '15000', 'Ropa'])
def test_get_products(mock_input, setup_db, capsys):
    """Prueba para verificar que los productos se imprimen correctamente."""
    conn = setup_db

    add_producto(conn)
    
    get_productos(conn)
    
    captured = capsys.readouterr()
    output = captured.out
    
    assert "SKU: 1" in output
    assert "Nombre: Polera" in output
    assert "Descripción: Algodón" in output
    assert "Cantidad: 10" in output
    assert "Precio: $15000" in output
    assert "Categoría: Ropa" in output

@patch('builtins.input')
def test_update_producto(mock_input, setup_db):
    """Prueba para actualizar un producto."""
    conn = setup_db

    with patch('builtins.input', side_effect=['Polera', 'Algodón', '10', '15000', 'Ropa']):
        add_producto(conn)
    
    cursor = conn.cursor()
    cursor.execute("SELECT sku FROM productos WHERE nombre = 'Polera'")
    sku = cursor.fetchone()[0]
    
    input_values = [
        'Polera',
        'Algodón',
        '20',
        '16000',
        'Ropa'
    ]
    
    with patch('builtins.input', side_effect=input_values):
        update_producto(sku, conn)

    cursor.execute("SELECT cantidad, precio FROM productos WHERE sku = ?", (sku,))
    resultado = cursor.fetchone()
    
    assert resultado[0] == 20
    assert resultado[1] == 16000

@patch('builtins.input', side_effect=['Polera', 'Algodón', '10', '15000', 'Ropa'])
def test_delete_producto(mock_input, setup_db):
    """Prueba para eliminar un producto."""
    conn = setup_db
    
    add_producto(conn)
    cursor = conn.cursor()
    cursor.execute("SELECT sku FROM productos WHERE nombre = 'Polera'")
    sku = cursor.fetchone()[0]
    
    delete_producto(sku, conn)
    
    cursor.execute("SELECT * FROM productos WHERE sku = ?", (sku,))
    resultado = cursor.fetchone()
    
    assert resultado is None

@patch('builtins.input')
def test_update_stock(mock_input, setup_db):
    """Prueba para actualizar el stock de un producto (añadir stock)."""
    conn = setup_db
    
    with patch('builtins.input', side_effect=['Polera', 'Algodón', '10', '15000', 'Ropa']):
        add_producto(conn)
    
    cursor = conn.cursor()
    cursor.execute("SELECT sku, cantidad FROM productos WHERE nombre = 'Polera'")
    sku, cantidad_inicial = cursor.fetchone()
    
    mock_input.side_effect = [str(sku), '15']
    
    update_stock(1, conn)
    
    cursor.execute("SELECT cantidad FROM productos WHERE sku = ?", (sku,))
    nueva_cantidad = cursor.fetchone()[0]
    
    assert nueva_cantidad == cantidad_inicial + 15

@patch('builtins.input')
def test_lookup_producto(mock_input, setup_db, capsys):
    """Prueba para buscar un producto."""
    conn = setup_db

    with patch('builtins.input', side_effect=['Polera', 'Algodón', '10', '15000', 'Ropa']):
        add_producto(conn)
    
    mock_input.side_effect = ['1', 'Polera']
    
    lookup_producto(conn)
    
    captured = capsys.readouterr()
    output = captured.out
    
    assert "SKU: 1" in output
    assert "Nombre: Polera" in output

@patch('builtins.input')
def test_gen_report(mock_input, setup_db, capsys):
    """Prueba para generar un reporte."""
    conn = setup_db
    
    with patch('builtins.input', side_effect=['Polera', 'Algodón', '10', '15000', 'Ropa']):
        add_producto(conn)
    
    gen_report(conn)

    captured = capsys.readouterr()
    output = captured.out
    
    assert "10 productos en inventario" in output
    assert "Valor total del inventario: $150000" in output
    assert "Productos sin stock:" not in output
