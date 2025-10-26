# Conversación con LLM durante el desarrollo

## Código inicial

Empecé con una implementación básica que tenía una sola clase Portfolio. El código funcionaba pero tenía algunos problemas de diseño que fui identificando con ayuda del LLM.

Código inicial que hice:
- Una clase Portfolio que manejaba todo
- Métodos con nombres como get_total_value(), get_current_allocation()
- Los precios estaban guardados en el portfolio directamente
- No había separación clara de responsabilidades

## Problemas que identifiqué

Mientras revisaba el código me di cuenta de varios temas:

1. El portfolio estaba haciendo demasiadas cosas. Tenía las acciones, los precios, la lógica de rebalanceo, todo mezclado.

2. Los nombres de variables podían confundir. Por ejemplo, usaba "allocation" para referirme tanto a la distribución actual como a la objetivo, y eso hacía que tuviera que leer el código varias veces para entender.

3. Estaba usando get_total_value() y otros métodos al estilo Java, cuando en Python es más común usar properties.

## Cambios que hice con ayuda del LLM

### Separar en múltiples clases

Le pregunté al LLM cómo podía mejorar la estructura y me sugirió separar responsabilidades:

- Crear una clase Stock que maneje la información de cada acción individual (precio, cantidad)
- Dejar Portfolio solo para manejar la colección de stocks
- Crear un servicio aparte para la lógica de rebalanceo

Esto tiene sentido porque el precio es un atributo de la acción, no del portfolio.

### Mejorar nombres de variables

El LLM me ayudó a ver dónde los nombres eran ambiguos. Por ejemplo:

Antes:
```python
def set_target_allocation(self, allocation: Dict[str, float]):
    current = self.get_current_allocation()
```

Después:
```python
def set_target_allocation(self, target_allocation: Dict[str, float]):
    current = self.current_allocation
```

Ahora es obvio cuál es la distribución actual y cuál es la objetivo.

### Usar properties en vez de getters

Le comenté que había visto código Python usando properties y me explicó que es más idiomático. Entonces cambié:


# Antes
value = stock.get_total_value()
price = stock.get_current_price()

# Después  
value = stock.total_value
price = stock.current_price

Se lee mucho más natural y limpio.

### Agregar type hints

El LLM me recordó que aunque Python no los requiere, los type hints son buena práctica. Agregué tipos a todos los métodos:

```python
def calculate_rebalance(
    self, 
    portfolio: Portfolio, 
    target_allocation: Dict[str, float]
) -> List[RebalanceAction]:
```

Esto ayuda a que el IDE me avise si meto la pata con los tipos.

### Comentarios más útiles

Tenía muchos comentarios que solo repetían lo que el código ya decía. El LLM me ayudó a identificar cuáles eran útiles y cuáles no:

Eliminé:
```python
def get_total_value(self) -> float:
    """Retorna el valor total"""  # esto esta de mas
```

Mantuve:
```python
# Si la diferencia es significativa (más de 0.01 para evitar ruido de redondeo)
if abs(difference) > 0.01:
```

Porque este explica el "por qué" del 0.01.

## Resultado final

El código quedó mucho más limpio y fácil de entender:

- Cada clase tiene una responsabilidad clara
- Los nombres no dejan duda de qué representan
- Usa convenciones de Python (properties, type hints)
- Los comentarios solo están donde realmente ayudan

La verdad es que el código original funcionaba, pero estos cambios lo hacen mucho más mantenible y profesional. Si alguien más (o yo en 6 meses) tiene que modificarlo, va a ser mucho más fácil entender qué hace cada parte.

## Herramientas usadas

- Python 3.x
- VS Code
- GitHub Copilot para ayudar con sugerencias y revisar la estructura
- Type hints de la librería typing estándar de Python


# Ayudas adicionales
- Me ayudé también a haciendo preguntas de cómo hacer ciertas cosas propias de python,
que yo las considero como "buenas prácticas", ya que inicialmente me gustaría hacer esto en java pero no tengo tiempo.

