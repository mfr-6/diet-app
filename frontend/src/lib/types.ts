import { z } from 'zod';

export const ProductSchema = z.object({
  id: z.number(),
  name: z.string(),
});

export type Product = z.infer<typeof ProductSchema>;

export const ProductCreateSchema = z.object({
  name: z.string().min(1),
});

export type ProductCreate = z.infer<typeof ProductCreateSchema>; 