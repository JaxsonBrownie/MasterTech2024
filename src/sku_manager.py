import json
import os
from typing import Dict, List, Optional, Tuple

class SKU_Manager:
    def __init__(self, db_path: str = "sku_manager.json"):
        """Initialize the database with the given path."""
        self.db_path = db_path
        self.data = self._load_database()

    def _load_database(self) -> Dict:
        """Load the database from file or create a new one if it doesn't exist."""
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                return json.load(f)
        return {
            "products": [],
            "metadata": {
                "total_products": 0,
                "last_updated": None,
                "version": "1.0"
            }
        }

    def save_database(self):
        """Save the current database state to file."""
        with open(self.db_path, 'w') as f:
            json.dump(self.data, f, indent=4)

    def add_product(self, 
                   sku: str,
                   name: str,
                   aisle_number: int,
                   shelf_number: int,  # 1-10
                   row_number: int,    # 1-5
                   bottom_left_coord: Tuple[float, float],
                   top_right_coord: Tuple[float, float],
                   product_id: Optional[str] = None) -> bool:
        """
        Add a new product to the database.
        Returns True if successful, False if product with SKU already exists.
        """
        # Validate input
        if not (1 <= shelf_number <= 10 and 1 <= row_number <= 5):
            raise ValueError("Shelf number must be 1-10 and row number must be 1-5")

        # Check if product already exists
        if any(p['sku'] == sku for p in self.data['products']):
            return False

        # Create product entry
        product = {
            "sku": sku,
            "product_id": product_id or f"P{len(self.data['products']) + 1:06d}",
            "name": name,
            "location": {
                "aisle": aisle_number,
                "shelf": shelf_number,
                "row": row_number
            },
            "coordinates": {
                "bottom_left": {
                    "x": bottom_left_coord[0],
                    "y": bottom_left_coord[1]
                },
                "top_right": {
                    "x": top_right_coord[0],
                    "y": top_right_coord[1]
                }
            }
        }

        self.data['products'].append(product)
        self.data['metadata']['total_products'] = len(self.data['products'])
        from datetime import datetime
        self.data['metadata']['last_updated'] = datetime.now().isoformat()
        self.save_database()
        return True

    def get_product_by_sku(self, sku: str) -> Optional[Dict]:
        """Retrieve a product by its SKU."""
        for product in self.data['products']:
            if product['sku'] == sku:
                return product
        return None

    def get_products_by_location(self, aisle: int, shelf: Optional[int] = None, row: Optional[int] = None) -> List[Dict]:
        """Find all products in a specific location."""
        products = []
        for product in self.data['products']:
            loc = product['location']
            if loc['aisle'] == aisle:
                if shelf is None or loc['shelf'] == shelf:
                    if row is None or loc['row'] == row:
                        products.append(product)
        return products

    def update_product_coordinates(self, 
                                 sku: str, 
                                 bottom_left_coord: Tuple[float, float],
                                 top_right_coord: Tuple[float, float]) -> bool:
        """Update the coordinates for a specific product."""
        product = self.get_product_by_sku(sku)
        if product:
            product['coordinates']['bottom_left'] = {"x": bottom_left_coord[0], "y": bottom_left_coord[1]}
            product['coordinates']['top_right'] = {"x": top_right_coord[0], "y": top_right_coord[1]}
            self.save_database()
            return True
        return False

    def delete_product(self, sku: str) -> bool:
        """Delete a product from the database."""
        initial_length = len(self.data['products'])
        self.data['products'] = [p for p in self.data['products'] if p['sku'] != sku]
        if len(self.data['products']) < initial_length:
            self.data['metadata']['total_products'] = len(self.data['products'])
            self.save_database()
            return True
        return False

# Example usage
if __name__ == "__main__":
    # Initialize database
    db = SKU_Manager()
    
    # Add a sample product
    db.add_product(
        sku="12345",
        name="Organic Bananas",
        aisle_number=3,
        shelf_number=2,
        row_number=3,
        bottom_left_coord=(0.0, 0.0),
        top_right_coord=(2.5, 1.8),
        product_id="BNAN001"
    )
    
    # Example JSON structure of a single product
    example_product = {
        "sku": "12345",
        "product_id": "BNAN001",
        "name": "Organic Bananas",
        "location": {
            "aisle": 3,
            "shelf": 2,
            "row": 3
        },
        "coordinates": {
            "bottom_left": {
                "x": 0.0,
                "y": 0.0
            },
            "top_right": {
                "x": 2.5,
                "y": 1.8
            }
        }
    }
    
    print("Example product structure:")
    print(json.dumps(example_product, indent=4))
