from typing import Dict, List, NamedTuple
from models.portfolio import Portfolio


class RebalanceAction(NamedTuple):
    """
    Representa una acción de rebalanceo (compra o venta).
    
    Attributes:
        symbol: Símbolo de la acción
        action: Tipo de acción ("BUY" o "SELL")
        quantity: Cantidad de acciones a comprar/vender
        value: Valor monetario de la transacción
    """
    symbol: str
    action: str
    quantity: float
    value: float


class RebalanceService:
    """
    Servicio encargado de calcular las operaciones necesarias
    para rebalancear un portfolio según su asignación objetivo.
    
    Responsabilidad: Implementar la lógica de rebalanceo
    (Single Responsibility Principle).
    """
    
    def calculate_rebalance(
        self, 
        portfolio: Portfolio, 
        target_allocation: Dict[str, float]
    ) -> List[RebalanceAction]:
        """
        Calcula las operaciones de compra/venta necesarias para
        alcanzar la asignación objetivo.
        
        Args:
            portfolio: Portfolio a rebalancear
            target_allocation: Asignación objetivo (ej: {"META": 0.4, "AAPL": 0.6})
        
        Returns:
            Lista de acciones de rebalanceo ordenadas (ventas primero, luego compras)
        
        Algoritmo:
        1. Calcula el valor total actual del portfolio
        2. Para cada acción, determina el valor objetivo basado en la asignación
        3. Compara valor actual vs valor objetivo
        4. Genera acciones de SELL para posiciones sobreponderadas
        5. Genera acciones de BUY para posiciones subponderadas
        """
        portfolio.set_target_allocation(target_allocation)
        
        total_value = portfolio.total_value
        if total_value == 0:
            raise ValueError("Cannot rebalance portfolio with zero value")
        
        actions: List[RebalanceAction] = []
        stocks = portfolio.get_all_stocks()
        
        for symbol, target_percentage in target_allocation.items():
            stock = stocks.get(symbol)
            if stock is None:
                raise ValueError(f"Stock {symbol} not found in portfolio")
            
            current_value = stock.total_value
            target_value = total_value * target_percentage
            difference = target_value - current_value
            
            # Si la diferencia es significativa (más de 0.01 para evitar ruido de redondeo)
            if abs(difference) > 0.01:
                current_price = stock.current_price
                quantity_change = difference / current_price
                
                if difference > 0:
                    # Necesitamos comprar más de esta acción
                    actions.append(RebalanceAction(
                        symbol=symbol,
                        action="BUY",
                        quantity=quantity_change,
                        value=difference
                    ))
                else:
                    # Necesitamos vender parte de esta acción
                    actions.append(RebalanceAction(
                        symbol=symbol,
                        action="SELL",
                        quantity=abs(quantity_change),
                        value=abs(difference)
                    ))
        
        # Ordenar: ventas primero, luego compras
        actions.sort(key=lambda x: (x.action == "BUY", x.symbol))
        
        return actions
    
    def apply_rebalance(
        self, 
        portfolio: Portfolio, 
        actions: List[RebalanceAction]
    ):
        """
        Aplica las acciones de rebalanceo al portfolio.
        
        Args:
            portfolio: Portfolio a modificar
            actions: Lista de acciones a aplicar
        """
        for action in actions:
            stock = portfolio.get_stock(action.symbol)
            if stock is None:
                raise ValueError(f"Stock {action.symbol} not found")
            
            if action.action == "BUY":
                stock.quantity += action.quantity
            elif action.action == "SELL":
                if stock.quantity < action.quantity:
                    raise ValueError(
                        f"Cannot sell {action.quantity} shares of {action.symbol}, "
                        f"only {stock.quantity} available"
                    )
                stock.quantity -= action.quantity
