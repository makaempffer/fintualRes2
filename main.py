"""
Ejemplo de uso del sistema de rebalanceo de portfolio.

Este script demuestra cómo:
1. Crear un portfolio con múltiples acciones
2. Definir una asignación objetivo
3. Calcular las operaciones necesarias para rebalancear
4. Aplicar el rebalanceo y verificar el resultado
"""

from models.portfolio import Portfolio
from services.rebalance_service import RebalanceService


def print_separator():
    print("\n" + "=" * 80 + "\n")


def print_portfolio_status(portfolio: Portfolio):
    """Imprime el estado actual del portfolio"""
    print(f"Portfolio Total Value: ${portfolio.total_value:,.2f}")
    print("\nCurrent Holdings:")
    print(f"{'Symbol':<10} {'Quantity':<15} {'Price':<15} {'Value':<15} {'Allocation':<15}")
    print("-" * 80)
    
    stocks = portfolio.get_all_stocks()
    current_allocation = portfolio.current_allocation
    
    for symbol, stock in stocks.items():
        value = stock.total_value
        allocation = current_allocation[symbol]
        print(
            f"{symbol:<10} "
            f"{stock.quantity:<15.2f} "
            f"${stock.current_price:<14.2f} "
            f"${value:<14.2f} "
            f"{allocation * 100:<14.2f}%"
        )


def print_rebalance_actions(actions):
    """Imprime las acciones de rebalanceo calculadas"""
    print("\nRebalance Actions Required:")
    print(f"{'Action':<10} {'Symbol':<10} {'Quantity':<15} {'Value':<15}")
    print("-" * 80)
    
    for action in actions:
        print(
            f"{action.action:<10} "
            f"{action.symbol:<10} "
            f"{action.quantity:<15.2f} "
            f"${action.value:<14.2f}"
        )


def main():
    print_separator()
    print("PORTFOLIO REBALANCING SYSTEM - DEMONSTRATION")
    print_separator()
    
    # Escenario: Portfolio inicial desbalanceado
    print("STEP 1: Creating Initial Portfolio")
    print("-" * 80)
    
    portfolio = Portfolio()
    
    # Agregar acciones al portfolio con diferentes valores
    portfolio.add_stock("META", quantity=20, current_price=300.0)
    portfolio.add_stock("AAPL", quantity=50, current_price=150.0)
    portfolio.add_stock("GOOGL", quantity=15, current_price=140.0)
    
    print_portfolio_status(portfolio)
    
    print_separator()
    print("STEP 2: Defining Target Allocation")
    print("-" * 80)
    
    # Definir asignación objetivo: 40% META, 40% AAPL, 20% GOOGL
    target_allocation = {
        "META": 0.40,
        "AAPL": 0.40,
        "GOOGL": 0.20
    }
    
    print("\nTarget Allocation:")
    for symbol, percentage in target_allocation.items():
        print(f"  {symbol}: {percentage * 100:.1f}%")
    
    print_separator()
    print("STEP 3: Calculating Rebalance Actions")
    print("-" * 80)
    
    rebalancer = RebalanceService()
    actions = rebalancer.calculate_rebalance(portfolio, target_allocation)
    
    if not actions:
        print("\nPortfolio is already balanced! No actions needed.")
    else:
        print_rebalance_actions(actions)
        
        # Mostrar resumen
        total_buys = sum(action.value for action in actions if action.action == "BUY")
        total_sells = sum(action.value for action in actions if action.action == "SELL")
        
        print(f"\nSummary:")
        print(f"  Total to SELL: ${total_sells:,.2f}")
        print(f"  Total to BUY:  ${total_buys:,.2f}")
    
    print_separator()
    print("STEP 4: Applying Rebalance")
    print("-" * 80)
    
    rebalancer.apply_rebalance(portfolio, actions)
    print("\nRebalance applied successfully!")
    
    print_portfolio_status(portfolio)
    
    # Verificar que la asignación es correcta
    print("\nVerifying Target Allocation:")
    current_allocation = portfolio.current_allocation
    target_allocation_result = portfolio.get_target_allocation()
    
    print(f"{'Symbol':<10} {'Target':<15} {'Actual':<15} {'Difference':<15}")
    print("-" * 80)
    
    for symbol in target_allocation_result.keys():
        target_pct = target_allocation_result[symbol] * 100
        actual_pct = current_allocation[symbol] * 100
        diff = abs(target_pct - actual_pct)
        print(
            f"{symbol:<10} "
            f"{target_pct:<14.2f}% "
            f"{actual_pct:<14.2f}% "
            f"{diff:<14.4f}%"
        )
    
    print_separator()
    print("STEP 5: Simulating Price Changes")
    print("-" * 80)
    
    print("\nSimulating market price changes...")
    portfolio.update_stock_price("META", 320.0)
    portfolio.update_stock_price("AAPL", 145.0)
    portfolio.update_stock_price("GOOGL", 155.0)
    
    print_portfolio_status(portfolio)
    
    print("\nCalculating new rebalance after price changes...")
    new_actions = rebalancer.calculate_rebalance(portfolio, target_allocation)
    
    if new_actions:
        print_rebalance_actions(new_actions)
    else:
        print("\nNo rebalance needed despite price changes!")
    
    print_separator()
    print("DEMONSTRATION COMPLETED")
    print_separator()


if __name__ == "__main__":
    main()
