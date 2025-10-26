# Portfolio Rebalancing System

Sistema simple para rebalancear un portfolio de inversiones basado en una distribución objetivo.

## Qué hace

El programa te ayuda a calcular qué acciones necesitas comprar o vender para mantener tu portfolio balanceado según los porcentajes que quieras tener de cada acción.

Por ejemplo, si quieres tener 40% META, 40% AAPL y 20% GOOGL, pero actualmente tienes 38% META, 48% AAPL y 13% GOOGL, el programa te dice exactamente cuántas acciones comprar o vender de cada una.

## Estructura del proyecto

```
models/
  - stock.py          Representa una acción individual con su precio y cantidad
  - portfolio.py      Contiene todas las acciones y la distribución objetivo

services/
  - rebalance_service.py    Hace los cálculos de qué comprar/vender

main.py               Ejemplo de cómo usar el sistema
```

## Cómo usar

Para ejecutar el ejemplo:

```
python main.py
```

El ejemplo muestra:
1. Crear un portfolio con algunas acciones
2. Definir qué porcentaje quieres de cada una
3. Calcular qué necesitas comprar o vender
4. Aplicar los cambios
5. Ver cómo queda balanceado

## Ejemplo de código

```python
from models.portfolio import Portfolio
from services.rebalance_service import RebalanceService

# Crear portfolio
portfolio = Portfolio()
portfolio.add_stock("META", quantity=20, current_price=300.0)
portfolio.add_stock("AAPL", quantity=50, current_price=150.0)

# Definir distribución deseada
target = {
    "META": 0.40,  # 40%
    "AAPL": 0.60   # 60%
}

# Calcular qué hacer
rebalancer = RebalanceService()
actions = rebalancer.calculate_rebalance(portfolio, target)

# Ver las acciones recomendadas
for action in actions:
    print(f"{action.action} {action.quantity:.2f} shares of {action.symbol}")
```

## Principios aplicados

El código está organizado siguiendo SOLID:
- Cada clase tiene una responsabilidad clara
- Stock maneja información de una acción
- Portfolio maneja la colección de acciones
- RebalanceService hace los cálculos de rebalanceo

## Requisitos

Python 3.8 o superior. No necesita librerías externas.
