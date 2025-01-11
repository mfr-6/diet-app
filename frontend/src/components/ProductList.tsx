import { useState, useEffect } from 'react';
import { Product } from '../lib/types';
import { getProducts, createProduct, updateProduct, deleteProduct } from '../lib/api';
import { ProductModal } from './ProductModal';

export function ProductList() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);

  useEffect(() => {
    loadProducts();
  }, []);

  async function loadProducts() {
    try {
      const data = await getProducts();
      setProducts(data);
      setError(null);
    } catch {
      setError('Failed to load products');
    } finally {
      setLoading(false);
    }
  }

  async function handleCreateProduct() {
    setSelectedProduct({ id: 0, name: '' });
  }

  async function handleSaveProduct(product: { name: string }) {
    try {
      if (selectedProduct?.id === 0) {
        const newProduct = await createProduct(product);
        setProducts([...products, newProduct]);
      } else if (selectedProduct) {
        const updated = await updateProduct(selectedProduct.id, product);
        setProducts(products.map(p => p.id === updated.id ? updated : p));
      }
      setSelectedProduct(null);
      setError(null);
    } catch {
      throw new Error('Failed to save product');
    }
  }

  async function handleDeleteProduct(id: number) {
    try {
      await deleteProduct(id);
      setProducts(products.filter(p => p.id !== id));
      setError(null);
    } catch {
      setError('Failed to delete product');
    }
  }

  if (loading) return <div>Loading...</div>;

  return (
    <div className="max-w-4xl mx-auto p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Products</h1>
        <button
          onClick={handleCreateProduct}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Add Product
        </button>
      </div>
      
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      <div className="space-y-4">
        {products.map(product => (
          <div key={product.id} className="border rounded p-4 flex items-center justify-between">
            <span className="text-lg">{product.name}</span>
            <div className="flex gap-2">
              <button
                onClick={() => setSelectedProduct(product)}
                className="bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600"
              >
                Edit
              </button>
              <button
                onClick={() => handleDeleteProduct(product.id)}
                className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>

      <ProductModal
        product={selectedProduct}
        onClose={() => setSelectedProduct(null)}
        onSave={handleSaveProduct}
      />
    </div>
  );
} 