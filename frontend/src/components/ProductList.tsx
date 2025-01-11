import { useQuery } from '@tanstack/react-query';
import { api } from '../lib/api';
import { Product, ProductSchema } from '../lib/types';

export function ProductList() {
  const { data: products, isLoading, error } = useQuery({
    queryKey: ['products'],
    queryFn: async (): Promise<Product[]> => {
      const response = await api.get('/products');
      return z.array(ProductSchema).parse(response.data);
    },
  });

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading products</div>;

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">Products</h2>
      <ul className="space-y-2">
        {products?.map((product) => (
          <li 
            key={product.id}
            className="p-3 bg-white rounded shadow"
          >
            {product.name}
          </li>
        ))}
      </ul>
    </div>
  );
} 