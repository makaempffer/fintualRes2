from typing import Dict, Optional
from models.stock import Stock


class Portfolio:
    """
    Representa un portfolio de inversiones con una colección de acciones
    y una asignación objetivo.
    
    Responsabilidad: Gestionar la colección de acciones y mantener
    la configuración de asignación objetivo del portfolio.
    """
    
    def __init__(self, total_value: Optional[float] = None):
        """
        Args:
            total_value: Valor total inicial del portfolio (opcional)
        """
        self._stocks: Dict[str, Stock] = {}
        self._target_allocation: Dict[str, float] = {}
        self._initial_value = total_value
    
    def add_stock(self, symbol: str, quantity: float, current_price: float):
        """
        Añade una acción al portfolio.
        
        Args:
            symbol: Símbolo de la acción
            quantity: Cantidad de acciones
            current_price: Precio actual por acción
        """
        if symbol in self._stocks:
            raise ValueError(f"Stock {symbol} already exists in portfolio")
        
        self._stocks[symbol] = Stock(symbol, quantity, current_price)
    
    def remove_stock(self, symbol: str):
        """Elimina una acción del portfolio"""
        if symbol not in self._stocks:
            raise ValueError(f"Stock {symbol} not found in portfolio")
        del self._stocks[symbol]
    
    def get_stock(self, symbol: str) -> Optional[Stock]:
        """Obtiene una acción específica del portfolio"""
        return self._stocks.get(symbol)
    
    def get_all_stocks(self) -> Dict[str, Stock]:
        """Retorna todas las acciones del portfolio"""
        return self._stocks.copy()
    
    def update_stock_price(self, symbol: str, new_price: float):
        """Actualiza el precio de una acción específica"""
        stock = self.get_stock(symbol)
        if stock is None:
            raise ValueError(f"Stock {symbol} not found in portfolio")
        stock.current_price = new_price
    
    def set_target_allocation(self, target_allocation: Dict[str, float]):
        """
        Define la asignación objetivo del portfolio.
        
        Args:
            target_allocation: Distribución deseada por símbolo (ej: {"META": 0.4, "AAPL": 0.6})
        """
        total = sum(target_allocation.values())
        if not (0.99 <= total <= 1.01):
            raise ValueError(f"Total allocation must sum to 1.0, got {total}")
        
        for symbol in target_allocation.keys():
            if symbol not in self._stocks:
                raise ValueError(f"Stock {symbol} not found in portfolio")
        
        self._target_allocation = target_allocation.copy()
    
    def get_target_allocation(self) -> Dict[str, float]:
        return self._target_allocation.copy()
    
    @property
    def total_value(self) -> float:
        """Valor total actual del portfolio"""
        return sum(stock.total_value for stock in self._stocks.values())
    
    @property
    def current_allocation(self) -> Dict[str, float]:
        """Distribución actual del portfolio basada en valores presentes"""
        if self.total_value == 0:
            return {symbol: 0.0 for symbol in self._stocks.keys()}
        
        return {
            symbol: stock.total_value / self.total_value
            for symbol, stock in self._stocks.items()
        }
    
    def __repr__(self) -> str:
        return f"Portfolio(stocks={len(self._stocks)}, total_value={self.total_value:.2f})"
