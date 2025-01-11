import { Product, ProductCreate, ProductSchema } from './types';

const API_URL = '/api/v1';

export async function getProducts(): Promise<Product[]> {
  const response = await fetch(`${API_URL}/products/`);
  if (!response.ok) {
    throw new Error('Failed to fetch products');
  }
  const data = await response.json();
  return data.map((item: unknown) => ProductSchema.parse(item));
}

export async function createProduct(product: ProductCreate): Promise<Product> {
  const response = await fetch(`${API_URL}/products/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(product),
  });
  if (!response.ok) {
    throw new Error('Failed to create product');
  }
  const data = await response.json();
  return ProductSchema.parse(data);
}

export async function updateProduct(id: number, product: ProductCreate): Promise<Product> {
  const response = await fetch(`${API_URL}/products/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(product),
  });
  if (!response.ok) {
    throw new Error('Failed to update product');
  }
  const data = await response.json();
  return ProductSchema.parse(data);
}

export async function deleteProduct(id: number): Promise<void> {
  const response = await fetch(`${API_URL}/products/${id}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    throw new Error('Failed to delete product');
  }
} 