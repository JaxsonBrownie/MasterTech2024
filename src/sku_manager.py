import json
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class SKU_Manager:
    def __init__(self, db_path: str = "sku_manager.json"):
        """Initialize the database with the given path."""
        # Convert relative path to absolute path
        self.db_path = os.path.abspath(db_path)
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.db_path) or '.', exist_ok=True)
        self.data = self._load_database()

    def _load_database(self) -> Dict:
        """Load the database from file or create a new one if it doesn't exist."""
        try:
            if os.path.exists(self.db_path):
                with open(self.db_path, 'r') as f:
                    return json.load(f)
            
            # Create new database with coordinate history
            initial_data = {
                "products": [],
                "metadata": {
                    "total_products": 0,
                    "last_updated": datetime.now().isoformat(),
                    "version": "1.0"
                }
            }
            
            # Immediately save the new database
            with open(self.db_path, 'w') as f:
                json.dump(initial_data, f, indent=4)
            
            return initial_data
            
        except Exception as e:
            print(f"Error loading/creating database: {str(e)}")
            raise

    def save_database(self):
        """Save the current database state to file."""
        try:
            with open(self.db_path, 'w') as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"Error saving database: {str(e)}")
            raise

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

        # Create product entry with coordinate history
        product = {
            "sku": sku,
            "product_id": product_id or f"P{len(self.data['products']) + 1:06d}",
            "name": name,
            "location": {
                "aisle": aisle_number,
                "shelf": shelf_number,
                "row": row_number
            },
            "coordinate_history": [
                {
                    "timestamp": datetime.now().isoformat(),
                    "coordinates": {
                        "bottom_left": {
                            "x": float(bottom_left_coord[0]),
                            "y": float(bottom_left_coord[1])
                        },
                        "top_right": {
                            "x": float(top_right_coord[0]),
                            "y": float(top_right_coord[1])
                        }
                    }
                }
            ]
        }

        self.data['products'].append(product)
        self.data['metadata']['total_products'] = len(self.data['products'])
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
        """Update coordinates for a specific product by adding to its history."""
        product = self.get_product_by_sku(sku)
        if product:
            # Add new coordinate entry to history
            new_coordinate = {
                "timestamp": datetime.now().isoformat(),
                "coordinates": {
                    "bottom_left": {
                        "x": float(bottom_left_coord[0]),
                        "y": float(bottom_left_coord[1])
                    },
                    "top_right": {
                        "x": float(top_right_coord[0]),
                        "y": float(top_right_coord[1])
                    }
                }
            }
            
            # Initialize coordinate_history if it doesn't exist
            if 'coordinate_history' not in product:
                product['coordinate_history'] = []
                
            product['coordinate_history'].append(new_coordinate)
            
            self.data['metadata']['last_updated'] = datetime.now().isoformat()
            self.save_database()
            return True
        return False

    def get_coordinate_history(self, sku: str) -> List[Dict]:
        """Get the complete coordinate history for a product."""
        product = self.get_product_by_sku(sku)
        if product and 'coordinate_history' in product:
            return product['coordinate_history']
        return []

    def delete_product(self, sku: str) -> bool:
        """Delete a product from the database."""
        initial_length = len(self.data['products'])
        self.data['products'] = [p for p in self.data['products'] if p['sku'] != sku]
        if len(self.data['products']) < initial_length:
            self.data['metadata']['total_products'] = len(self.data['products'])
            self.data['metadata']['last_updated'] = datetime.now().isoformat()
            self.save_database()
            return True
        return False