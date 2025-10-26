from typing import Protocol


class PriceProvider(Protocol):
    """Protocolo para proveedores de precio (Dependency Inversion Principle)"""
    def get_current_price(self) -> float:
        ...


class Stock:
    """
    Representa una acción individual en el portfolio.
    
    Responsabilidad: Mantener información básica de una acción
    (símbolo, cantidad, precio actual).
    """
    
    def __init__(self, symbol: str, quantity: float, current_price: float):
        """
        Args:
            symbol: Símbolo de la acción (ej: "META", "AAPL")
            quantity: Cantidad de acciones poseídas
            current_price: Precio actual por acción
        """
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        if current_price < 0:
            raise ValueError("Current price cannot be negative")
            
        self._symbol = symbol
        self._quantity = quantity
        self._current_price = current_price
    
    @property
    def symbol(self) -> str:
        return self._symbol
    
    @property
    def quantity(self) -> float:
        return self._quantity
    
    @quantity.setter
    def quantity(self, value: float):
        if value < 0:
            raise ValueError("Quantity cannot be negative")
        self._quantity = value
    
    @property
    def current_price(self) -> float:
        return self._current_price
    
    @current_price.setter
    def current_price(self, value: float):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._current_price = value
    
    @property
    def total_value(self) -> float:
        """Valor total de la posición (cantidad × precio)"""
        return self._quantity * self._current_price
    
    def get_current_price(self) -> float:
        """Mantener para compatibilidad con PriceProvider protocol"""
        return self.current_price
    
    def __repr__(self) -> str:
        return f"Stock(symbol='{self._symbol}', quantity={self._quantity}, price={self._current_price})"
