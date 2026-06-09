from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from langchain_core.tools import tool


class ShoppingDataStore:
    """Student scaffold for mock-data lookup."""

    def __init__(self, json_path: Path) -> None:
        if not json_path.exists():
            raise FileNotFoundError(f"Mock data file not found at {json_path}")
        
        data = json.loads(json_path.read_text(encoding="utf-8"))
        self.metadata = data.get("metadata", {})
        self.customers_list = data.get("customers", [])
        self.orders_list = data.get("orders", [])
        self.vouchers_list = data.get("vouchers", [])
        
        # Build indexes
        self.customer_by_id = {c["customer_id"]: c for c in self.customers_list}
        self.order_by_id = {o["order_id"]: o for o in self.orders_list}
        
        # Group orders by customer
        self.orders_by_customer = {}
        for o in self.orders_list:
            c_id = o["customer_id"]
            if c_id not in self.orders_by_customer:
                self.orders_by_customer[c_id] = []
            self.orders_by_customer[c_id].append(o)
            
        # Sort each customer's orders by created_at descending
        for c_id in self.orders_by_customer:
            self.orders_by_customer[c_id].sort(key=lambda x: x.get("created_at", ""), reverse=True)
            
        # Group vouchers by customer
        self.vouchers_by_customer = {}
        for v in self.vouchers_list:
            c_id = v["customer_id"]
            if c_id not in self.vouchers_by_customer:
                self.vouchers_by_customer[c_id] = []
            self.vouchers_by_customer[c_id].append(v)

    def get_customer_by_id(self, customer_id: str) -> dict[str, Any]:
        if customer_id not in self.customer_by_id:
            return {"status": "not_found", "customer_id": customer_id}
        return {"status": "ok", "customer": self.customer_by_id[customer_id]}

    def get_orders_by_customer_id(self, customer_id: str, limit: int = 10) -> dict[str, Any]:
        if customer_id not in self.customer_by_id:
            return {"status": "not_found", "customer_id": customer_id}
        orders = self.orders_by_customer.get(customer_id, [])[:limit]
        return {"status": "ok", "orders": orders}

    def get_order_detail_by_order_id(self, order_id: str) -> dict[str, Any]:
        if order_id not in self.order_by_id:
            return {"status": "not_found", "order_id": order_id}
        return {"status": "ok", "order": self.order_by_id[order_id]}

    def get_vouchers_by_customer_id(
        self,
        customer_id: str,
        only_active: bool = False,
    ) -> dict[str, Any]:
        if customer_id not in self.customer_by_id:
            return {"status": "not_found", "customer_id": customer_id}
        vouchers = self.vouchers_by_customer.get(customer_id, [])
        if only_active:
            vouchers = [
                v for v in vouchers
                if v.get("status") in ("active", "restored") and v.get("remaining_uses", 0) > 0
            ]
        return {"status": "ok", "vouchers": vouchers}


def build_data_tools(store: ShoppingDataStore) -> list:
    @tool
    def get_customer_by_id(customer_id: str) -> dict[str, Any]:
        """Tra cứu thông tin chi tiết của khách hàng theo mã khách hàng (customer_id), ví dụ 'C001'."""
        return store.get_customer_by_id(customer_id)

    @tool
    def get_orders_by_customer_id(customer_id: str, limit: int = 10) -> dict[str, Any]:
        """Tra cứu danh sách đơn hàng gần đây của khách hàng theo mã khách hàng (customer_id), sắp xếp theo thứ tự mới nhất."""
        return store.get_orders_by_customer_id(customer_id, limit)

    @tool
    def get_order_detail_by_order_id(order_id: str) -> dict[str, Any]:
        """Tra cứu thông tin chi tiết của một đơn hàng theo mã đơn hàng (order_id), ví dụ '1971' hoặc '2058'."""
        return store.get_order_detail_by_order_id(order_id)

    @tool
    def get_vouchers_by_customer_id(customer_id: str, only_active: bool = False) -> dict[str, Any]:
        """Tra cứu danh sách voucher của khách hàng theo mã khách hàng (customer_id). Nếu only_active=True, chỉ lấy các voucher còn sử dụng được (status là active hoặc restored và remaining_uses > 0)."""
        return store.get_vouchers_by_customer_id(customer_id, only_active)

    return [
        get_customer_by_id,
        get_orders_by_customer_id,
        get_order_detail_by_order_id,
        get_vouchers_by_customer_id,
    ]
