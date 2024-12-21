# diet-app

Features:

1. CRUD: Ingredients

-> Product
    - name
    - weight
    - protein: float
    - fats: float
    - carbs: float
    - kcal (per 100g)
    - barcode: str

////////////////////////////////
2. CRUD: Meals

-> Ingredient
    - product: Product
    - weight: int

-> Meal
    - ingredients: List[Ingredient]
    - recipe
